# workspace_generator.py

import yaml
import logging
from ..base.constants import *
from ..base.file_generator import FileGenerator

class EnvFileGenerator(FileGenerator):
    """
    A class to generate the Azure workspace configuration file

    Attributes:
        config_file_path (str): The path to the config file
        output_file_path (str): The path to the generated file

    Methods:
        generate(): Generate the workspace .env file 

    """

    def __init__(self,config_file_path: str, output_file_path: str):
        """
        Initialize the Azure workspace generator with the template file path and the generated file path
        Args:
            config_file_path (str): The path to the template file
            output_file_path (str): The path to the generated file
        """
        super().__init__(config_file_path, output_file_path)

    @staticmethod
    def generate_phase_resources(phase:str, phase_configs_value:dict, content: dict) -> dict:
        """
        Generate the resources for the training or inference phase
        The configurations for the phase declared in the yaml file will be used, if not found, default values will be used.
        Args:
            phase (str): The phase name
            phase_configs_value (dict): The configurations for the phase declared in the yaml file
            content (dict): The content to be generated in the .env file. 
        Returns:
            dict: The content with the configurations for the phase
        """
        config_resources_data = {
                COMPUTE_NAME :EMPTY_CONSTANT, 
                MIN_INSTANCES: DEFAULT_MIN_INSTANCES,
                MAX_INSTANCES: DEFAULT_MAX_INSTANCES, 
                COMPUTE_TYPE: DEFAULT_COMPUTE_TYPE, 
                VM_SIZE: DEFAULT_VM_SIZE,
                COMPUTE_USER_ASSIGNED_IDENTITY: DEFAULT_COMPUTE_USER_ASSIGNED_IDENTITY,
                IDLE_SECONDS_BEFORE_SCALE_DOWN: DEFAULT_IDLE_SECONDS_BEFORE_SCALE_DOWN, 
                TIER: DEFAULT_TIER,
                SUBNET: DEFAULT_SUBNET,
                ENVIRONMENT_NAME: EMPTY_CONSTANT,
                ENVIRONMENT_VERSION: DEFAULT_ENVIRONMENT_VERSION,
                ENVIRONMENT_IMAGE: DEFAULT_ENVIRONMENT_IMAGE ,
                ENDPOINT_NAME: EMPTY_CONSTANT,
                DEPLOYMENT_NAME: EMPTY_CONSTANT,
                }
        if phase_configs_value:
            for key,default_value in config_resources_data.items():
                content_key = phase + "_" + key
                content[content_key] = phase_configs_value.get(key, default_value)
                if not phase_configs_value.get(key, ""):
                    logging.info(f"{key} in {phase} phase is not found in template file, set to {default_value}")
        else:
            logging.warning(f"{phase} configuration not found in the template file")
        return content
    
    def write_file(self, data: dict, output_file_path: str) -> None:
        with open(output_file_path, 'w') as file:
                for key,value in data.items():
                    file.write(f"{key.upper()}={value}\n")
                logging.info("Workspace configuration file generated")
    def generate(self) -> None:
        """
        Generate the workspace .env file
        For some configurations, if they are not found in the template file, default values will be used.
        Returns:
            A .env file with the workspace configuration will be generated
        """
        try:
            # Load the data from the YAML file
            data = self.get_config()

            # Initialize the content dictionary, this includes all the configurations will be written to the .env file
            content = {}

            general_config_data = {
                RESOURCE_GROUP: DEFAULT_RESOURCE_GROUP,
                WORKSPACE_NAME: DEFAULT_WORKSPACE_NAME,
                LOCATION: DEFAULT_LOCATION,
                EXPERIMENT_NAME: DEFAULT_EXPERIMENT_NAME,
                RUN_NAME: EMPTY_CONSTANT,
                TAGS: DEFAULT_TAGS,
                DESCRIPTION: EMPTY_CONSTANT,
                MODEL_NAME: EMPTY_CONSTANT,
                MODEL_PATH: EMPTY_CONSTANT,
                MODEL_VERSION: EMPTY_CONSTANT,
                MODEL_TYPE: DEFAULT_MODEL_TYPE,
            }
            for key,default_value in general_config_data.items():
                content[key] = data.get(key, default_value)
                if key not in data:
                    logging.info(f"{key} not found in template file, using {default_value}")
            

            phase_configs = {
                TRAINING_PHASE: data.get(TRAINING_PHASE, {}), 
                INFERENCE_PHASE: data.get(INFERENCE_PHASE, {})
            }
            for phase, phase_configs_value in phase_configs.items():
                content = self.generate_phase_resources(phase, phase_configs_value, content)
            
            # Write the content to the .env file
            self.write_file(content, self.output_file_path)

        except Exception as e:
            logging.error(f"Workspace generator, an error occurred with: {e}")            

    
