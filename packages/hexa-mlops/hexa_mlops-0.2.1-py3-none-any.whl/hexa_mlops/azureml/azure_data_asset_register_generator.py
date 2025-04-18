import yaml
import logging
import os
from collections import OrderedDict
from ..base.file_generator import FileGenerator

yaml.add_representer(OrderedDict, FileGenerator.represent_ordereddict)

class AzDataAssetRegisterFileGenerator(FileGenerator):
    """
    A class to generate the Azure ML Data Asset Register file
    """

    def __init__(self, config_file_path: str, output_file_path: str):
        super().__init__(config_file_path, output_file_path)

    @staticmethod
    def check_required_values(data: dict) -> None:
        """
        Ensure required fields are present in the configuration data
        """
        required_fields = [
            DATA_ASSET_NAME,
            TYPE,
            PATH,
            VERSION
         ]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Missing or empty required value: {field}")

    def write_file(self, data: OrderedDict) -> None:
        """
        Write the generated content to a YAML file
        """
        with open(self.output_file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
            logging.info(f"Data Asset file generated at {self.output_file_path}")

    def add_optional_config(self, stream: dict, data: dict) -> dict:
        """
        Add optional configurations like description, version, and tags
        """
        try:
            optional_config = [DESCRIPTION, TAGS]
            for config in optional_config:
                config_value = data.get(config)
                if config_value:
                    stream[config] = config_value
        except Exception as e:
           logging.error(f"Error occurred while adding optional config to the deployment stream: {e}")
        return stream


    def generate(self) -> None:
        """
        Generate the Data Asset YAML file
        """
        try:
            data = self.get_config()
            self.check_required_values(data)

            # Build the Data Asset schema
            data_asset_stream = OrderedDict([
                ('$schema', DATA_ASSET_SCHEMA),
                ('type', data.get(TYPE)),
                ('name', data.get(DATA_ASSET_NAME)),
                ('path', data.get(PATH)),
                ('version', data.get(VERSION))
            ])

            # Add optional fields
            updated_data_asset_stream = self.add_optional_config(data_asset_stream, data)

            self.write_file(updated_data_asset_stream)

        except Exception as e:
            logging.error(f"AzDataAssetRegisterFileGenerator: Error occurred - {e}")