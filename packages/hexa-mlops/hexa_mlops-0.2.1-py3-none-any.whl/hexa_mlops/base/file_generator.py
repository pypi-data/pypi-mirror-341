from abc import ABC, abstractmethod
import logging
import yaml
from yaml import Dumper, Node
import sys
from collections import OrderedDict

class FileGenerator(ABC):
    """
    Abstract base class for Azure File Generator classes.
    """

    def __init__(
        self, 
        config_file_path: str, 
        output_file_path: str,
    ):
        """
        Initializes an instance of the AzGenerator class.

        Args:
            config_file_path (str): The path to the configuration file.
            output_file_path (str): The path to the generated file.
        """
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
        self.config_file_path = config_file_path
        self.output_file_path = output_file_path

    def get_config(self):
        """
        Retrieves configuration information from a YAML file.

        Returns:
            dict: A dictionary containing configuration information.
        """
        logging.info(f"Retrieving configuration from file: {self.config_file_path}")
        try:
            with open(self.config_file_path, 'r') as file:
                docs = yaml.safe_load(file)
                return docs
        except FileNotFoundError as e:
            logging.error(f"Configuration file not found: {self.config_file_path}")
            raise e
            
    
    @staticmethod
    def represent_ordereddict(dumper: Dumper, data: OrderedDict) -> Node:
        """
        Represent an ordered dictionary as a YAML mapping.

        Args:
            dumper (yaml.Dumper): The YAML dumper object.
            data (collections.OrderedDict): The ordered dictionary to represent.

        Returns:
            yaml.Node: The YAML node representing the ordered dictionary.
        """
        return dumper.represent_mapping('tag:yaml.org,2002:map', data.items())
    
    @abstractmethod
    def write_file(self, data: OrderedDict) -> None:
        """
        Write data to a file.
        Args:
            data (dict): The data to write to the file.
        """
        pass
    @abstractmethod
    def generate(self) -> None:
        """
        Generate a YAML file, the content depending on the child class.
        """
        pass