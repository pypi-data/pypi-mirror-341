import json
import os
import subprocess
from pathlib import Path
import logging
from go4py.types import GoFunction


logger = logging.getLogger(__name__)


def get_go_functions(module_folder: str):
    """list all go exported functions in the go module"""

    # Path to the generated functions.json file
    functions_json_path = Path("artifacts/functions.json")

    # Check if the functions.json file was generated
    if not functions_json_path.exists():
        logger.error(f"Error: {functions_json_path} was not generated")
        raise FileNotFoundError(f"{functions_json_path} was not generated")

    # Read the functions.json file
    logger.debug(f"Reading functions from: {functions_json_path.name}")
    with open(functions_json_path, "r") as f:
        functions_data = json.load(f)

    # Generate GoFunction objects from the JSON data
    go_functions = []
    for func_data in functions_data:
        try:
            go_function = GoFunction.model_validate(func_data)
            go_functions.append(go_function)
            # print(f"Parsed function: {go_function.name}")
        except Exception as e:
            logger.warning(
                f"function skipped: {func_data['name']} (set log-level to DEBUG for more info)"
            )
            logger.debug(f"Error: {e}")

    logger.info(f"Successfully parsed {len(go_functions)} functions")

    # Return the list of GoFunction objects for further processing
    return go_functions
