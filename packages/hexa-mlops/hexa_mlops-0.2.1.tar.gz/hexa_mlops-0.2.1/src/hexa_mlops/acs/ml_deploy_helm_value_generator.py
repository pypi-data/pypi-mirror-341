import logging
import yaml
import os
from ..utils.acs_utils import *
from ..base.file_generator import FileGenerator
class MLDeploymentHelmValueGenerator(FileGenerator):
    """
    Class for generating Helm values files for ML deployments.
    """

    def __init__(
        self, 
        config_file_path: str, 
        output_file_path: str,
        phase_name: str,
        model_config_file_path: str,
    ):
        """
        Initializes an instance of the MLDeploymentHelmValueGenerator class.

        Args:
            config_file_path (str): The path to the configuration file.
            output_file_path (str): The path to the generated file.
            model_name (str): The name of the model.
            phase_name (str): The name of the phase.
            base_path (str): The base path for the generated file.
        """
        super().__init__(config_file_path, output_file_path)
        self.phase_name = phase_name
        self.model_config_file_path = model_config_file_path
        self.common_config = self.get_common_config()

    @staticmethod
    def create_phase(phase: Phase, docker_dict: Dict) -> Dict:
            reverse_proxy = phase["reverse_proxy"]
            if reverse_proxy is not None:
                reverse_proxy = ReverseProxy(**reverse_proxy)

            
            phase_dict = {
                **phase,
                "docker": docker_dict[phase["docker"]],
                "docker_helm": docker_dict[phase["docker_helm"]],
                "reverse_proxy": reverse_proxy,
            }
            return phase_dict
    def get_common_config(self):
        """
        Retrieves common configuration information from a YAML file.

        Returns:
            dict: A dictionary containing common configuration information.
        """
        common_config = self.get_config()

        #build env
        raw_env_dict = {env["name"]: env for env in common_config.get("environments", [])}

        # Building the inherited dictionary for each environment
        # Then doing preprocessing on the dict (Jinja notably)
        processed_env_dict = [
            Environment.build_processed_dict(
                Environment.build_inherited_dict(raw_env_dict, name)
            )
            for name in raw_env_dict.keys()
        ]

        # Building common config phase with docker information
        docker_dict = {docker["name"]: Docker(**docker) for docker in common_config.get("docker", [])}

        return Config(
            model_storage=common_config["model_storage"],
            phases= [Phase(**self.create_phase(phase, docker_dict)) for phase in common_config.get("phases", [])],
            environments=[Environment(**env) for env in processed_env_dict],
            labels=common_config["labels"],
        )

    def get_model_configs(self):
        """
        Retrieves model configuration information from a YAML file.

        Returns:
            dict: A dictionary containing model configuration information.
        """
        logging.info(f"Retrieving model configuration from file: {self.model_config_file_path}")
        try:
            with open(self.model_config_file_path, 'r') as file:
                model_configs = yaml.safe_load(file)
            
            # Test if model environment is declared in common configuration file, environment field 
            model_config_lst = []
            for model_config in model_configs:
                
                env_data = model_config["environment"]
                try:
                    environment = next(
                        env for env in self.common_config.environments if env.name == env_data["name"]
                    )
                except StopIteration:
                    raise ValueError(
                        f"Environment {env_data['name']}, referenced in model config: {model_config} not found in config"
                    )
                # Get model versions
                versions = [Version(**version) for version in model_config["versions"]]

                # Get cluster info if model cluster phase is declared in common config and as requested phase
                clusters = [
                        Cluster(
                            phase=next(
                                phase for phase in self.common_config.phases if phase.name == cluster["phase"]
                            ),
                            deploy=Deploy(**cluster["deploy"]),
                        )
                        for cluster in model_config["clusters"]
                        if cluster["phase"] in self.phase_name 
                    ]
                
                
                # If model belong to a cluster phase, create model config object
                if clusters and model_config["monitoring_input_path"]:
                    model_info = Model(
                    name=model_config["name"],
                    environment=environment,
                    environment_version=env_data["version"],
                    versions=versions,
                    clusters=clusters,
                    monitoring_input_path=model_config.get("monitoring_input_path")
                )

                    model_config_lst.append(model_info)
            return model_config_lst

        except FileNotFoundError as e:
            logging.error(f"Model configuration file not found: {self.model_config_file_path}")
            raise e
        
    @staticmethod
    def get_image_value(model: Model, cluster: Cluster) -> str:
        docker = cluster.phase.docker_helm
        env = model.environment
        env_version = model.environment_version
        if cluster.phase.namespace:
            return f"{docker.registry}/{docker.namespace}/{docker.repository}/{env.name}:{env_version}"
        return f"{docker.registry}/{docker.repository}/{env.name}:{env_version}"

    @staticmethod
    def build_version_details( model: Model, version:str, total_weight:float, model_path: Dict) -> Dict:
        return {
            "version": version.version,
            "version_path": model_path.render(
                {
                    "model": model.name,
                    "version": version.version,
                }
            ),
            "percentage": version.weight / total_weight * 100,
        }

    def get_monitoring_input(self, model: Model):
        monitoring_input_path = os.path.join(
        os.path.dirname(self.config_file_path), model.monitoring_input_path
    )
        if os.path.exists(monitoring_input_path):
            with open(monitoring_input_path) as f:
                return f.read()
        raise FileNotFoundError(f"""Monitoring input file not found for model {model.name}""")
        
    def model_values(self, model: Model, cluster: Cluster) -> Dict:
        total_weight = float(sum([version.weight for version in model.versions]))
        deploy = cluster.deploy
        model_values = {
            "name": model.name,
            "image": self.get_image_value(model, cluster),
            "versions": " ".join([str(v.version) for v in model.versions]),
            "versions_details": [
                self.build_version_details(
                    model, v, total_weight, model.environment.model_version_path
                )
                for v in model.versions
            ],
            "minReplicas": deploy.min_replicas,
            "maxReplicas": deploy.max_replicas,
            "memory": deploy.memory,
            "cpu": deploy.cpu,
            "targetCPU": deploy.target_cpu,
            "envVars": deploy.env_vars,
            "port": model.environment.port,
            "metricsPort": model.environment.metrics_port,
            "readinessPath": model.environment.readiness_path,
            "readinessPort": model.environment.readiness_port,
            "labels": model.environment.labels,
        }
        if self.get_monitoring_input(model):
            model_values["monitoring_input"] = self.get_monitoring_input(model)
        return model_values
    
    
    def generate(self):
        logging.info(f"Generating configuration for phase {self.phase_name}")

        # Get phase
        phase = phase = next(phase for phase in self.common_config.phases if phase.name == self.phase_name)

        # Get models info
        model_config_list = self.get_model_configs()
        models = {
                model.name: self.model_values(model, cluster)
                for model in model_config_list
                for cluster in model.clusters
                if cluster.phase.name == self.phase_name
         }

        content = {
            "models": models,
            "containerName": self.common_config.model_storage,
            "labels": { **self.common_config.labels, **phase.labels,},
            "reverse_proxy": {
                "image": phase.reverse_proxy.image,
                "replicas": phase.reverse_proxy.replicas,
                "memory": phase.reverse_proxy.memory,
                "cpu": phase.reverse_proxy.cpu,
            },
        }
        if phase.reverse_proxy:
            content["reverse_proxy"] = {
                "image": phase.reverse_proxy.image,
                "replicas": phase.reverse_proxy.replicas,
                "memory": phase.reverse_proxy.memory,
                "cpu": phase.reverse_proxy.cpu,
            }

        self.write_file(content)

    def write_file(self, content):
        with open(self.output_file_path, "w") as values_file:
            yaml.dump(content, values_file)
  

