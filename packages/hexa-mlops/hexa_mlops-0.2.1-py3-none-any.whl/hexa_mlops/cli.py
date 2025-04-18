import argparse

from .azureml.azure_inference_deployment_file_generator import AzOnlineDeploymentFileGenerator, AzBatchDeploymentFileGenerator
from .azureml.azure_pipeline_file_generator import AzPipelineFileGenerator
from .azureml.azure_training_batch_deployment_file_generator import AzTrainingBatchDeploymentFileGenerator
from .azureml.env_file_generator import EnvFileGenerator
from .azureml.conda_file_generator import CondaFileGenerator
from .azureml.azure_datastore_register_generator import AzDatastoreRegisterFileGenerator
from .azureml.azure_data_asset_register_generator import AzDataAssetRegisterFileGenerator
from .acs.ml_deploy_helm_value_generator import MLDeploymentHelmValueGenerator

def add_generate_subparser(parser):
    subparser = parser.add_subparsers(dest='action', help='Choose action')
    generate_parser = subparser.add_parser('generate', help='Generate deployment file')
    generate_parser.add_argument('input', type=str, help='Path to the configuration file')
    generate_parser.add_argument('output', type=str, help='Path to the output file')
    return generate_parser

def main():
    parser = argparse.ArgumentParser(prog='hexa', description='File Generator CLI')

    subparsers = parser.add_subparsers(dest='engine_type', help='Choose a generator')
     # az sub-command
    az_parser = subparsers.add_parser('az', description='Azure Generator')
    az_subparsers = az_parser.add_subparsers(dest='file_type', help='Choose an Azure generator')
    # general sub-command
    general_parser = subparsers.add_parser('general', description='General Generator')
    general_subparsers = general_parser.add_subparsers(dest='file_type', help='Choose a general generator')

    # k8s sub-command
    helm_parser = subparsers.add_parser('helm', description='Helm Chart Generator')
    helm_subparsers = helm_parser.add_subparsers(dest='file_type', help='Choose a helm chart generator' )

    # AZ Online Inference Deployment Generator
    az_online_deployment_parser = az_subparsers.add_parser('online_deployment', help='Azure Online Inference Deployment file')
    add_generate_subparser(az_online_deployment_parser)

    # AZ Batch Inference Deployment Generator
    az_batch_deployment_parser = az_subparsers.add_parser('batch_deployment', help='Azure Batch Inference Deployment file')
    add_generate_subparser(az_batch_deployment_parser)

    # AZ Training Pipeline Generator
    az_training_pipeline_parser = az_subparsers.add_parser('training_pipeline', help='Azure Pipeline file with Global Inputs values')
    az_training_pipeline_subparser = add_generate_subparser(az_training_pipeline_parser)
    az_training_pipeline_subparser.add_argument('input_training_file', type=str, help='Path to the training file')

    # AZ Training Endpoint Generator
    az_training_endpoint_parser = az_subparsers.add_parser('training_endpoint', help='Azure Pipeline file without Global Inputs values for Training Batch Endpoint deployment')
    az_training_subparser = add_generate_subparser(az_training_endpoint_parser)
    az_training_subparser.add_argument('input_training_file', type=str, help='Path to the training file')
    az_training_subparser.add_argument('output_inputs_file', type=str, help='Path to the output file, in this case a file with all global inputs values')

    # AZ Training Batch Deployment Generator
    az_training_batch_parser = az_subparsers.add_parser('training_batch_deployment', help='Azure Training Batch Deployment file')
    add_generate_subparser(az_training_batch_parser)

    # AZ Datastore Register Generator
    az_datastore_register_parser = az_subparsers.add_parser('datastore_register', help='Azure Datastore Registry file')
    add_generate_subparser(az_datastore_register_parser)

    # AZ Data Asset Register Generator
    az_data_asset_register_parser = az_subparsers.add_parser('data_asset_register', help='Azure Data Asset Registry file')
    add_generate_subparser(az_data_asset_register_parser)


    # Env Generator
    env_parser = general_subparsers.add_parser('env', help='Environment file generator')
    add_generate_subparser(env_parser)

    # Conda Generator for Training phase
    training_conda_parser = general_subparsers.add_parser('training_conda', help='Conda environment file generator')
    add_generate_subparser(training_conda_parser)

    # Conda Generator for Inference phase
    inference_conda_parser = general_subparsers.add_parser('inference_conda', help='Conda environment file generator')
    add_generate_subparser(inference_conda_parser)

    # Helm Generator for ML Deployment helm value
    ml_deployment_helm_parser = helm_subparsers.add_parser('online_deployment_helm_value', help='Helm value for ML online deployment file generator')
    ml_deployment_helm_subparser = add_generate_subparser(ml_deployment_helm_parser)
    ml_deployment_helm_subparser.add_argument('phase', type=str, help='Deployment Phase')
    ml_deployment_helm_subparser.add_argument('model_config_file', type=str, help='Path to model configuration file')


    args = parser.parse_args()
    print(f"Parsed arguments: {args}")

    if args.engine_type == 'az'and args.action == "generate" and args.input and args.output:
        if args.file_type == 'online_deployment':
            generator = AzOnlineDeploymentFileGenerator(args.input, args.output)
        elif args.file_type == 'batch_deployment': #and args.file_type == 'generate' and args.input and args.output:
            generator = AzBatchDeploymentFileGenerator(args.input, args.output)
        elif args.file_type == 'training_pipeline' and args.input_training_file: #and args.file_type == 'generate' and args.input and args.output and args.input_training_file:
            generator = AzPipelineFileGenerator(args.input, args.output, args.input_training_file)
        elif args.file_type == 'training_endpoint' and args.input_training_file and args.output_inputs_file: #and args.file_type == 'generate' and args.input and args.output and args.input_training_file and args.output_inputs_file:
            generator = AzPipelineFileGenerator(args.input, args.output, args.input_training_file, args.output_inputs_file, pipeline_with_value=False)
        elif args.file_type == 'training_batch_deployment': # and args.file_type == 'generate' and args.input and args.output:
            generator = AzTrainingBatchDeploymentFileGenerator(args.input, args.output)
        elif args.file_type == 'datastore_register':
            generator = AzDatastoreRegisterFileGenerator(args.input, args.output)
        elif args.file_type == 'data_asset_register':
            generator = AzDataAssetRegisterFileGenerator(args.input, args.output)
        else:
            parser.print_help()
        generator.generate()
    elif args.engine_type == 'general' and args.action == "generate" and args.input and args.output:
        if args.file_type == 'env':
            generator = EnvFileGenerator(args.input, args.output)
        elif args.file_type == 'training_conda':
            generator = CondaFileGenerator(args.input, args.output, is_training_phase=True)
        elif args.file_type == 'inference_conda':
            generator = CondaFileGenerator(args.input, args.output, is_training_phase=False)
        else:
            parser.print_help()
        generator.generate()
    elif args.engine_type == 'helm' and args.action == "generate" and args.input and args.output:
        if args.file_type == 'online_deployment_helm_value':
            generator = MLDeploymentHelmValueGenerator(args.input, args.output, args.phase, args.model_config_file)
        else:
            parser.print_help()
        generator.generate()
    else:
        parser.print_help()


