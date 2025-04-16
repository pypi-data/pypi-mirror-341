import ast
import json
import os
import shlex
import time

from loguru import logger


def get_kubeconfig_path():
    """
    Returns the path to the kubeconfig file included in the package.
    """
    # This function can remain as a stub for compatibility
    return None


def perpare_data_to_pvc(config, unique_id, steps_data, class_current_timestamp, step_file_name, DebugMode):
    """
    Redirects to perpare_data_to_local since we're replacing PVC with local storage.

    This function maintains the original signature for backward compatibility.
    """
    return perpare_data_to_local(config, unique_id, steps_data, class_current_timestamp, step_file_name, DebugMode)


def perpare_data_to_local(config, unique_id, steps_data, class_current_timestamp, step_file_name, DebugMode):
    """
    Prepare data and push it to a local path.

    Args:
        config: Configuration dictionary containing target_path settings
        unique_id: Unique identifier for the data
        steps_data: Data to store in the step file
        class_current_timestamp: Timestamp string
        step_file_name: Name of the output file
        DebugMode: Enable debug logging
    """
    try:
        if not all([config, unique_id]):
            if DebugMode:
                logger.error("Missing required parameters (config or unique_id) for perpare_data_to_local")
            return

        if DebugMode:
            logger.debug(f"Preparing to push data for unique_id: {unique_id}")

        # Extract target path
        target_path = config.get("target_path")

        if not all([target_path, step_file_name]):
            if DebugMode:
                logger.error("Missing essential configuration for perpare_data_to_local")
            return

        # Generate timestamp folder name
        timestamp_folder = class_current_timestamp.replace(" ", "_").replace(":", "")

        full_folder_path = os.path.join(target_path, unique_id, timestamp_folder)
        os.makedirs(full_folder_path, exist_ok=True)

        file_path = os.path.join(full_folder_path, step_file_name)

        # Write data to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(steps_data, f, ensure_ascii=False, indent=4)

        if DebugMode:
            logger.debug(f"Data successfully written to {file_path}")

        return True

    except Exception as e:
        if DebugMode:
            logger.error(f"Unexpected error in perpare_data_to_local: {e}")
        return


# The following functions are kept as stubs for compatibility but will not be used

def get_or_create_pod(kubeconfig_path, api_version, kind, namespace, pvc_name, name, container_name,
                      container_image, container_command, volume_mount_path, volume_mount_name, volume_name,
                      pvc_claim_name, specified_pod_name, DebugMode):
    """
    Stub function maintained for compatibility. Not used in local storage version.
    """
    if DebugMode:
        logger.debug("get_or_create_pod: Using local storage implementation, this function does nothing.")
    return "local_storage"


def execute_pod_command(v1, pod_name, namespace, command):
    """
    Stub function maintained for compatibility. Not used in local storage version.
    """
    logger.debug("execute_pod_command: Using local storage implementation, this function does nothing.")
    return ""


def create_or_update_step_file(v1, pod_name, namespace, allstep_path, steps_list_data, timestamp,
                               step_file_name, DebugMode):
    """
    Stub function maintained for compatibility. Not used in local storage version.
    """
    if DebugMode:
        logger.debug("create_or_update_step_file: Using local storage implementation, this function does nothing.")
    return True


def push_data_to_pvc(unique_id, pod_name, kubeconfig_path, namespace, target_path, timestamp,
                     timestamp_folder, step_data, step_file_name, DebugMode):
    """
    Stub function that redirects to local storage implementation.
    Maintained for compatibility.
    """
    try:
        config = {"target_path": target_path}
        return perpare_data_to_local(config, unique_id, step_data, timestamp, step_file_name, DebugMode)
    except Exception as e:
        if DebugMode:
            logger.error(f"Unexpected error in push_data_to_pvc (redirected to local): {e}")
        return