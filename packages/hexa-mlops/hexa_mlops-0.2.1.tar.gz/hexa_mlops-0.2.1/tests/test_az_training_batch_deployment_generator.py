import unittest
import logging
import yaml
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from hexa_mlops.azureml.azure_training_batch_deployment_file_generator import AzTrainingBatchDeploymentFileGenerator
from hexa_mlops.base.constants import PIPELINE_NO_VALUE


class TestTraingBatchDeploymentGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
    def setUp(self):
        self.maxDiff = None
        self.config_file =  "test_inputs/training_config.yaml"
        self.deployment_file = "test_outputs/batch_training_deployment.yaml"
    
    def test_generating(self):
        logging.info("Test generating deployment file")
        self.generator =  AzTrainingBatchDeploymentFileGenerator(self.config_file, self.deployment_file)
        self.generator.generate()
        with open(self.deployment_file, 'r') as file:
            result = yaml.safe_load(file)
        expected = {
                    "$schema": "https://azuremlschemas.azureedge.net/latest/pipelineComponentBatchDeployment.schema.json",
                    "type": "pipeline",
                    "component": PIPELINE_NO_VALUE,
                    "settings": {
                        "continue_on_step_failure": False,
                        "default_compute": "demo-compute",
                    }
        }
        self.assertEqual(result, expected)
if __name__ == "__main__":
    unittest.main()