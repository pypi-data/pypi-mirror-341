import yaml
import logging
import sys
import os
from collections import OrderedDict, namedtuple
from typing import Union
from ..base.constants import *
from ..base.file_generator import FileGenerator

SourceCodePath = namedtuple('SourceCodePath', ['folder_path', 'script_name'])
Compute = namedtuple('Compute', ['name', 'instance_count'])
yaml.add_representer(OrderedDict, FileGenerator.represent_ordereddict)

class AzOnlineDeploymentFileGenerator(FileGenerator):
    """
    A class to generate the Azure Managed Online Deployment Endpoint file

    Attributes:
        config_file_path (str): The path to the config file
        output_file_path (str): The path to the generated file

    Methods:
        get_inference_values(data: dict): Retrieve the inference values from the configuration data
        get_environment_values(data: dict): Retrieve the environment values from the configuration data
        get_source_code_path(data: dict): Retrieve the source code path from the configuration data
        generate(): Generate Azure Azure Managed Online Deployment Endpoint file
    """

    def __init__(self,config_file_path: str, output_file_path: str):
        super().__init__(config_file_path, output_file_path)

    @staticmethod
    def get_inference_values(data: dict, inference_type:str) -> dict:
        """
        Retrieve the inference values from the configuration data

        Args:
            data (dict): The configuration data

        Returns:
            dict: A dictionary containing the inference values
        """
        try:
            inference_values = data.get(INFERENCE_PHASE, EMPTY_CONSTANT)
            if inference_values == EMPTY_CONSTANT:
                raise Exception("Inference values not found in the configuration data")
            if inference_values.get(ENDPOINT_TYPE, EMPTY_CONSTANT) != inference_type:
                raise Exception(f"{inference_type} type not set in the configuration data")
            return inference_values
        except Exception as e:
            logging.error(f"Error occurred while retrieving the inference values: {e}")

    @staticmethod
    def get_environment_values(inference_values: dict) -> Union[str, dict]:
        """
        Retrieve the environment values from the configuration data
        If environment name and version are found, it means environment is already created
        If not found, it means the custom environment will be created using a dockerfile

        Args:
            data (dict): The configuration data

        Returns:
            dict: A dictionary containing the environment values
        """
        environment = {}
        environment["name"] = inference_values.get(ENVIRONMENT_NAME, EMPTY_CONSTANT)
        environment["version"] = inference_values.get(ENVIRONMENT_VERSION, EMPTY_CONSTANT)
        environment["docker_file_path"] = inference_values.get(DOCKER_FILE_PATH, EMPTY_CONSTANT)
        for k,v in environment.items():
            if not v :
                logging.info(f" Environment {k} not found in the inference configuration data")
        if environment["name"] and environment["version"]:
            environment_values = f"azureml:{environment['name']}:{environment['version']}"
            return environment_values
        if environment["docker_file_path"]:
            environment_values = {"build":{
                                    "path": environment["docker_file_path"]}
                                }
            return environment_values
            
    @staticmethod
    def get_source_code_path(inference_value: dict) -> namedtuple:
        """
        Retrieve the source code path from the configuration data

        Args:
            inference_value (dict): Inference configuration data

        Returns:
            str: The source code path
        """

        source_code_path = inference_value.get(SCORING_SCRIPT_PATH, EMPTY_CONSTANT)
        if not source_code_path:
            logging.info("Scoring script path not found in the configuration data")
            return SourceCodePath(EMPTY_CONSTANT, EMPTY_CONSTANT)
        folder_path = os.path.dirname(source_code_path)
        score_script_name = os.path.basename(source_code_path)
        return SourceCodePath(folder_path, score_script_name)


    @staticmethod
    def check_required_values(to_check: dict) -> None:
        """
        Check if the required values are present in the dictionary
        """
        for k,v in to_check.items():
            if not v:
                raise ValueError(f"{k} not found in the configuration data")
    
    def add_optional_config(self,deployment_stream: dict, inference_values: dict) -> dict:
        """
        Add optional configurations to the deployment stream

        Args: 
            deployment_stream (dict): The deployment stream
            inference_values (dict): Inference configuration data
        Returns:
            dict: The deployment stream with optional configurations if declared
        """
        # Add request and traffic settings to the deployment stream if declared
        try:
            optional_config = {
                    "request_settings":[
                        REQUEST_TIMEOUT_MS, 
                        MAX_CONCURRENT_REQUESTS_PER_INSTANCE, 
                        MAX_QUEUE_WAIT_MS
                        ],
                    "liveness_probe":[
                        LIVENESS_PROBE_INITIAL_DELAY,
                        LIVENESS_PROBE_PERIOD,
                        LIVENESS_PROBE_TIMEOUT,
                        LIVENESS_PROBE_FAILURE_THRESHOLD,
                        LIVENESS_PROBE_SUCCESS_THRESHOLD,
                    ],
                    "readiness_probe":[
                        READINESS_PROBE_INITIAL_DELAY,
                        READINESS_PROBE_PERIOD,
                        READINESS_PROBE_TIMEOUT,
                        READINESS_PROBE_FAILURE_THRESHOLD,
                        READINESS_PROBE_SUCCESS_THRESHOLD
                    ]
                }
            for group,configs in optional_config.items():
                declared_configs = {}
                for config in configs:
                    config_value = inference_values.get(config, EMPTY_CONSTANT)
                    if config_value:
                        declared_configs[config] = config_value
                    else:
                        logging.info(f"{config} not found in the configuration data ")
                if declared_configs:
                    deployment_stream[group] = declared_configs
            # Add the model path to the deployment stream if declared
            model_path = inference_values.get(MODEL, EMPTY_CONSTANT)
            if model_path:
                deployment_stream["model"] = model_path

            # Add code configuration to the deployment stream if declared
            source_code_values = self.get_source_code_path(inference_values)
            if source_code_values.folder_path and source_code_values.script_name:
                deployment_stream['code_configuration']= {
                                'code':source_code_values.folder_path , 
                                'scoring_script': source_code_values.script_name
                                }
        except Exception as e:
            logging.error(f"Error occurred while adding optional config to the deployment stream: {e}")
        return deployment_stream
    
    def write_file(self, data: OrderedDict) -> None:
        """
        Write the content to the .yaml file

        Args:
            data (Ordereddict): Data to write to the file
        """
        with open(self.output_file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
            logging.info(f"Online Endpoint Deployment file generated at {self.output_file_path}")

    def generate(self) -> None:
        """
        Generate Azure Managed Online Deployment Endpoint file
        
        Returns:
            An Azure Managed Online Deployment Endpoint file will be generated
        """
        try:
            # Load the data from the YAML file
            data = self.get_config()
            
            inference_values = self.get_inference_values(data, ONLINE_INFERENCE)
            environment_value = self.get_environment_values(inference_values)
            deployment_name = inference_values.get(DEPLOYMENT_NAME, EMPTY_CONSTANT)
            endpoint_name = inference_values.get(ENDPOINT_NAME, EMPTY_CONSTANT)
            
            # Perform a check to ensure that environment, deployment_name, and endpoint_name are not empty
            to_check = {
                "environment": environment_value,
                  "deployment_name": deployment_name, 
                  "endpoint_name": endpoint_name
                  }
            self.check_required_values(to_check)

            # Initialize the content dictionary, this includes all the configurations will be written to the .yaml file
            deployment_stream = OrderedDict([
                    ('$schema',MANAGED_ONLINE_INFERENCE_SCHEMA),
                    ('name', deployment_name),
                    ('endpoint_name',endpoint_name),
                    ('egress_public_network_access',EGRESS_PUBLIC_NETWORK_ACCESS_DEFAULT),
                    ('environment', environment_value),
                    ('instance_type', inference_values.get(INSTANCE_TYPE, DEFAULT_VM_SIZE)),
                    ('instance_count', inference_values.get(INSTANCE_COUNT, DEFAULT_MAX_INSTANCES)),
                    ('app_insights_enabled', inference_values.get(APP_INSIGHTS_ENABLED, FALSE_CONSTANT)),
                    ('environment_variables', inference_values.get(ENVIRONMENT_VARIABLES, EMPTY_CONSTANT))
                ])
            # For optional config, only add in the content dictionary if the value is declared
            updated_deployment_stream = self.add_optional_config(deployment_stream, inference_values)
    
            self.write_file( updated_deployment_stream)

        except Exception as e:
            logging.error(f"AzOnlineDeploymentFileGenerator, an error occurred with: {e}")            

    
class AzBatchDeploymentFileGenerator(FileGenerator):
    """
    A class to generate the Azure Managed Batch Deployment Endpoint file
    Attributes:
        config_file_path (str): The path to the config file
        output_file_path (str): The path to the generated file
    Methods:
        generate(): Generate Azure Azure Managed Batch Deployment Endpoint file
    """

    def __init__(self, config_file_path: str, output_file_path: str):
        super().__init__(config_file_path, output_file_path)
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    @staticmethod
    def get_compute(inference_values: dict) -> str:
        """
        Retrieve the compute from the configuration data

        Args:
            inference_values (dict): The configuration data

        Returns:
            str: The compute
        """
        try:
            compute_name = inference_values.get(COMPUTE_NAME, EMPTY_CONSTANT)
            compute_instance_count = inference_values.get(INSTANCE_COUNT, EMPTY_CONSTANT)
            if not compute_name:
                raise Exception("Compute name not found in the configuration data")
            if not compute_instance_count:
                raise Exception("Instance count not found in the configuration data")
            return Compute(compute_name, compute_instance_count)
        except Exception as e:
            logging.error(f"Error occurred while retrieving the compute name for AzBatchDeploymentFileGenerator: {e}")
    @staticmethod
    def get_retry_optional_config(inference_values: dict) -> dict:
        """
        Retrieve the retry optional config from the configuration data

        Args:
            inference_values (dict): The configuration data

        Returns:
            dict: A dictionary containing the retry optional config
        """
        retry_optional_config = {}
        max_retries = inference_values.get(MAX_RETRIES, EMPTY_CONSTANT)
        if max_retries:
            logging.info("Max retries declared in the configuration data")
            retry_optional_config["max_retries"]= max_retries
        timeout = inference_values.get(TIMEOUT, EMPTY_CONSTANT)
        if timeout:
            logging.info("Timeout declared in the configuration data")
            retry_optional_config["timeout"]= timeout
        return retry_optional_config
    @staticmethod
    def add_optional_settings_config(deployment_stream: dict, inference_values: dict) -> dict:
        """
        Add optional settings configurations to the deployment stream
        
        Args:
            deployment_stream (dict): The deployment stream
            inference_values (dict): Inference configuration data
        Returns:
            dict: The deployment stream with optional settings configurations if declared
        """
        settings_optional_config = [
                    MAX_CONCURRENCY_PER_INSTANCE, 
                    MINI_BATCH_SIZE, 
                    OUTPUT_ACTION, 
                    OUTPUT_FILE_NAME,
                    ERROR_THRESHOLD, 
                    LOGGING_LEVEL, 
                    ENVIRONMENT_VARIABLES,
                    ]
        settings = {}
        for config in settings_optional_config:
            config_value = inference_values.get(config, EMPTY_CONSTANT)
            if config_value:
                settings[config] = config_value
            else:
                logging.info(f"{config} not found in the configuration data ")
    
        if settings:
            deployment_stream["settings"] = settings
        return deployment_stream

    def write_file(self, data: OrderedDict) -> None:
        """
        Write the content to the .yaml file
        Args:
            data (Ordereddict): Data to write to the file
        """
        with open(self.output_file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
            logging.info(f"Batch Endpoint Deployment file generated at {self.output_file_path}")

    def generate(self) -> None:
        """
        Generate Azure Azure Managed Batch Deployment Endpoint file
        
        Returns:
            A Azure Azure Managed Batch Deployment Endpoint file to deploy an endpoint will be generated
        """
        try:
            # Load the data from the YAML file
            data = self.get_config()
            
            inference_values = AzOnlineDeploymentFileGenerator.get_inference_values(data, BATCH_INFERENCE)
            source_code_values = AzOnlineDeploymentFileGenerator.get_source_code_path(inference_values)
            environment_value = AzOnlineDeploymentFileGenerator.get_environment_values(inference_values)
            deployment_name = inference_values.get(DEPLOYMENT_NAME, EMPTY_CONSTANT)
            endpoint_name = inference_values.get(ENDPOINT_NAME, EMPTY_CONSTANT)
            compute = self.get_compute(inference_values)
            
            # Perform a check to ensure that the environment, deployment_name, and endpoint_name are not empty
            to_check = {
                "environment": environment_value,
                  "deployment_name": deployment_name, 
                  "endpoint_name": endpoint_name
                  }
            AzOnlineDeploymentFileGenerator.check_required_values(to_check)
            # Initialize the content dictionary, this includes all the configurations will be written to the .env file
            deployment_stream = OrderedDict([
                    ('$schema',MANAGED_BATCH_INFERENCE_SCHEMA),
                    ('name', deployment_name),
                    ('endpoint_name',endpoint_name),
                    ('type', BATCH_MODEL_TYPE),
                    ('model', inference_values.get(MODEL, EMPTY_CONSTANT)),
                    ('code_configuration', {
                        'code':source_code_values.folder_path , 
                        'scoring_script': source_code_values.script_name
                    }),
                    ('environment', environment_value),
                    ('compute', f"azureml:{compute.name}"),
                    ('resources', {
                        'instance_count': compute.instance_count
                    }),
                                
                    ('environment_variables', inference_values.get(ENVIRONMENT_VARIABLES, EMPTY_CONSTANT ))
            ])

            updated_deployment_stream = self.add_optional_settings_config(deployment_stream, inference_values)
            
            # add the retry optional config to the deployment_stream
            retry_optional_config = self.get_retry_optional_config(inference_values)

            if retry_optional_config:#list(retry_optional_config.values()):
                updated_deployment_stream["settings"]["retry_settings"] = retry_optional_config

            self.write_file(updated_deployment_stream)

        except Exception as e:
            logging.error(f"Azure Managed Batch deployment file generator, an error occurred with: {e}")

    
    