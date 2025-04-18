import unittest
import logging
import yaml
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from hexa_mlops.azureml.conda_file_generator import CondaFileGenerator

class TestCondaGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
    def setUp(self):
        self.maxDiff = None
        self.training_config_file =  "test_inputs/training_config.yaml"
        self.inference_config_file ="test_inputs/inference_config.yaml"
        self.training_conda_file = "test_outputs/training_conda.yaml"
        self.inference_conda_file = "test_outputs/inference_conda.yaml"
    
    def test_generating_training(self):
        logging.info("Test generating conda file for training phase")
        self.generator =  CondaFileGenerator(self.training_config_file, self.training_conda_file, is_training_phase=True)
        self.generator.generate()
        with open(self.training_conda_file, 'r') as file:
            result = yaml.safe_load(file)
        expected = {
            "name": "h2o_env",
            "channels": ["conda-forge", "anaconda"],
            "dependencies" : [
                "python=3.8",
                "numpy=1.21.2",
                "pip=21.2.4",
                "scikit-learn=0.24.2",
                "scipy=1.7.1",
                "pandas>=1.1,<1.2",
                "openjdk",
                "aiohttp",
                "aiofiles",
                {"pip": [
                    "inference-schema[numpy-support]==1.3.0",
                    "xlrd==2.0.1",
                    "mlflow==2.6.0",
                    "azureml-mlflow==1.42.0",
                    "neobase",
                    "h2o"
            ]
                }
            ]
        }
        self.assertEqual(result, expected)
    def test_generating_inference(self):
        logging.info("Test generating conda file for inference phase")
        self.generator =  CondaFileGenerator(self.inference_config_file, self.inference_conda_file, is_training_phase=False)
        self.generator.generate()
        with open(self.inference_conda_file, 'r') as file:
            result = yaml.safe_load(file)
        expected = {
            "name": "h2o_env",
            "channels": ["conda-forge", "anaconda"],
            "dependencies" : [
                "python=3.8",
                "numpy=1.21.2",
                "pip=21.2.4",
                "scikit-learn=0.24.2",
                "scipy=1.7.1",
                "pandas>=1.1,<1.2",
                "openjdk",
                "aiohttp",
                "aiofiles",
                {"pip": [
                    "inference-schema[numpy-support]==1.3.0",
                    "xlrd==2.0.1",
                    "mlflow==2.6.0",
                    "azureml-mlflow==1.42.0",
                    "neobase",
                    "h2o",
                    "matplotlib",
                    "tqdm",
                    "azure-storage-blob",
                    "azure-identity",
            ]
                }
            ]
        }
        self.assertEqual(result, expected)
if __name__ == "__main__":
    unittest.main()