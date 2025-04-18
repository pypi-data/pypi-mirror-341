import os
import yaml
import unittest
import logging
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from hexa_mlops.acs.ml_deploy_helm_value_generator import MLDeploymentHelmValueGenerator

class TestMLDeploymentHelmValueGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
    def setUp(self):
        self.maxDiff = None
        self.config_file = os.path.join(os.path.dirname(__file__), "test_inputs", "helm_common_config.yaml")
        self.model_config_file = os.path.join(os.path.dirname(__file__), "test_inputs", "helm_model_config.yaml")
        self.output_file = os.path.join(os.path.dirname(__file__), "test_outputs", "generated_helm_values.yaml")
        self.expected_output_file = os.path.join(os.path.dirname(__file__), "test_outputs", "expected_helm_values.yaml")
        self.phase = "tst"
        
    def tearDown(self):
        # Cleanup the generated file after the test
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_generating(self):
        logging.info("Test generating deployment file")

        # Ensure input files exist
        self.assertTrue(os.path.exists(self.config_file), f"Config file not found: {self.config_file}")
        self.assertTrue(os.path.exists(self.model_config_file), f"Model config file not found: {self.model_config_file}")
        self.assertTrue(os.path.exists(self.expected_output_file), f"Expected output file not found: {self.expected_output_file}")

        # Generate the YAML file
        self.generator =  MLDeploymentHelmValueGenerator(self.config_file, self.output_file , self.phase, self.model_config_file)
        self.generator.generate()
        
        # Load file
        with open(self.expected_output_file, "r") as f:
            expected_data = yaml.safe_load(f)

        with open(self.output_file, "r") as f:
            generated_data = yaml.safe_load(f)

        self.assertEqual(expected_data, generated_data)
if __name__ == "__main__":
    unittest.main()
