import yaml
import logging
from ..base.constants import *
from ..base.file_generator import FileGenerator
from collections import OrderedDict
yaml.add_representer(OrderedDict, FileGenerator.represent_ordereddict)

class AzTrainingBatchDeploymentFileGenerator(FileGenerator):
    """
    A class to generate the Azure Training Batch Deployment Endpoint file

    Attributes:
        config_file_path (str): The path to the config file
        output_file_path (str): The path to the generated file

    Methods:
        generate(): Generate Azure Training Batch Deployment Endpoint file
    """

    def __init__(self,config_file_path: str, output_file_path: str):
        super().__init__(config_file_path, output_file_path)

    def write_file(self, data: OrderedDict ) -> None:
        with open(self.output_file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
            logging.info(f"Training Batch Endpoint Deployment file generated at {self.output_file_path}")
    
    def generate(self) -> None:
        """
        Generate Azure Training Batch Deployment Endpoint file
        Default compute name is equivalent to compute name in the training phase
        Component is the default name of pipeline without value file
        Returns:
            A Azure Training Batch Deployment Endpoint file to deploy an endpoint will be generated
        """
        try:
            # Load the data from the YAML file
            data = self.get_config()
            try:
                # Fetch compute name under the training phase
                default_compute_name = data.get(TRAINING_PHASE, EMPTY_CONSTANT).get(COMPUTE_NAME, EMPTY_CONSTANT)
            except Exception as e:
                logging.error(f"Cannot retrieve compute name: {e}")

            # Initialize the content dictionary, this includes all the configurations will be written to the .env file
            deployment_stream = OrderedDict([
                    ('$schema',BATCH_PIPELINE_COMPONENT_SCHEMA),
                    ('type', "pipeline"),
                    ("component", PIPELINE_NO_VALUE),
                    ("settings", {
                        "continue_on_step_failure": False,
                        "default_compute": default_compute_name,
                                 }),
                ])
            
            self.write_file(deployment_stream)

        except Exception as e:
            logging.error(f"Generating training batch deployment file generator, an error occurred with: {e}")            

    
