# HexaMLOPS CLI


The  HexaMLOps command line tool allows data science teams to generate deployment files needed for platforms like Azure, Kubeflow, and more (coming soon).

By using our abstraction files, data science teams can easily generate deployment files that are compatible with the CLI or SDK of various Machine Learning (ML) platforms, enabling seamless operations on those platforms.


## Installation

```bash
# Create a VENV
python3 -m venv VENV
. ./VENV/bin/activate
```

```bash
pip install hexa-mlops --upgrade # upgrade to last version
```



## Usage

```bash
$ hexa [engine_type] [ file_type ] [ command ] {parameters}
```

## Get Started

Please refer to the [User guide](docs/USERGUIDE.md) for in-depth instructions.

For usage and help content, pass in the `-h` parameter, for example:

```bash
$ hexa az -h
$ hexa general -h
```

## Testing

```bash
python -m build && pip install . && cd tests && python -m unittest
```
## Inputs
Primary input files are `configuration.yaml` and `training.yaml`

`configuration.yaml` example

```bash
# General fields
resource_group: xxx
workspace_name: xxx
location: xxx
experiment_name: hexa_mlops
tags: created_by:hexa_mlops

# Fields to generate files for training
training:  
  compute_name: hexa_compute
  max_instances: 2

  environment_name: hexa_env
  environment_version: 1
  environment_dependencies:
    - python=3.8
    - numpy=1.21.2
    - pip=21.2.4
    - scikit-learn=0.24.2
    - pip:
        - inference-schema[numpy-support]==1.3.0
        - xlrd==2.0.1
        - mlflow==2.6.0
        - azureml-mlflow==1.42.0
    source_code_path: ./src
# Fields to generate files for inference
inference:
    compute_name: inference_compute
    max_instances: 3
    environment_name: inference_env
    environment_version: 2
    endpoint_name: hexa_ml_endpoint
    deployment_name: hexa_ml_blue_deployment
```

`training.yaml` example
```bash
# Jobs within your training pipeline
run_name: training_example
steps:
  - name: download_data
    inputs:
      - data_config: 
          type: uri_file
          path: ./src/download_data/config_yaml
     
    outputs:
      - data_folder: 

  - name : data_prep
    inputs:
      - json_folder: download_data.outputs.data_folder
    outputs:
      - output_folder: 
          type: uri_folder
          mode: upload
 
```
## Outputs

Command to generate files which are used with Azure Machine Learning CLI for ML operation on Azure ML platform, for example:


- Training a model with `pipeline.yaml`
```bash
$ hexa az training_pipeline generate config.yaml pipeline.yaml training.yaml
```

- Deploy a model as an online endpoint with `online_deployment.yaml`
```bash
$ hexa az online_deployment generate config.yaml online_deployment.yaml
```
For other supported file types, check `-h` command