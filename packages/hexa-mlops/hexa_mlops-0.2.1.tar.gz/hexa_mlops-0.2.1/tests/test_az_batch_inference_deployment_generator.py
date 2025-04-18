import unittest
import logging
import yaml
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from hexa_mlops.azureml.azure_inference_deployment_file_generator import AzBatchDeploymentFileGenerator


class TestOnlineDeploymentGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
    def setUp(self):
        self.maxDiff = None
        self.config_file = "test_inputs/batch_inference_config.yaml"
        self.deployment_file = "test_outputs/batch_inference_deployment.yaml"
        
    def test_generating(self):
        logging.info("Test generating deployment file")
        self.generator =  AzBatchDeploymentFileGenerator(self.config_file, self.deployment_file)
        self.generator.generate()
        with open(self.deployment_file, 'r') as file:
            result = yaml.safe_load(file)
        expected = {'$schema': 'https://azuremlschemas.azureedge.net/latest/batchDeployment.schema.json',
                        'name': 'my_dummy_online_deployment',
                        'endpoint_name': 'my_dummy_online_endpoint',
                        'type': 'model',
                        'model': 'azureml:my_dummy_model:1',
                        'code_configuration': {'code': 'TST/scr/score', 'scoring_script': 'score.py'},
                        'environment': 'azureml:h2o_env:3',
                        'compute': 'azureml:dummy',
                        'resources':{'instance_count': 1},
                        'environment_variables': None}
        self.assertEqual(result, expected)
if __name__ == "__main__":
    unittest.main()