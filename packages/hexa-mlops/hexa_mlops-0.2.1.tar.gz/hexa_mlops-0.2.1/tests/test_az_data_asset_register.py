import unittest
import logging
import yaml
import os
from hexa_mlops.azureml.azure_data_asset_register_generator import AzDataAssetRegisterFileGenerator

class TestDataAssetRegisterGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)

    def setUp(self):
        self.maxDiff = None
        self.config_file = "test_inputs/data_asset_config.yaml"
        self.output_file = "test_outputs/data_asset.yaml"

    def test_generating(self):
        logging.info("Test generating data asset file")
        generator = AzDataAssetRegisterFileGenerator(self.config_file, self.output_file)
        generator.generate()

        with open(self.output_file, 'r') as file:
            result = yaml.safe_load(file)

        expected = {
            '$schema': 'https://azuremlschemas.azureedge.net/latest/data.schema.json',
            'type': 'uri_file',
            'name': 'test_data_asset',
            'description': 'Register test dataset as a data asset',
            'tags': 'dataset:test',
            'path': 'azureml://datastores/test_datastore/paths/mlops_data/my_data.csv',
            'version': 1
        }

        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
