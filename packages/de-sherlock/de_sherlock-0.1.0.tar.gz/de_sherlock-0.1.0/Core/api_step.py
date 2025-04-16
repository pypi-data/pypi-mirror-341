from loguru import logger
from .prepare_steps import Step
import pandas as pd
import re
from datetime import datetime
import pytz
import os
import json


class APIStep(Step):
    def __init__(self, name, title, description, step_number, timestamp, unique_id, config, debugMode=False):
        super().__init__(name, title, description, step_number, timestamp, unique_id, config, debugMode)
        # Create timestamp format for file paths
        self.timestamp_for_file_path = self.timestamp_for_file_path.replace(" ", "_").replace(":", "")
        # Get target path from config or use default
        self.target_path = config.get("target_path", "./data_storage")

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
        """Extracts the trailing number from the step name or defaults to 0."""
        match = re.search(r'(\d+)$', getattr(self, 'step_number', ''))
        return int(match.group(1)) if match else 0

    def get_ist_timestamp(self):
        """Returns the current timestamp in IST format."""
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist).strftime("%d %b %Y %I:%M:%S %p")

    def process_step_api(self, url=None, request_type=None, payload=None, username=None, password=None, hostname=None,
                     port=None, ssl_value=None, input_df=None, output_df=None, step_number=None,
                     status="Not Executed", error=None):
        """
        Process and store API step information locally.

        Args:
            url (str, optional): API endpoint URL
            request_type (str, optional): HTTP method (GET, POST, etc.)
            payload (dict, optional): Data payload for the request
            username (str, optional): API authentication username
            password (str, optional): API authentication password
            hostname (str, optional): API hostname
            port (int, optional): API port
            ssl_value (bool, optional): Whether to use SSL
            input_df (DataFrame, optional): Input DataFrame
            output_df (DataFrame, optional): Output DataFrame
            step_number (int, optional): Step number (extracted automatically if not provided)
            status (str): Status of the step execution
            error (str, optional): Error message if any
        """
        step_number = self.extract_step_number()
        name = getattr(self, 'name', 'apistep')

        logger.info(f"Step #{step_number} {name} process started")
        if self.DebugMode:
            logger.debug(f"Processing step {step_number or 'Unknown'} started.")

        # Build the main information dictionary
        main_info = self.filter_none_values({
            "step_number": step_number,
            "type": "api",
            "name": name,
            "title": getattr(self, 'title', 'API Request Handler'),
            "description": getattr(self, 'description', None),
            "status": status,
            "error": error,
            "timestamp": self.get_ist_timestamp()
        })

        # Add connection parameters
        main_info["connection_params"] = self.filter_none_values({
            "username": username,
            "password": password,
            "hostname": hostname,
            "port": port,
            "ssl_value": ssl_value
        })

        # Add config parameters
        main_info["config_params"] = self.filter_none_values({
            "url": url,
            "request_type": request_type,
            "payload": payload
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