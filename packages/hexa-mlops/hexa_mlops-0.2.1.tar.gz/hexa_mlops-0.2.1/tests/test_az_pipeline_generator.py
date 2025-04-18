import unittest
import logging
import yaml
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from hexa_mlops.azureml.azure_pipeline_file_generator import AzPipelineFileGenerator


class TestPipelineGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
    def setUp(self):
        self.maxDiff = None
        self.training_file = "test_inputs/training.yaml"
        self.config_file =  "test_inputs/training_config.yaml"
        self.pipeline_file = "test_outputs/pipeline.yaml"
        self.pipeline_no_value_file =  "test_outputs/pipeline_no_value.yaml"
        self.inputs_file_path = "test_outputs/inputs.yaml"
        self.generator_w_value = AzPipelineFileGenerator( self.config_file,self.pipeline_file, self.training_file)
        self.generator_no_value = AzPipelineFileGenerator(self.config_file,self.pipeline_no_value_file, self.training_file, input_file_path=self.inputs_file_path, pipeline_with_value=False)
    
    def test_generating_pipeline_file_w_value(self):
        logging.info("Test generating pipeline file with value ")
        self.generator_w_value.generate()
        with open(self.pipeline_file , 'r') as file:
            result = yaml.safe_load(file)
        self.assertEqual(result["display_name"], "Primitive Training")
        self.assertEqual(result["experiment_name"], "ahp_mlops")
        self.assertEqual(
            result["jobs"]["prep"],
            {
                'code': '../src/prep/',
                'command': 'python prep.py --data_folder ${{inputs.data_folder}} --some_number ${{inputs.some_number}} --some_string ${{inputs.some_string}} --prep_data ${{outputs.prep_data}}',
                'compute': 'azureml:demo-compute',
                'environment': 'azureml:h2o_env:3',
                'inputs': {
                    'data_folder': 
                        {"path": "azureml://datastores/workspaceblobstore/paths/UI/2024-10-06_150541_UTC/office_data/paris", "type": "uri_folder"},
                    'some_number': 3,
                    'some_string':'paris'
            },
                'outputs': {
                        'prep_data': {'mode': 'upload', 'path': 'azureml://datastores/workspaceblobstore/paths/dynamic_params/office/prep_data','type': 'uri_folder'}
            },
                'type': 'command'
                    }
        )
        self.assertEqual(
            result["jobs"]["transform"],
            {
                'code': '../src/transform/',
                'command': 'python transform.py --clean_data ${{inputs.clean_data}} --transformed_data ${{outputs.transformed_data}}',
                'compute': 'azureml:demo-compute',
                'environment': 'azureml:h2o_env:3',
                'inputs': {'clean_data': '${{parent.jobs.prep.outputs.prep_data}}'},
                'outputs': {'transformed_data': None},
                'type': 'command'
            }
        )
        self.assertEqual(
            result["jobs"]["train"],
            {
                'code': '../src/train/',
                'command': 'python train.py --training_data ${{inputs.training_data}} --model_output ${{outputs.model_output}} --test_data ${{outputs.test_data}}',
                'compute': 'azureml:demo-compute',
                'environment': 'azureml:h2o_env:3',
                'inputs': {
                    'training_data': '${{parent.jobs.transform.outputs.transformed_data}}',
                    },
                'outputs': {
                        'model_output': {'mode': 'upload', 'path': 'azureml://datastores/workspaceblobstore/paths/dynamic_params/office/train_output', 'type': 'uri_folder'},
                        'test_data': None
                },
                'type': 'command'
            }
        )
        self.assertEqual(
            result["jobs"]["predict"],
            {
                'code': '../src/predict/',
                'command': 'python predict.py --model_input ${{inputs.model_input}} --test_data ${{inputs.test_data}} --predictions ${{outputs.predictions}}',
                'compute': 'azureml:demo-compute',
                'environment': 'azureml:h2o_env:3',
                'inputs': {
                    'model_input': '${{parent.jobs.train.outputs.model_output}}',
                    'test_data': '${{parent.jobs.train.outputs.test_data}}'
                },
                'outputs': {'predictions': None},
                'type': 'command'
            }
        )

    def test_generating_pipeline_file_wo_value(self):
        logging.info("Test generating pipeline file without value")
        self.generator_no_value.generate()
        with open(self.pipeline_no_value_file , 'r') as file:
            result = yaml.safe_load(file)

        self.assertEqual(result["display_name"], "Primitive Training")
        self.assertEqual(result["experiment_name"], "ahp_mlops")
        self.assertEqual(
            result["jobs"]["prep"]["inputs"],
            {
                    'data_folder': None,
                    'some_number': None,
                    'some_string': None
            }
        )
        self.assertEqual(
            result["jobs"]["prep"]["outputs"],
            {
                'prep_data': None
            }
        )
        self.assertEqual(
            result["jobs"]["train"]["outputs"]["model_output"],
            None
        )
        
    def test_inputs_file_generation(self):
        self.generator_no_value.generate()
        logging.info("Test generating inputs file ")

        with open(self.inputs_file_path , 'r') as file:
            result = yaml.safe_load(file)

        self.assertEqual(
            result["inputs"]["data_folder"],
            {
                "path": "azureml://datastores/workspaceblobstore/paths/UI/2024-10-06_150541_UTC/office_data/paris",
                "type": "uri_folder"
            }
        )
        self.assertEqual(result["inputs"]["some_number"], 3)
        self.assertEqual(result["inputs"]["some_string"], "paris")
        self.assertEqual(result["outputs"]["prep_data"], {
            "mode": "upload",
            "path": "azureml://datastores/workspaceblobstore/paths/dynamic_params/office/prep_data",
            "type": "uri_folder"
        })
        self.assertEqual(result["outputs"]["model_output"], {
            "mode":"upload",
            "path": "azureml://datastores/workspaceblobstore/paths/dynamic_params/office/train_output",
            "type": "uri_folder",
        })
if __name__ == "__main__":
    unittest.main()