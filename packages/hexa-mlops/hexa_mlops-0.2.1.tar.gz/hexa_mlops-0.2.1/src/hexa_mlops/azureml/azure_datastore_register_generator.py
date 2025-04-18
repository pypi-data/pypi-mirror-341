import yaml
import logging
import sys
import os
from collections import OrderedDict, namedtuple
from typing import Union
from ..base.constants import *
from ..base.file_generator import FileGenerator


yaml.add_representer(OrderedDict, FileGenerator.represent_ordereddict)

class AzDatastoreRegisterFileGenerator(FileGenerator):
    """
    A class to generate the Azure ML Datastore Register file

    Attributes:
        config_file_path (str): The path to the config file
        output_file_path (str): The path to the generated file

    Methods:
        get_values(data: dict): Retrieve datastore values from the configuration data
        generate(): Generate Azure Azure Managed Online Deployment Endpoint file
    """

    def __init__(self,config_file_path: str, output_file_path: str):
        super().__init__(config_file_path, output_file_path)

    @staticmethod
    def check_required_values(data: dict) -> dict:
        """
        Check if required data is declared

        Args:
            data (dict): configuration data
        """
        check_list = [
            DATASTORE_NAME,
            STORAGE_ACCOUNT_NAME,
            FILE_SYSTEM_NAME,
            TENANT_ID,
            CLIENT_ID
        ]
        for key in check_list:
            if key not in data or not data[key]:
                raise ValueError(f"Missing or empty required value: {key}")

    
    def write_file(self, data: OrderedDict) -> None:
        """
        Write the content to the .yaml file

        Args:
            data (Ordereddict): Data to write to the file
        """
        with open(self.output_file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
            logging.info(f"Online Endpoint Deployment file generated at {self.output_file_path}")

    def add_optional_config(self,stream: dict, data: dict) -> dict:
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
            optional_config = [DESCRIPTION, TAGS, DATA_ENDPOINT]
            for config in optional_config:
                config_value = data.get(config, EMPTY_CONSTANT)
                if config_value:
                    stream[config] = config_value
        except Exception as e:
            logging.error(f"Error occurred while adding optional config to the deployment stream: {e}")
        return stream

    def generate(self) -> None:
        """
        Generate Azure Managed Online Deployment Endpoint file
        
        Returns:
            An Azure Managed Online Deployment Endpoint file will be generated
        """
        try:
            # Load the data from the YAML file
            data = self.get_config()
            
            self.check_required_values(data)

            # Initialize the content dictionary, this includes all the configurations will be written to the .yaml file
            deployment_stream = OrderedDict([
                    ('$schema',DATALAKE_ZEN_2_DATASTORE_SCHEMA),
                    ('type', AZURE_DATALAKE_GEN2), 
                    ('name', data.get(DATASTORE_NAME)),
                    ('account_name',data.get(STORAGE_ACCOUNT_NAME)),
                    ('filesystem',data.get(FILE_SYSTEM_NAME)),
                    ('credentials', {
                        'tenant_id': data.get(TENANT_ID),
                        'client_id': data.get(CLIENT_ID)
                    })
                    ])
            protocol = data.get(PROTOCOL)
            if not protocol:
                deployment_stream['protocol'] = HTTPS
            else:
                if protocol in [HTTPS, ABFSS]:
                    deployment_stream['protocal'] = protocol
                else:
                    logging.error(f"Protocal value '{protocol}' is not allowed. Options: {HTTPS} or {ABFSS}")

            # For optional config, only add in the content dictionary if the value is declared
            updated_deployment_stream = self.add_optional_config(deployment_stream, data)
    
            self.write_file(updated_deployment_stream)

        except Exception as e:
            logging.error(f"AzDatastoreFileGenerator, an error occurred with: {e}")   