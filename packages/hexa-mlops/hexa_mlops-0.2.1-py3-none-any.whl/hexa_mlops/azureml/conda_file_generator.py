import yaml
import logging
from ..base.constants import *
from ..base.file_generator import FileGenerator
from collections import OrderedDict
yaml.add_representer(OrderedDict, FileGenerator.represent_ordereddict)

class CondaFileGenerator(FileGenerator):
    """
    A class to generate a Conda environment file

    Attributes:
        config_file_path (str): The path to the config file
        output_file_path (str): The path to the generated file

    Methods:
        generate(): Generate a Conda environment file
    """

    def __init__(self,config_file_path: str, output_file_path: str, is_training_phase: bool):
        super().__init__(config_file_path, output_file_path)
        self.is_training_phase = is_training_phase

    def write_file(self, data: OrderedDict ) -> None:
        """
        Write environment dependencies to a conda.yaml file
        Args:
            data (dict): The data to write to the file.
        """
        with open(self.output_file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
            logging.info(f"Conda environment file generated at {self.output_file_path}")
    
    def validate_generate_environment_dependencies(self, data: dict, phase: str) -> None:
        """
        Generate the environment dependencies for the training or inference phase
        The configurations for the phase declared in the yaml file will be used, if not found, default values will be used.
        Args:
            data: The configurations for the phase declared in the yaml file
            phase (str): The phase name
        """
        dependencies = data.get(phase, EMPTY_CONSTANT).get(ENVIRONMENT_DEPENDENCIES, EMPTY_CONSTANT)
        name = data.get(phase, EMPTY_CONSTANT).get(ENVIRONMENT_NAME, EMPTY_CONSTANT)
        if not dependencies:
            raise ValueError(f"Environment dependencies not found in {phase} phase")
        if not name:
            raise ValueError(f"Environment name not found in {phase} phase")
        content = OrderedDict([
            ("name", name),
            ("channels", ["conda-forge", "anaconda"]),
            ("dependencies", dependencies)
        ])
        self.write_file(content)

    def generate(self) -> None:
        """
        Generate Azure Training Batch Deployment Endpoint file
        Default compute name is equivalent to compute name in the training phase
        Component is the default name of pipeline without value file
        Returns:
            A Azure Training Batch Deployment Endpoint file to deploy an endpoint will be generated
        """
        try:
            data = self.get_config()
        
            if self.is_training_phase:
                self.validate_generate_environment_dependencies(data, TRAINING_PHASE)
            else:
                self.validate_generate_environment_dependencies(data, INFERENCE_PHASE)
        except Exception as e:
            logging.error(f"Generating Conda file, an error occurred with: {e}")       