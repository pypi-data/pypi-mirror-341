import yaml
from collections import OrderedDict
import logging
from ..base.constants import *
from ..base.file_generator import FileGenerator
yaml.add_representer(OrderedDict, FileGenerator.represent_ordereddict)

class AzPipelineFileGenerator(FileGenerator):
    """
    A class that represents an Azure Pipeline File Generator.

    This class is responsible for generating an Azure Pipeline YAML file based on the provided configuration.
    It provides methods to generate pipeline jobs, job inputs, job outputs, and the overall pipeline.

    Attributes:
        config_file_path (str): The path to the config.
        training_file_path (str): The path to the training data.
        output_file_path (str): The path to the generated file.
        pipeline_with_value (bool): Indicates whether to generate a pipeline with global input values. Defaults to True.

    Methods:
        get_training_file_contents(): Load content from the training pipeline file and return the pipeline inputs, outputs, and jobs.
        generate_global_inputs_outputs(item_list: list) -> dict: Generate global input/output based on the given global input/output list.
        generate_job_input/output(job_input: dict, inputs: dict, command: list) -> dict: Generate the Azure pipeline job inputs/outputs
        generate_pipeline_job(config: dict, job: dict) -> tuple: Generate a pipeline job based on the provided config and job information.
        generate_pipeline_jobs(config: dict, pipeline: list) -> OrderedDict: Generate pipeline jobs based on the provided config and pipeline.
        generate() -> yaml: Generate the Azure Pipeline YAML file based on the provided configuration.
    """
    def __init__(self,
                 config_file_path: str, 
                 output_file_path: str,
                 training_file_path: str, 
                 input_file_path: str=None,
                 pipeline_with_value: bool=True,
                
                ):
        """
        Initialize an instance of the AzurePipelineGenerator class.
        Args:
            config_file_path (str): The path to the config.
            training_file_path (str): The path to the training data.
            output_file_path (str): The path to the generated file.
            pipeline_with_value (bool): Indicates whether to generate a pipeline has input/output values. Defaults to True.
            input_file_path (str): The path to the input file to be generated. Defaults to None.
        """
   
        super().__init__(config_file_path, output_file_path)
        self.training_file_path = training_file_path
        self.pipeline_with_value = pipeline_with_value
        self.input_file_path = input_file_path

    def get_training_file_contents(self)-> tuple:
        """
        Args:
            training_file_path (str): The path to the training file.
        Returns:
            tuple: A tuple containing the pipeline inputs, pipeline outputs, and pipeline.
        """
        logging.info("Loading training documents from file: {}".format(self.training_file_path))
        
        with open(self.training_file_path, 'r') as file:
            documents = yaml.safe_load(file)
        
        pipeline_inputs = documents.get(INPUTS)
        pipeline_outputs = documents.get(OUTPUTS)
        pipeline = documents.get(STEPS)
        run_name = documents.get(RUN_NAME)
   
        if pipeline is None:
            logging.warning('No jobs found in the training documents.')
        
        return pipeline_inputs, pipeline_outputs, pipeline, run_name

    def generate_global_inputs_outputs(self, item_list: list)-> dict:
        """ Convert the format of global inputs/outputs from input file
        Args:
            item_list: list of global inputs or outputs
        Returns:
            dict: a dictionary containing inputs/outputs in a new format
        """
        generated_item = {}
        for item in item_list:
            item_name = item.get(JOB_NAME)
            item.pop(JOB_NAME)
            generated_item[item_name] = item
        return generated_item
    
    @staticmethod
    def generate_job_input_output(job_item: dict, return_value: dict, command: dict, is_output=False, with_value=True)-> list:
        """
        Generates the Azure pipeline job input/ output. 
        If the job input/output comes from global pipeline inputs/outputs (contains "parent" string), change the format of the input_value : input_value -> ${{input_value}}
        If the job input/output comes from a pipeline output (contains "outputs" string), change the format of the input_value : input_value -> ${{parent.jobs.input_value}}
        If the job input/output is defined directly in the job, keep the value as it is if with_value is True, else store these value in another place holder to be generated seperatedly

        Args:
            job_item (dict): A dictionary storing value of the input/output
            return_value (dict): A dictionary to store the new formatted job inputs
            command (dict): A dctionary to store all the configs (keys of the first key:value pairx of the job) to be included in the command of a py scripts, seperated by inputs/outputs key
            literal_value (dict): A dictionary to store input/output value if they are literal values and not referenced from another job
            is_output (bool): If true, the function is callled to generate a job output. If false, it is to generate a job input
            with_value (bool): If true, the function is called to generate a pipeline.yaml file with value. If false, it is to generate a pipeline without value (is used for a batch training endpoint deployment) 

        Returns:
            list: A list of 2 dictionaries: updated return value and literal value
        """

        literal_value = {}
        config_name, item_value = list(job_item.items())[0]
        
        # If job_item is a job input, the value must not be null
        if not is_output and not item_value:
            raise ValueError(f"Input value for {config_name} is None. A value is required")
        
        if is_output:
            command[OUTPUTS].append(config_name)
        if not is_output:
            command[INPUTS].append(config_name)

        # If item_value is a string, take into account the following scenario
        if isinstance(item_value, str):
            value_list = item_value.split(".")
            # if it references global input, keep the same content
            if "parent" in value_list:
                return_value[config_name] = "${{" + item_value + "}}"
            # if it references another job output, adjust the string value to reflect it
            elif "outputs" in value_list:
                return_value[config_name] = "${{parent.jobs." + item_value + "}}"
            # if plain string: 
            else:
                # keep the value as it is if to generate input/output for a pipeline with full value
                if with_value:
                    return_value[config_name] = item_value
                # save the value to literal_value dict and null value in return_value
                else:
                    literal_value[config_name] = item_value
                    return_value[config_name] = None
        else:
            if with_value:
                    return_value[config_name] = item_value   
            else:
                if item_value:
                        literal_value[config_name] = item_value
                return_value[config_name] = None

        return return_value, literal_value

    @staticmethod
    def validate_and_get_required_value(training_config: dict, key: str)-> str:
        """
        Validate the required value in the training config.
        Args:
            training_config (dict): The training config.
            key (str): The key to be validated.
        Returns:
            str: The value of the key.
        """
        value = training_config.get(key, EMPTY_CONSTANT)
        if not value:
            raise ValueError(f"The '{key}' key is missing from the config or its value is None")
        return value
    
    def generate_pipeline_job(self, training_config: dict, job: dict, literal_values:dict, with_value=True)-> tuple:
        """
        Args:
            training_config (dict): The config information.
            job (dict): The job information.
        Returns:
            tuple: A tuple containing the job name and the generated job value.
            A job value containing key:value pairs. The keys include: compute, environment, code, type, inputs, outputs, command
        """
        job_name = job.get(JOB_NAME)
        job_input_list = job.get(INPUTS)
        job_output_list = job.get(OUTPUTS)

        job_value = {}
        inputs = {}
        outputs = {}
        command = {INPUTS: [], OUTPUTS: []}

        compute_name = self.validate_and_get_required_value(training_config, COMPUTE_NAME)
        environment_name = self.validate_and_get_required_value(training_config, ENVIRONMENT_NAME)
        environment_version = self.validate_and_get_required_value(training_config, ENVIRONMENT_VERSION)
        source_code_path = self.validate_and_get_required_value(training_config, SOURCE_CODE_PATH)
    
        if with_value:
            for job_input in job_input_list:
                inputs,literal_values = self.generate_job_input_output(job_input, inputs, command)

            for job_output in job_output_list:
                outputs,literal_values = self.generate_job_input_output(job_output, outputs, command,is_output=True) 
        else:
            for job_input in job_input_list:
                inputs, literal_value = self.generate_job_input_output(job_input, inputs, command, with_value=False)
                literal_values[INPUTS].update(literal_value)
            for job_output in job_output_list:
                outputs, literal_value = self.generate_job_input_output(job_output, outputs, command,is_output=True, with_value=False) 
                literal_values[OUTPUTS].update(literal_value)
            
        # Generate command string 
        # TODO: Add support for other types of jobs
        command_str = "python " + job_name + PY_EXT
        for param in command[INPUTS]:
            command_str += " --" + param + " ${{inputs." + param + "}}"
        
        for param in command[OUTPUTS]:
            command_str += " --" + param + " ${{outputs." + param + "}}"
        
        job_value[TYPE] = COMMAND
        job_value[COMPUTE] = "azureml:" + str(compute_name)    
        job_value[COMMAND] = command_str
        job_value[CODE] =  str(source_code_path) + "/" + job_name + "/"
        job_value[INPUTS] = inputs
        job_value[OUTPUTS] = outputs
        job_value[ENVIRONMENT] = "azureml:" + environment_name + ":" + str(environment_version)
      
        return job_name, job_value, literal_values

    def generate_pipeline_jobs(self, config: dict, pipeline: list, with_value=True,) -> OrderedDict:
        """
        Args:
            config: config dictionary
            pipeline: pipeline list containing the pipeline definition.
        Returns:
            pipeline_jobs: An ordered dictionary containing the generated pipeline jobs.
        """
        logging.info("Read training_pipeline file, generating pipeline jobs....")
        pipeline_jobs = OrderedDict()
        literal_values = {INPUTS:{},OUTPUTS:{} }
        for job in pipeline:
            logging.info(f"Generating job: {job.get(JOB_NAME)}")
            if with_value:
                job_name, job_value, literal_values = self.generate_pipeline_job(config, job, literal_values)
            else:
                job_name, job_value, literal_values = self.generate_pipeline_job(config, job, literal_values, with_value=False)
            pipeline_jobs[job_name] = job_value
        return pipeline_jobs, literal_values

    def write_file(self, data: OrderedDict, output_file_path: str, file_type: str, is_inputs=False) -> None:
        """
        Write data to a file.
        Args:
            data (dict): The data to write to the file.
            output_file_path (str): The path to the generated file.
            file_type (str): The type of the file to be generated.
            is_inputs (bool): Indicates whether the file is an input file. Defaults to False.
        """
        with open(output_file_path, 'w') as file:
            if not is_inputs:
                yaml.dump(data, file, default_flow_style=False)
            else:
                yaml.dump(
                    {
                        "inputs":data[INPUTS],
                        "outputs": data[OUTPUTS]
                    }, 
                    file, default_flow_style=False)
            logging.info(f" {file_type} generated successfully at {output_file_path}")

    def generate(self) -> None:
        """
        Generate the Azure Pipeline YAML file based on the provided configuration.
        The pipeline.yaml file generated can contains global input value or not, control by value of self.pipeline_with_value
        Returns:
            yaml: The generated Azure Pipeline YAML content.
            The yaml file contains key:value pairs. The keys include: scheme, type, experiment_name, inputs, outputs, jobs.
        """
        try:
            
            config = self.get_config()
            training_config = config.get(TRAINING_PHASE,EMPTY_CONSTANT)
            if not training_config:
                raise ValueError("The 'training' key is missing from the config or its value is None")

             #Get information from training_pipeline file
            pipeline_inputs, pipeline_outputs,pipeline, run_name = self.get_training_file_contents()

            # Check which type of pipeline file to be generated
            if not self.pipeline_with_value:
                logging.info("Pipeline.yaml file to be generated is without input values")
                generated_pipeline_jobs,literal_value = self.generate_pipeline_jobs(training_config, pipeline, with_value=False )
                self.write_file(literal_value, self.input_file_path, "Input file", is_inputs=True)
            else:
                logging.info("Pipeline.yaml file to be generated is with input values ")
                generated_pipeline_jobs,_ = self.generate_pipeline_jobs(training_config, pipeline)

            
            pipeline_stream = OrderedDict([
                    ('$schema', PIPELINE_JOB_SCHEMA ),
                    ('type', "pipeline"),
                    ("experiment_name", config.get(EXPERIMENT_NAME,"")),
                    ("display_name", run_name),
                    ("jobs", generated_pipeline_jobs),
                ])

            if pipeline_inputs:
                logging.info("Generating global inputs ...")
                generated_pipeline_inputs = self.generate_global_inputs_outputs(pipeline_inputs)
                pipeline_stream.update({"inputs": generated_pipeline_inputs})
            else:
                logging.info("Global inputs are not defined. Pipeline file to be generated without global inputs")
    
            if pipeline_outputs:
                logging.info("Generating global outputs ...")
                generated_pipeline_outputs = self.generate_global_inputs_outputs(pipeline_outputs)
                pipeline_stream.update({"outputs": generated_pipeline_outputs})
            else: 
                logging.info("Global outputs are not defined. Pipeline file to be generated without global outputs")

            self.write_file(pipeline_stream, self.output_file_path, "Pipeline file")

        except Exception as e:
            logging.error("Error occurred while generating pipeline file: {}".format(e))