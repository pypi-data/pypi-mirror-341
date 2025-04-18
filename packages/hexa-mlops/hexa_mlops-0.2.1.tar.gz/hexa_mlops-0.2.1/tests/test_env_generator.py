import unittest
import logging
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from hexa_mlops.azureml.env_file_generator import EnvFileGenerator


class TestAzureWorkspaceGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
    def setUp(self):
        self.maxDiff = None
        ''' Set up test samples under different layouts
        '''
        self.training_phase = "training"
        self.inference_phase = "inference"
        self.training_phase_configs = {
            "compute_name": "ahp_training",
            "min_instances": "1",
            "max_instances": "10",
            "environment_version": "3",
        }
        self.inference_phase_configs = {
            "compute_name": "ahp_inference",
            "max_instances": "3",
            "idle_seconds_before_scale_down": "100",
            "environment_version": "10",
        }
        self.output_training_file = "test_outputs/training_workspace.env"
        self.output_inference_file = "test_outputs/inference_workspace.env"
        self.output_training_inference_file = "test_outputs/training_inference_config.env"
        self.training_workspace_file = "test_inputs/training_config_2.yaml"
        self.inference_workspace_file = "test_inputs/inference_config.yaml"
        self.training_inference_workspace_file = "test_inputs/training_inference_config.yaml"
        
    def test_training_phase(self):
        logging.info("Testing method to generate config if training phase exists")
        result = EnvFileGenerator.generate_phase_resources(self.training_phase, self.training_phase_configs, {}) 
        expected = {
            "training_compute_name": "ahp_training",
            "training_min_instances": "1",
            "training_max_instances": "10",
            "training_compute_type": "amlcompute",
            "training_vm_size": "STANDARD_D13_V2",
            "training_idle_seconds_before_scale_down": "120",
            "training_tier": "dedicated",
            "training_subnet": "",
            "training_compute_user_assigned_identity": "",
            "training_environment_name": None,
            "training_environment_version": "3",
            "training_environment_image": "mcr.microsoft.com/azureml/intelmpi2018.3-ubuntu16.04:20200821.v1",
            "training_endpoint_name": None,
            "training_deployment_name": None,
        }
        self.assertEqual(expected, result)
    
    
    def test_inference_phase(self):
        logging.info("Testing method to generate config if inference phase exists")
        result = EnvFileGenerator.generate_phase_resources(self.inference_phase, self.inference_phase_configs, {})
        expected = {
            "inference_compute_name": "ahp_inference",
            "inference_min_instances": "0",
            "inference_max_instances": "3",
            "inference_compute_type": "amlcompute",
            "inference_vm_size": "STANDARD_D13_V2",
            "inference_idle_seconds_before_scale_down": "100",
            "inference_tier": "dedicated",
            "inference_subnet": "",
            "inference_compute_user_assigned_identity": "",
            "inference_environment_name": None,
            "inference_environment_version": "10",
            "inference_environment_image": "mcr.microsoft.com/azureml/intelmpi2018.3-ubuntu16.04:20200821.v1",
            "inference_endpoint_name": None,
            "inference_deployment_name": None,

        }
        self.assertEqual(expected, result)

    def test_generate_training(self):
        logging.info("Testing method to generate .env file for training phase only")
        self.training_generator = EnvFileGenerator(self.training_workspace_file, self.output_training_file)
        self.training_generator.generate()
        load_dotenv(self.output_training_file)
        result = {
            "RESOURCE_GROUP": os.getenv("RESOURCE_GROUP"),
            "WORKSPACE_NAME": os.getenv("WORKSPACE_NAME"),
            "LOCATION": os.getenv("LOCATION"),
            "EXPERIMENT_NAME": os.getenv("EXPERIMENT_NAME"),
            "TAGS": os.getenv("TAGS"),
            "DESCRIPTION": os.getenv("DESCRIPTION"),
            "MODEL_NAME": os.getenv("MODEL_NAME"),
            "MODEL_VERSION": os.getenv("MODEL_VERSION"),
            "MODEL_TYPE": os.getenv("MODEL_TYPE"),
            "MODEL_PATH": os.getenv("MODEL_PATH"),
            "TRAINING_COMPUTE_NAME": os.getenv("TRAINING_COMPUTE_NAME"),
            "TRAINING_COMPUTE_USER_ASSIGNED_IDENTITY": os.getenv("TRAINING_COMPUTE_USER_ASSIGNED_IDENTITY"),
            "TRAINING_MIN_INSTANCES": os.getenv("TRAINING_MIN_INSTANCES"),
            "TRAINING_MAX_INSTANCES": os.getenv("TRAINING_MAX_INSTANCES"),
            "TRAINING_COMPUTE_TYPE": os.getenv("TRAINING_COMPUTE_TYPE"),
            "TRAINING_VM_SIZE": os.getenv("TRAINING_VM_SIZE"),
            "TRAINING_IDLE_SECONDS_BEFORE_SCALE_DOWN": os.getenv("TRAINING_IDLE_SECONDS_BEFORE_SCALE_DOWN"),
            "TRAINING_TIER": os.getenv("TRAINING_TIER"),
            "TRAINING_SUBNET": os.getenv("TRAINING_SUBNET"),
            "TRAINING_ENVIRONMENT_NAME": os.getenv("TRAINING_ENVIRONMENT_NAME"),
            "TRAINING_ENVIRONMENT_VERSION": os.getenv("TRAINING_ENVIRONMENT_VERSION"),
            "TRAINING_ENVIRONMENT_IMAGE": os.getenv("TRAINING_ENVIRONMENT_IMAGE"),
        }
        expected = {
            "RESOURCE_GROUP": "hexa_rg",
            "WORKSPACE_NAME": "hexa_ws",
            "LOCATION": "westeurope",
            "EXPERIMENT_NAME": "ahp_mlops",
            "TAGS": {"finops": "ahp_mlops"},
            "DESCRIPTION": '',
            "MODEL_NAME": "demo_model",
            "MODEL_VERSION": "1",
            "MODEL_TYPE": '',
            "MODEL_PATH": './src/mlops_framework/azureml/test/model.pkl',
            "TRAINING_COMPUTE_USER_ASSIGNED_IDENTITY": "user_id",
            "TRAINING_COMPUTE_NAME": "ahp_mlops",
            "TRAINING_MIN_INSTANCES": "0",
            "TRAINING_MAX_INSTANCES": "8",
            "TRAINING_COMPUTE_TYPE": "amlcompute",
            "TRAINING_VM_SIZE": "STANDARD_D13_V2",
            "TRAINING_IDLE_SECONDS_BEFORE_SCALE_DOWN": "120",
            "TRAINING_TIER": "dedicated",
            "TRAINING_SUBNET": "",
            "TRAINING_ENVIRONMENT_NAME": "ahp_mlops",
            "TRAINING_ENVIRONMENT_VERSION": "3",
            "TRAINING_ENVIRONMENT_IMAGE": "mcr.microsoft.com/azureml/intelmpi2018.3-ubuntu16.04:20200821.v1",

        }
        self.assertTrue(result, expected)

    def test_generate_inference(self):
        logging.info("Testing method to generate .env file for inference phase only")
        self.inference_generator = EnvFileGenerator(self.inference_workspace_file, self.output_inference_file)
        self.inference_generator.generate()
        load_dotenv(self.output_inference_file)
        result = {
            "RESOURCE_GROUP": os.getenv("RESOURCE_GROUP"),
            "WORKSPACE_NAME": os.getenv("WORKSPACE_NAME"),
            "LOCATION": os.getenv("LOCATION"),
            "EXPERIMENT_NAME": os.getenv("EXPERIMENT_NAME"),
            "TAGS": os.getenv("TAGS"),
            "INFERENCE_COMPUTE_NAME": os.getenv("INFERENCE_COMPUTE_NAME"),
            "INFERENCE_MIN_INSTANCES": os.getenv("INFERENCE_MIN_INSTANCES"),
            "INFERENCE_MAX_INSTANCES": os.getenv("INFERENCE_MAX_INSTANCES"),
            "INFERENCE_COMPUTE_TYPE": os.getenv("INFERENCE_COMPUTE_TYPE"),
            "INFERENCE_VM_SIZE": os.getenv("INFERENCE_VM_SIZE"),
            "INFERENCE_COMPUTE_USER_ASSIGNED_IDENTITY": os.getenv("INFERENCE_COMPUTE_USER_ASSIGNED_IDENTITY"),
            "INFERENCE_IDLE_SECONDS_BEFORE_SCALE_DOWN": os.getenv("INFERENCE_IDLE_SECONDS_BEFORE_SCALE_DOWN"),
            "INFERENCE_TIER": os.getenv("INFERENCE_TIER"),
            "INFERENCE_SUBNET": os.getenv("INFERENCE_SUBNET"),
            "INFERENCE_ENVIRONMENT_NAME": os.getenv("INFERENCE_ENVIRONMENT_NAME"),
            "INFERENCE_ENVIRONMENT_VERSION": os.getenv("INFERENCE_ENVIRONMENT_VERSION"),
            "INFERENCE_ENVIRONMENT_IMAGE": os.getenv("INFERENCE_ENVIRONMENT_IMAGE"),
        }
        expected = {
            "RESOURCE_GROUP": "hexa_rg",
            "WORKSPACE_NAME": "hexa_ws",
            "LOCATION": "westeurope",
            "EXPERIMENT_NAME": "ahp_mlops",
            "TAGS": "ahp_mlops",
            "INFERENCE_COMPUTE_NAME": "cluster_ahp",
            "INFERENCE_MIN_INSTANCES": "0",
            "INFERENCE_MAX_INSTANCES": "8",
            "INFERENCE_COMPUTE_TYPE": "amlcompute",
            "INFERENCE_VM_SIZE": "STANDARD_D13_V2",
            "INFERENCE_COMPUTE_USER_ASSIGNED_IDENTITY": "user_id",
            "INFERENCE_IDLE_SECONDS_BEFORE_SCALE_DOWN": "120",
            "INFERENCE_TIER": "dedicated",
            "INFERENCE_SUBNET": "",
            "INFERENCE_ENVIRONMENT_NAME": "h2o_env",
            "INFERENCE_ENVIRONMENT_VERSION": "1",
            "INFERENCE_ENVIRONMENT_IMAGE": "mcr.microsoft.com/azureml/intelmpi2018.3-ubuntu16.04:20200821.v1",

        }
        self.assertTrue(result, expected)
    def test_generate_training_inference(self):
        logging.info("Testing method to generate .env file for both training and inference phases")
        self.training_inference_generator = EnvFileGenerator(self.training_inference_workspace_file, self.output_training_inference_file)
        self.training_inference_generator.generate()
        load_dotenv(self.output_training_inference_file)
        result = {
            "RESOURCE_GROUP": os.getenv("RESOURCE_GROUP"),
            "WORKSPACE_NAME": os.getenv("WORKSPACE_NAME"),
            "LOCATION": os.getenv("LOCATION"),
            "EXPERIMENT_NAME": os.getenv("EXPERIMENT_NAME"),
            "TAGS": os.getenv("TAGS"),
            "TRAINING_COMPUTE_NAME": os.getenv("TRAINING_COMPUTE_NAME"),
            "TRAINING_MIN_INSTANCES": os.getenv("TRAINING_MIN_INSTANCES"),
            "TRAINING_MAX_INSTANCES": os.getenv("TRAINING_MAX_INSTANCES"),
            "TRAINING_COMPUTE_TYPE": os.getenv("TRAINING_COMPUTE_TYPE"),
            "TRAINING_VM_SIZE": os.getenv("TRAINING_VM_SIZE"),
            "TRAINING_IDLE_SECONDS_BEFORE_SCALE_DOWN": os.getenv("TRAINING_IDLE_SECONDS_BEFORE_SCALE_DOWN"),
            "TRAINING_TIER": os.getenv("TRAINING_TIER"),
            "TRAINING_SUBNET": os.getenv("TRAINING_SUBNET"),
            "TRAINING_ENVIRONMENT_NAME": os.getenv("TRAINING_ENVIRONMENT_NAME"),
            "TRAINING_ENVIRONMENT_VERSION": os.getenv("TRAINING_ENVIRONMENT_VERSION"),
            "TRAINING_ENVIRONMENT_IMAGE": os.getenv("TRAINING_ENVIRONMENT_IMAGE"),
            "TRAINING_COMPUTE_USER_ASSIGNED_IDENTITY": os.getenv("TRAINING_COMPUTE_USER_ASSIGNED_IDENTITY"),
            "INFERENCE_COMPUTE_NAME": os.getenv("INFERENCE_COMPUTE_NAME"),
            "INFERENCE_MIN_INSTANCES": os.getenv("INFERENCE_MIN_INSTANCES"),
            "INFERENCE_MAX_INSTANCES": os.getenv("INFERENCE_MAX_INSTANCES"),
            "INFERENCE_COMPUTE_TYPE": os.getenv("INFERENCE_COMPUTE_TYPE"),
            "INFERENCE_VM_SIZE": os.getenv("INFERENCE_VM_SIZE"),
            "INFERENCE_IDLE_SECONDS_BEFORE_SCALE_DOWN": os.getenv("INFERENCE_IDLE_SECONDS_BEFORE_SCALE_DOWN"),
            "INFERENCE_TIER": os.getenv("INFERENCE_TIER"),
            "INFERENCE_SUBNET": os.getenv("INFERENCE_SUBNET"),
            "INFERENCE_ENVIRONMENT_NAME": os.getenv("INFERENCE_ENVIRONMENT_NAME"),
            "INFERENCE_ENVIRONMENT_VERSION": os.getenv("INFERENCE_ENVIRONMENT_VERSION"),
            "INFERENCE_ENVIRONMENT_IMAGE": os.getenv("INFERENCE_ENVIRONMENT_IMAGE"),
            "INFERENCE_COMPUTE_USER_ASSIGNED_IDENTITY": os.getenv("INFERENCE_COMPUTE_USER_ASSIGNED_IDENTITY")

        }
        expected = {
            "RESOURCE_GROUP": "hexa_rg",
            "WORKSPACE_NAME": "hexa_ws",
            "LOCATION": "westeurope",
            "EXPERIMENT_NAME": "ahp_mlops",
            "TAGS": "ahp_mlops",
            "TRAINING_COMPUTE_NAME": "ahp_mlops",
            "TRAINING_MIN_INSTANCES": "0",
            "TRAINING_MAX_INSTANCES": "8",
            "TRAINING_COMPUTE_TYPE": "amlcompute",
            "TRAINING_VM_SIZE": "STANDARD_D13_V2",
            "TRAINING_IDLE_SECONDS_BEFORE_SCALE_DOWN": "120",
            "TRAINING_TIER": "dedicated",
            "TRAINING_SUBNET": "",
            "TRAINING_ENVIRONMENT_NAME": "ahp_mlops",
            "TRAINING_ENVIRONMENT_VERSION": "3",
            "TRAINING_ENVIRONMENT_IMAGE": "mcr.microsoft.com/azureml/intelmpi2018.3-ubuntu16.04:20200821.v1",
            "TRAINING_COMPUTE_USER_ASSIGNED_IDENTITY": "",
            "INFERENCE_COMPUTE_NAME": "cluster_drift14",
            "INFERENCE_MIN_INSTANCES": "0",
            "INFERENCE_MAX_INSTANCES": "2",
            "INFERENCE_COMPUTE_TYPE": "amlcompute",
            "INFERENCE_VM_SIZE": "STANDARD_D13_V2",
            "INFERENCE_IDLE_SECONDS_BEFORE_SCALE_DOWN": "120",
            "INFERENCE_TIER": "dedicated",
            "INFERENCE_SUBNET": "",
            "INFERENCE_ENVIRONMENT_NAME": "h2o_env",
            "INFERENCE_ENVIRONMENT_VERSION": "latest",
            "INFERENCE_ENVIRONMENT_IMAGE": "mcr.microsoft.com/azureml/intelmpi2018.3-ubuntu16.04:20200821.v1",
            "INFERENCE_COMPUTE_USER_ASSIGNED_IDENTITY":""
        }
        self.assertTrue(result, expected)

if __name__ == "__main__":
    unittest.main()