import unittest
import logging
import yaml
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from hexa_mlops.azureml.azure_datastore_register_generator import AzDatastoreRegisterFileGenerator


class TestDatastoreRegisterGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
    def setUp(self):
        self.maxDiff = None
        self.config_file = "test_inputs/datastore_config.yaml"
        self.deployment_file = "test_outputs/datastore.yaml"
        
    def test_generating(self):
        logging.info("Test generating deployment file")
        self.generator =  AzDatastoreRegisterFileGenerator(self.config_file, self.deployment_file)
        self.generator.generate()
        with open(self.deployment_file, 'r') as file:
            result = yaml.safe_load(file)
        expected = {'$schema': 'https://azuremlschemas.azureedge.net/latest/azureDataLakeGen2.schema.json',
                        'type': 'azure_data_lake_gen2',
                        'name': 'test_datastore',
                        'account_name': 'mlops_input_storage',
                        'filesystem': 'mlops_data_container',
                        'credentials':
                            {'tenant_id': 12345,
                            'client_id': 'dummy_client',
                            },
                        'protocol': 'https',
                        'description': 'register test storage as datalake gen2 with service principle',
                        'tags': 'data:test',
        }
        self.assertEqual(result, expected)
if __name__ == "__main__":
    unittest.main()