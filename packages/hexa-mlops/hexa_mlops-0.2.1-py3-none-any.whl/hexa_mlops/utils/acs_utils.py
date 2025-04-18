from dataclasses import dataclass, field, fields, is_dataclass
from jinja2 import Template
from typing import List, Dict, Optional, get_origin, get_args, Union

def checkNonNullDataclass(instance):
    if not is_dataclass(instance):
        raise ValueError("Provided instance is not a dataclass")

    for field in fields(instance):
        value = getattr(instance, field.name)
        field_type = field.type

        # Check if the field type is Optional (i.e., Union[..., None])
        if get_origin(field_type) is Union and type(None) in get_args(field_type):
            # Skip validation for Optional fields
            continue

        # Raise an error if the value is None for non-Optional fields
        if value is None:
            raise ValueError(f"Field '{field.name}' cannot be None")

@dataclass
class Environment:
    name: str
    version: int
    dockerfile: str
    port: int
    metrics_port: int
    readiness_path: str
    readiness_port: int
    model_version_path: Template
    build_args: Dict[str, str]
    labels: Dict[str, str]

    def __post_init__(self):
        checkNonNullDataclass(self)

    @staticmethod
    def build_processed_dict(data):
        """
        This is a helper function to process the model_version_path field in the environment
        It is converting it to a jinja template
        """
        jinja_template = Template(data["model_version_path"])
        copy = {
            **data,
        }
        copy["model_version_path"] = jinja_template
        return copy

    @staticmethod
    def build_inherited_dict(
        all_envs_dict,
        env_name,
    ):
        """
        This is a helper function to build the inherited dictionary for the environment
        It is used to resolve the inheritance of the environment
        """
        current_dict = {}

        def get_field(field_name, env, depth=0):

            MAX_INHERITANCE_DEPTH = 3
            if depth > 3:
                raise ValueError(
                    f"Inheritence depth exceeded {MAX_INHERITANCE_DEPTH} in environment {env_name}: Do a simpler config"
                )

            if field_name in env:
                return env[field_name]
            else:
                if not "parent_environment" in env:
                    raise ValueError(
                        f"Field {field_name} is not defined in environment {env_name} and it has no parent"
                    )
                parent_name = env["parent_environment"]
                if not parent_name:
                    raise ValueError(
                        f"Field {field_name} is not defined in environment {env_name} and it's parent is empty"
                    )

                parent = all_envs_dict[parent_name]
                if not parent:
                    raise ValueError(
                        f"Field {field_name} is not defined in environment {env_name} and it's parent {parent_name} is not defined"
                    )

                return get_field(field_name, parent, depth + 1)

        fields = [
            "name",
            "version",
            "dockerfile",
            "port",
            "metrics_port",
            "readiness_path",
            "readiness_port",
            "model_version_path",
            "build_args",
            "labels",
        ]

        current_env = all_envs_dict[env_name]
        for field in fields:
            current_dict[field] = get_field(field, current_env)

        return current_dict

@dataclass
class Docker:
    name: str
    registry: str
    namespace: str
    repository: str

    def __post_init__(self):
        checkNonNullDataclass(self)

@dataclass
class ReverseProxy:
    image: str
    replicas: int
    memory: str
    cpu: str

    def __post_init__(self):
        checkNonNullDataclass(self)    
@dataclass
class Phase:
    name: str
    cluster: str
    namespace: str
    docker: Docker  # Optional field with default value None
    docker_helm: Docker
    reverse_proxy: Optional[ReverseProxy] = None
    labels: Dict[str, str] = field(default_factory=dict)  # Default empty dictionary

    def __post_init__(self):
        checkNonNullDataclass(self)
        
@dataclass
class Config:
    model_storage: str
    labels: Dict[str, str]
    phases: List[Phase] = field(default_factory=list)
    environments: List[Environment] = field(default_factory=list)

    def __post_init__(self):
        checkNonNullDataclass(self)

@dataclass
class Version:
    version: int
    weight: int

    def __post_init__(self):
        checkNonNullDataclass(self)

@dataclass
class Deploy:
    max_replicas: int
    min_replicas: int
    target_cpu: int
    memory: str
    cpu: str
    env_vars: Dict[str, str]

    def __post_init__(self):
        checkNonNullDataclass(self)
@dataclass
class Cluster:
    phase: Phase
    deploy: Deploy

    def __post_init__(self):
        checkNonNullDataclass(self)

@dataclass
class Model:
    name: str
    environment: Environment
    environment_version: int
    versions: List[Version]
    clusters: List[str]
    monitoring_input_path: Optional[str] = None

    def __post_init__(self):
        checkNonNullDataclass(self)