import unittest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from hexa_mlops.cli import main
from hexa_mlops.azureml.azure_inference_deployment_file_generator import AzOnlineDeploymentFileGenerator, AzBatchDeploymentFileGenerator
from hexa_mlops.azureml.azure_pipeline_file_generator import AzPipelineFileGenerator
from hexa_mlops.azureml.azure_training_batch_deployment_file_generator import AzTrainingBatchDeploymentFileGenerator
from hexa_mlops.azureml.env_file_generator import EnvFileGenerator
from hexa_mlops.azureml.conda_file_generator import CondaFileGenerator
from hexa_mlops.azureml.azure_datastore_register_generator import AzDatastoreRegisterFileGenerator
from hexa_mlops.azureml.azure_data_asset_register_generator import AzDataAssetRegisterFileGenerator

from hexa_mlops.acs.ml_deploy_helm_value_generator import MLDeploymentHelmValueGenerator

class TestCli(unittest.TestCase):
    @patch('sys.argv', ['hexa','az','online_deployment', 'generate', 'test_inputs/online_inference_config.yaml', 'test_outputs/online_inference_deployment.yaml'])
    @patch.object(AzOnlineDeploymentFileGenerator, 'generate')
    def test_az_online_deployment_cli(self, mock_generate):
        main()
        mock_generate.assert_called_once()

    @patch('sys.argv', ['hexa','az','batch_deployment', 'generate', 'test_inputs/batch_inference_config.yaml', 'test_outputs/batch_inference_deployment.yaml'])
    @patch.object(AzBatchDeploymentFileGenerator, 'generate')
    def test_az_batch_deployment_cli(self, mock_generate):
        main()
        mock_generate.assert_called_once()

    @patch('sys.argv', ['hexa','az', 'training_pipeline', 'generate', 'test_inputs/training_config.yaml', 'test_outputs/pipeline.yaml', 'test_inputs/training.yaml'])
    @patch.object(AzPipelineFileGenerator, 'generate')
    def test_az_training_pipeline_cli(self, mock_generate):
        main()
        mock_generate.assert_called_once()

    @patch('sys.argv', ['hexa','az', 'training_endpoint', 'generate', 'test_inputs/training_config.yaml', 'test_outputs/pipeline_no_value.yaml', 'test_inputs/training.yaml', 'test_outputs/inputs.yaml'])
    @patch.object(AzPipelineFileGenerator, 'generate')
    def test_az_training_endpoint_cli(self, mock_generate):
        main()
        mock_generate.assert_called_once()

    @patch('sys.argv', ['hexa','az', 'training_batch_deployment', 'generate', 'test_inputs/training_config.yaml', 'test_outputs/batch_training_deployment.yaml'])
    @patch.object(AzTrainingBatchDeploymentFileGenerator, 'generate')
    def test_az_training_batch_deployment_cli(self, mock_generate):
        main()
        mock_generate.assert_called_once()

    @patch('sys.argv', ['hexa','az', 'datastore_register', 'generate', 'test_inputs/datastore_config.yaml', 'test_outputs/datastore.yaml'])
    @patch.object(AzDatastoreRegisterFileGenerator, 'generate')
    def test_az_datastore_register_cli(self, mock_generate):
        main()
        mock_generate.assert_called_once()

    @patch('sys.argv', ['hexa','az', 'data_asset_register', 'generate', 'test_inputs/data_asset_config.yaml', 'test_outputs/data_asset.yaml'])
    @patch.object(AzDataAssetRegisterFileGenerator, 'generate')
    def test_az_data_asset_register_cli(self, mock_generate):
        main()
        mock_generate.assert_called_once()

    @patch('sys.argv', ['hexa','general', 'env', 'generate', 'test_inputs/training_config_2.yaml', 'test_outputs/training_workspace.env'])
    @patch.object(EnvFileGenerator, 'generate')
    def test_env_generation(self, mock_generate):
        main()
        mock_generate.assert_called_once()

    @patch('sys.argv', ['hexa','general', 'training_conda', 'generate', 'test_inputs/training_config.yaml', 'test_outputs/training_conda.yaml'])
    @patch.object(CondaFileGenerator, 'generate')
    def test_conda_generation(self, mock_generate):
        main()
        mock_generate.assert_called_once()

    @patch('sys.argv', ['hexa','general', 'inference_conda', 'generate', 'test_inputs/inference_config.yaml', 'test_outputs/inference_conda.yaml'])
    @patch.object(CondaFileGenerator, 'generate')
    def test_conda_generation(self, mock_generate):
        main()
        mock_generate.assert_called_once()
    
    @patch('sys.argv', ['hexa','helm', 'online_deployment_helm_value', 'generate', 'test_inputs/helm_common_config.yaml', 'test_outputs/generated_helm_values.yaml', 'tst', 'test_inputs/helm_model_config.yaml'])
    @patch.object(MLDeploymentHelmValueGenerator, 'generate')
    def test_helm_ml_deployment_generation(self, mock_generate):
        main()
        mock_generate.assert_called_once()

if __name__ == "__main__":
    unittest.main()