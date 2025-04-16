from loguru import logger
from .prepare_steps import Step
import pandas as pd
import re
from datetime import datetime
import pytz
import os
import json


class OracleStep(Step):
    def __init__(self, name, title, description, step_number, timestamp, unique_id, config, debugMode,pvc_root_directory):
        super().__init__(name, title, description, step_number, timestamp, unique_id, config, debugMode,pvc_root_directory)
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
        """Extracts the trailing number from the step number or defaults to 0."""
        match = re.search(r'(\d+)$', getattr(self, 'step_number', ''))
        return int(match.group(1)) if match else 0

    def get_ist_timestamp(self):
        """Returns the current timestamp in IST format."""
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist).strftime("%d %b %Y %I:%M:%S %p")

    def process_step_oracle(self, table_name=None, sql_query=None, username=None, password=None, service_name=None,
                      hostname=None, port=None, input_df=None, output_df=None, step_number=None,
                      status="Not Executed", error=None):
        """
        Process and store Oracle step information locally.

        Args:
            table_name (str, optional): Oracle table name
            sql_query (str, optional): SQL query for Oracle
            username (str, optional): Oracle username
            password (str, optional): Oracle password
            service_name (str, optional): Oracle service name
            hostname (str, optional): Oracle host
            port (int, optional): Oracle port
            input_df (DataFrame, optional): Input DataFrame
            output_df (DataFrame, optional): Output DataFrame
            step_number (int, optional): Step number (extracted automatically if not provided)
            status (str): Status of the step execution
            error (str, optional): Error message if any
        """
        step_number = self.extract_step_number()
        name = getattr(self, 'name', 'oraclestep')
        pvc_root_directory = getattr(self, 'pvc_root_directory', None)

        logger.info(f"Step #{step_number} {name} process started")
        if self.DebugMode:
            logger.debug(f"Processing step {step_number or 'Unknown'} started.")

        # Build the main information dictionary
        main_info = self.filter_none_values({
            "step_number": step_number,
            "name": name,
            "type": "oracle",
            "title": getattr(self, 'title', 'Oracle Data Handler'),
            "description": getattr(self, 'description', None),
            "status": status,
            "error": error,
            "timestamp": self.get_ist_timestamp()
        })

        # Add connection parameters
        main_info["connection_params"] = self.filter_none_values({
            "username": username,
            "password": password,
            "service_name": service_name,
            "hostname": hostname,
            "port": port
        })

        # Add config parameters
        main_info["config_params"] = self.filter_none_values({
            "table_name": table_name,
            "sql_query": sql_query
        })

        # Add input preview if provided
        if input_df is not None:
            main_info["input_preview"] = self.build_data_preview(input_df)

        # Add output preview if provided
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
            allstep_path = os.path.join(pvc_root_directory, folder_path)
            os.makedirs(allstep_path, exist_ok=True)

            # Save step info to JSON file
            step_file_path = os.path.join(allstep_path, f"{name}.json")
            with open(step_file_path, "w", encoding="utf-8") as f:
                json.dump(main_info, f, indent=4, ensure_ascii=False)

            logger.info(f"{name} stored successfully in local storage at time: {self.timestamp_for_file_path}")
            return True

        except Exception as e:
            logger.error(
                f"Error occurred: {name} not stored successfully in local storage at time: {self.timestamp_for_file_path}. Error: {str(e)}")
            return False