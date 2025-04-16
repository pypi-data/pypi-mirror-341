import os
import json
from datetime import datetime
import yaml
from loguru import logger
from importlib.resources import path as resource_path

from de_sherlock.api_step import APIStep
from de_sherlock.description_step import DescriptionStep
from de_sherlock.kafka_step import KafkaStep
from de_sherlock.elastic_step import ElasticStep
from de_sherlock.oracle_step import OracleStep
from de_sherlock.prepare_steps import Step
from de_sherlock.transform_step import TransformStep


class StepInitializer:
    STEP_CLASSES = {
        "kafkastep": KafkaStep,
        "elasticstep": ElasticStep,
        "oraclestep": OracleStep,
        "apistep": APIStep,
        "transformstep": TransformStep,
        "descriptionstep": DescriptionStep,
    }

    def __init__(self, unique_id, pvc_root_directory, mode=None, debugMode=False,**step_details):
        """
        Initializes steps in the provided sequence.
        Supports repeated steps with unique identifiers.
        """
        self.DebugMode = debugMode
        self.pvc_root_directory = pvc_root_directory
        self.steps = []
        self.step_data = []
        self.config = self._load_config()
        self.allowed_steps = self.config.get('allowed_steps', [])
        self.mode = mode if mode else self.config.get("mode")
        self.unique_id = str(unique_id)
        self.current_timestamp = datetime.now().strftime("%d-%b-%Y %I:%M%p")

        # Initialize steps
        for step_counter, (step_key, step_info) in enumerate(step_details.items(), start=1):
            base_step_name = ''.join(filter(lambda x: not x.isdigit(), step_key))

            if base_step_name not in self.allowed_steps:
                raise ValueError(
                    f"de-sherlock : Invalid step '{step_key}'. Allowed steps: {self.allowed_steps}"
                )

            step_class = self.STEP_CLASSES.get(base_step_name, Step)
            step_instance = step_class(
                step_info.get('name', step_key),
                step_info.get('title', step_key),
                step_info.get('description', 'No description provided'),
                str(step_counter),
                self.current_timestamp,
                self.unique_id,
                self.config,
                self.DebugMode,
                self.pvc_root_directory
            )

            self.steps.append(step_instance)
            setattr(self, step_key, step_instance)

            # Collect step data in JSON format
            self.step_data.append({
                "step_number": step_counter,
                "title": step_info.get('title', step_key),
                "name": step_info.get('name', step_key),
                "description": step_info.get('description', 'No description provided')
            })

        # Save step data to local storage
        step_file_name = self.config.get("step_file_name", "allsteps")
        time_stamp_file_name = self.config.get("time_stamp_file_name", "timestamp")
        target_path = self.config.get("target_path", "Data/details")

        is_saved = self.save_data_to_local(self.pvc_root_directory,target_path, step_file_name, time_stamp_file_name)
        if is_saved:
            logger.info("All Steps Initialized Successfully and data saved to local storage")
        else:
            logger.error("Error Occurred while saving data to local storage")

    def _load_config(self):
        """Loads the config.yaml file from the 'creds' package"""
        with resource_path("creds", "config.yaml") as config_path:
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)
        return config_data

    def execute_steps(self):
        """Execute all initialized steps"""
        for step in self.steps:
            logger.debug(f"➞ Executing step: {step.name}")

    def get_step_data(self):
        """Return collected step data"""
        return self.step_data

    def save_data_to_local(self,pvc_root_directory, target_path, step_file_name, time_stamp_file_name):
        """Save step data to local storage"""
        try:
            # Create timestamp folder for this run
            timestamp_folder = self.current_timestamp.replace(" ", "_").replace(":", "")

            # Define paths for storage
            allstep_path_relative = os.path.join(target_path, self.unique_id, timestamp_folder)
            timestamp_path_relative = os.path.join(target_path, self.unique_id)

            allstep_path = os.path.join(pvc_root_directory, allstep_path_relative)
            timestamp_path = os.path.join(pvc_root_directory, timestamp_path_relative)

            # Create directories
            os.makedirs(allstep_path, exist_ok=True)
            os.makedirs(timestamp_path, exist_ok=True)

            if self.DebugMode:
                logger.debug(f"Saving to: {allstep_path}, Timestamp path: {timestamp_path}")

            # Save step data file
            allstep_file_path = os.path.join(allstep_path, step_file_name)
            success_allstep = self._save_step_data(allstep_file_path)

            # Save timestamp file
            timestamp_file_path = os.path.join(timestamp_path, time_stamp_file_name)
            success_timestamp = self._save_timestamp(timestamp_file_path)

            return success_allstep and success_timestamp

        except Exception as e:
            if self.DebugMode:
                logger.error(f"Error saving data to local storage: {e}")
            return False

    def _save_step_data(self, file_path):
        """Save step data to JSON file"""
        try:
            # Prepare data structure
            step_data = {
                "consistData": [{"step_data": self.step_data}],
                "timestamp": self.current_timestamp
            }

            # Check if file exists
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)

                    # Update existing data
                    if "consistData" in existing_data and isinstance(existing_data["consistData"], list):
                        existing_data["consistData"].append({"step_data": self.step_data})
                    else:
                        existing_data["consistData"] = [{"step_data": self.step_data}]

                    existing_data["timestamp"] = self.current_timestamp
                    step_data = existing_data

                except (json.JSONDecodeError, Exception) as e:
                    if self.DebugMode:
                        logger.warning(f"Could not read existing step file: {e}. Creating new.")

            # Write data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(step_data, f, ensure_ascii=False, indent=4)

            if self.DebugMode:
                logger.debug(f"Successfully saved step data to {file_path}")
            return True

        except Exception as e:
            if self.DebugMode:
                logger.error(f"Failed to save step data: {e}")
            return False

    def _save_timestamp(self, file_path):
        """Save timestamp to JSON file"""
        try:
            timestamps = []

            # Check if file exists
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        timestamps = json.load(f)
                    if not isinstance(timestamps, list):
                        timestamps = []
                except Exception:
                    if self.DebugMode:
                        logger.warning("Could not read existing timestamp file. Creating new.")

            # Add current timestamp if not already present
            if self.current_timestamp not in timestamps:
                timestamps.append(self.current_timestamp)

            # Write timestamps
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(timestamps, f, ensure_ascii=False, indent=4)

            if self.DebugMode:
                logger.debug(f"Successfully saved timestamp to {file_path}")
            return True

        except Exception as e:
            if self.DebugMode:
                logger.error(f"Failed to save timestamp: {e}")
            return False