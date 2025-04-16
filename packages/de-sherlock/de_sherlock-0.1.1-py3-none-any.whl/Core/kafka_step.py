from loguru import logger
from .prepare_steps import Step
import pandas as pd
import re
from datetime import datetime
import pytz
import os
import json


class KafkaStep(Step):
    def __init__(self, name, title, description, step_number, timestamp, unique_id, config, debugMode=False):
        super().__init__(name, title, description, step_number, timestamp, unique_id, config, debugMode)
        # Create timestamp format for file paths
        self.timestamp_for_file_path = self.timestamp_for_file_path.replace(" ", "_").replace(":", "")
        # Get target path from config or use default
        self.target_path = config.get("target_path", "Data/details")

    def filter_none_values(self, data):
        """Utility to filter out None values from a dictionary."""
        return {k: v for k, v in data.items() if v is not None}

    def build_data_preview(self, data):
        """Build a preview of data for display in the step description."""
        if isinstance(data, pd.DataFrame):
            # Convert datetime columns to string to ensure JSON serialization
            for col in data.select_dtypes(include=['datetime64[ns]']).columns:
                data[col] = data[col].astype(str)
            return {"columns": data.columns.tolist(), "data": data.head(10).to_dict(orient='records')}
        elif isinstance(data, str):
            # For string data, show first 50 lines
            preview = data.splitlines()[:50]
            if len(preview) < len(data.splitlines()):
                preview.append("...")
            return {"data": preview}
        elif isinstance(data, list):
            # For list data, show first 20 items
            preview = data[:20]
            if len(preview) < len(data):
                preview.append("...")
            return {"data": preview}
        else:
            if self.DebugMode:
                logger.error("Unsupported data type for data.")
            return {"data": []}

    def extract_step_number(self):
        """Extracts the trailing number from the step number or defaults to 0."""
        match = re.search(r'(\d+)$', getattr(self, 'step_number', ''))
        return int(match.group(1)) if match else 0

    def get_ist_timestamp(self):
        """Returns the current timestamp in IST format."""
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist).strftime("%d %b %Y %I:%M:%S %p")

    def process_step_kafka(self, topic=None, key_field=None, compression_type=None, batch_size=None, input_df=None,
                           output_df=None, status="Not Executed", bootstrap_servers=None,
                           security_protocol=None, sasl_mechanism=None, sasl_username=None, sasl_password=None,
                           error=None,
                           ssl_key_password=None, ssl_ca_location=None, ssl_certificate_location=None,
                           offset_reset=None, group_id=None):
        """
        Process and store Kafka step information locally.

        Args:
            topic (str, optional): Kafka topic
            key_field (str, optional): Field to use as message key
            compression_type (str, optional): Compression type for Kafka messages
            batch_size (int, optional): Batch size for Kafka operations
            input_df (DataFrame, optional): Input DataFrame
            output_df (DataFrame, optional): Output DataFrame
            status (str): Status of the step execution
            bootstrap_servers (str, optional): Kafka bootstrap servers
            security_protocol (str, optional): Security protocol for Kafka
            sasl_mechanism (str, optional): SASL mechanism for authentication
            sasl_username (str, optional): SASL username
            sasl_password (str, optional): SASL password
            error (str, optional): Error message if any
            ssl_key_password (str, optional): SSL key password
            ssl_ca_location (str, optional): SSL CA certificate location
            ssl_certificate_location (str, optional): SSL certificate location
            offset_reset (str, optional): Consumer offset reset strategy
            group_id (str, optional): Consumer group ID
        """
        step_number = self.extract_step_number()
        name = getattr(self, 'name', 'kafkastep')

        logger.info(f"Step #{step_number} {name} process started")
        if self.DebugMode:
            logger.debug(f"Processing step {step_number or 'Unknown'} started.")

        # Build the main information dictionary
        main_info = self.filter_none_values({
            "step_number": step_number,
            "type": "kafka",
            "name": name,
            "title": getattr(self, 'title', 'Kafka Event Publisher'),
            "description": getattr(self, 'description', None),
            "status": status,
            "error": error,
            "timestamp": self.get_ist_timestamp(),
            "Class_timestamp": self.timestamp_for_file_path
        })

        # Add connection parameters
        main_info["connection_params"] = self.filter_none_values({
            "bootstrap_servers": bootstrap_servers,
            "security_protocol": security_protocol,
            "sasl_mechanism": sasl_mechanism,
            "sasl_username": sasl_username,
            "sasl_password": sasl_password,
            "ssl_key_password": ssl_key_password,
            "ssl_ca_location": ssl_ca_location,
            "ssl_certificate_location": ssl_certificate_location
        })

        # Add config parameters
        main_info["config_params"] = self.filter_none_values({
            "topic": topic,
            "key_field": key_field,
            "compression_type": compression_type,
            "batch_size": batch_size,
            "offset_reset": offset_reset,
            "group_id": group_id
        })

        # Add input DataFrame preview if provided
        if input_df is not None:
            main_info["input_preview"] = self.build_data_preview(input_df)

        # Add output DataFrame preview if provided
        if output_df is not None:
            main_info["output_preview"] = self.build_data_preview(output_df)

        # Update status based on error
        main_info["status"] = "error" if error is not None else "completed"

        # Save to local storage
        try:
            # Create directory structure for this run
            folder_path = os.path.join(
                self.target_path,
                self.unique_id,
                self.timestamp_for_file_path
            )
            os.makedirs(folder_path, exist_ok=True)
            print(name)

            # Save step info to JSON file
            step_file_path = os.path.join(folder_path, f"{name}.json")
            with open(step_file_path, "w", encoding="utf-8") as f:
                json.dump(main_info, f, indent=4, ensure_ascii=False)

            logger.info(f"{name} stored successfully in local storage at time: {self.timestamp_for_file_path}")
            return True

        except Exception as e:
            logger.error(
                f"Error occurred: {name} not stored successfully in local storage at time: {self.timestamp_for_file_path}. Error: {str(e)}")
            return False