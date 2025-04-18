import os
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
import shutil
import logging
from typing import Any
import mlflow
import atexit
import signal
from collections import defaultdict


def now() -> str:
    return "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"


def convert_to_dns_name(string: str) -> str:
    # Convert the string to lowercase
    string = string.lower()

    # Replace non-alphanumeric characters with hyphens
    string = "".join("-" if not c.isalnum() else c for c in string)

    # Remove leading and trailing hyphens
    string = string.strip("-")

    # Replace multiple consecutive hyphens with a single hyphen
    string = "-".join(filter(None, string.split("-")))

    # Ensure the resulting string is not empty
    if not string:
        raise ValueError(f"Cannot convert `{string}` to DNS name.")

    return string


def _exit_handler():
    """End the current MLFlow run on exit or crash."""
    mlflow.end_run()


class EcidaModule:
    def __init__(self, name: str, version: str):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        self._name = convert_to_dns_name(name)
        self._version = version
        self._description = ""

        self._inputs = {}
        self._outputs = {}
        self._configs = {}

        self._topics_envVars = {}
        self._topics_names = {}
        self._consumers = {}
        self._directories = {}
        self._producer = None
        self._initialized = False
        self._kafka_config = {}

        self._tracking_prefix = os.environ.get("MLFLOW_TRACKING_PREFIX")
        if self._tracking_prefix:
            self._tracking_prefix += "-"
        else:
            self._tracking_prefix = ""
        self._metric_steps = defaultdict(int)

        self._deployed = os.getenv("ECIDA_DEPLOY", "").lower() == "true"

        self.logger.debug(
            f"{name}:{version} is initialized with deployed = {self._deployed}"
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def topics_envVars(self) -> dict[str, str]:
        return self._topics_envVars

    @property
    def inputs(self) -> dict[str, str]:
        return self._inputs

    @property
    def outputs(self) -> dict[str, str]:
        return self._outputs

    @property
    def configs(self) -> dict[str, str]:
        return self._configs

    @property
    def directories(self) -> dict[str, str]:
        return self._directories

    @property
    def description(self) -> str:
        return self._description

    @name.setter
    def name(self, _value):
        raise AttributeError("Attribute is read-only")

    @version.setter
    def version(self, _value):
        raise AttributeError("Attribute is read-only")

    @version.setter
    def deployed(self, _value):
        raise AttributeError("Attribute is read-only")

    def add_input(self, inp: str, type: str):
        inp = convert_to_dns_name(inp)

        self._inputs[inp] = type
        self._topics_envVars[inp] = "KAFKA_TOPIC_" + inp.upper()

    def add_output(self, out: str, type: str):
        out = convert_to_dns_name(out)

        self._outputs[out] = type
        self._topics_envVars[out] = "KAFKA_TOPIC_" + out.upper()

    def add_config(self, conf: str, type: str):
        conf = convert_to_dns_name(conf)

        self._configs[conf] = type

    def add_input_directory(self, inp: str):
        localPath = convert_to_dns_name(inp)
        self._inputs[inp] = "directory"
        self.directories[inp] = {}
        self.directories[inp]["localPath"] = localPath

    def add_output_directory(self, out: str):
        localPath = convert_to_dns_name(out)
        self._outputs[out] = "directory"
        self.directories[out] = {}
        self.directories[out]["localPath"] = localPath

    def add_input_from_git(self, name: str, git: str, path: str):
        self.add_input_directory(name)
        self.__add_git_to_directory(name, git, path)

    def add_output_to_git(self, name: str, git: str, path: str):
        self.add_output_directory(name)
        self.__add_git_to_directory(name, git, path)

    def add_description(self, description: str):
        self._description = description

    def get_path(self, name: str) -> str:
        if self._deployed:
            return "/" + self.directories[name]["localPath"]
        else:
            return "./" + self.directories[name]["localPath"]

    def __add_git_to_directory(self, name: str, git: str, path: str):
        self._directories[name]["source"] = git
        self._directories[name]["folder"] = path

    def _create_directory(self, directory_path: str):
        if os.path.exists(directory_path):
            self.logger.debug(f"Deleting existing directory: {directory_path}")
            shutil.rmtree(directory_path)

        try:
            self.logger.debug(f"Creating directory: {directory_path}")
            os.mkdir(directory_path)
        except OSError as e:
            self.logger.error(f"Failed to create directory: {directory_path}")
            self.logger.error(f"Error: {str(e)}")

    def to_yaml(self) -> str:
        return str(self._inputs) + "\n" + str(self._outputs)

    def set_kafka_config(self, config: dict[str, Any]):
        """
        Set Kafka consumer and producer configuration parameters.

        Args:
            config (dict): Dict containing Kafka configuration parameters
                           like 'session.timeout.ms', 'heartbeat.interval.ms', etc.
        """
        self._kafka_config = config
        self.logger.info(f"Kafka configuration updated: {config}")
        return self

    def initialize(self):
        if self._deployed:
            has_kafka_input = False
            for _, value in self._inputs.items():
                if value != "directory":
                    has_kafka_input = True
            has_kafka_output = False
            for _, value in self._outputs.items():
                if value != "directory":
                    has_kafka_output = True

            if has_kafka_input or has_kafka_output:
                self._KAFKA_BOOTSTRAP_SERVER = os.environ["KAFKA_BOOTSTRAP_SERVER"]
                self._KAFKA_SASL_MECHANISM = os.environ["KAFKA_SASL_MECHANISM"]
                self._KAFKA_SECURITY_PROTOCOL = os.environ["KAFKA_SECURITY_PROTOCOL"]
                self._KAFKA_USERNAME = os.environ["KAFKA_USERNAME"]
                self._KAFKA_PASSWORD = os.environ["KAFKA_PASSWORD"]
                self._KAFKA_GROUP_ID = os.environ["KAFKA_USERNAME"]
                self._KAFKA_CA_CERT_PATH = os.environ["KAFKA_CA_CERT_PATH"]

            for input_name, input_type in self._inputs.items():
                if input_type == "directory":
                    continue

                topic_name = os.environ.get(self._topics_envVars[input_name])
                self._topics_names[input_name] = topic_name

                # Base consumer configuration
                consumer_config = {
                    "bootstrap_servers": self._KAFKA_BOOTSTRAP_SERVER,
                    "sasl_plain_username": self._KAFKA_USERNAME,
                    "sasl_plain_password": self._KAFKA_PASSWORD,
                    "sasl_mechanism": self._KAFKA_SASL_MECHANISM,
                    "security_protocol": self._KAFKA_SECURITY_PROTOCOL,
                    "group_id": self._KAFKA_GROUP_ID,
                    "ssl_cafile": self._KAFKA_CA_CERT_PATH,
                }

                # Apply any custom Kafka configuration
                for config_key, config_value in self._kafka_config.items():
                    consumer_config[config_key] = config_value

                consumer = KafkaConsumer(topic_name, **consumer_config)
                self._consumers[input_name] = consumer

            if len(self._outputs) > 0 and has_kafka_output:
                # Base producer configuration
                producer_config = {
                    "bootstrap_servers": self._KAFKA_BOOTSTRAP_SERVER,
                    "sasl_plain_username": self._KAFKA_USERNAME,
                    "sasl_plain_password": self._KAFKA_PASSWORD,
                    "sasl_mechanism": self._KAFKA_SASL_MECHANISM,
                    "security_protocol": self._KAFKA_SECURITY_PROTOCOL,
                    "ssl_cafile": self._KAFKA_CA_CERT_PATH,
                }

                # Apply relevant producer configs from kafka_config
                producer_keys = [
                    "batch_size",
                    "linger_ms",
                    "buffer_memory",
                    "max_request_size",
                ]
                for key in producer_keys:
                    if key in self._kafka_config:
                        producer_config[key] = self._kafka_config[key]

                self._producer = KafkaProducer(**producer_config)

            for output_name, output_type in self._outputs.items():
                if output_type == "directory":
                    continue

                self._topics_names[output_name] = os.environ.get(
                    self._topics_envVars[output_name]
                )

            self._initialized = True

        else:
            for output in self._outputs:
                if output in self._directories:
                    path = self.get_path(self._directories[output]["localPath"])
                    self._create_directory(path)

        mlflow.set_experiment(os.environ.get("MLFLOW_EXPERIMENT_NAME") or self._name)
        mlflow.start_run(os.environ.get("MLFLOW_RUN_ID"))

        atexit.register(_exit_handler)
        signal.signal(signal.SIGTERM, _exit_handler)
        signal.signal(signal.SIGINT, _exit_handler)

    def push(self, output_channel: str, message: Any) -> bool:
        output_channel = convert_to_dns_name(output_channel)

        if not self._deployed:
            print(f"{now()} {output_channel}: {message}")
            return

        if output_channel not in self._outputs:
            return False

        if output_channel not in self._topics_names:
            self.logger.warning(f"Cannot push to disconnected output {output_channel}")
            return False

        self._producer.send(
            self._topics_names[output_channel],
            value=str(message).encode("utf-8"),
        )
        return True

    def pull(self, input_name: str, timeout_ms: int | None = None) -> str | None:
        """
        Pull data from the specified input, with an optional timeout.
        If no timeout is set, will wait indefinitely.

        NOTE: either always use a timeout or not - do not omit the timeout only from some calls.

        Args:
            input_name (str): The name of the input to pull from

        Returns:
            str: The data pulled from the input
        """
        input_name = convert_to_dns_name(input_name)

        if not self._deployed:
            return input(f"{now()} {input_name}:")

        if input_name not in self._inputs:
            return None

        if input_name not in self._topics_names:
            self.logger.warning(f"Cannot pull from disconnected input {input_name}")
            return None

        # poll() returns a dict of topic name to list of messages,
        # so we poll 1 message (max_records=1) and return it, if it exists
        if timeout_ms is not None:
            topic_in_partitions = self._consumers[input_name].poll(
                timeout_ms=timeout_ms, max_records=1
            )
            for _, records in topic_in_partitions.items():
                for record in records:
                    return record.value.decode("utf-8")

            return None

        # If no timeout is given, use the iterator interface to fetch messages
        for msg in self._consumers[input_name]:
            return msg.value.decode("utf-8")

    def get_config(self, conf: str) -> str | None:
        """
        Get the value of a config.

        Args:
            conf (str): Name of the config to get the value of

        Returns:
            str | None: The config value, or None if the config does not exist or was not set.
        """
        conf = convert_to_dns_name(conf)

        if conf not in self._configs:
            self.logger.warning(f"Config {conf} does not exist")
            return None

        value = os.environ.get("CONF_" + conf.upper())

        if value is None:
            self.logger.warning(f"Config {conf} has not been set")
            return None

        return value

    def log_params(self, **params: dict[str, float]):
        """Log parameters for experiment tracking."""
        params = {
            f"{self._tracking_prefix}{key}": value for key, value in params.items()
        }
        mlflow.log_params(params)

    def log_metric(self, metric_name: str, value: float):
        """Log a metric value for experiment tracking."""
        metric_name = f"{self._tracking_prefix}{metric_name}"

        mlflow.log_metric(metric_name, value, step=self._metric_steps[metric_name])
        self._metric_steps[metric_name] += 1

    def enable_large_messages(self):
        """Allow sending and receiving larger messages than default."""
        self.set_kafka_config(
            {
                "auto_offset_reset": "earliest",
                "enable_auto_commit": True,
                "fetch_max_bytes": 104857600,  # 100MB max fetch size
                "max_partition_fetch_bytes": 104857600,  # 100MB max partition fetch
                "max_poll_records": 500,  # Process 500 messages per poll
                "max_poll_interval_ms": 300000,  # 5 minutes to avoid rebalancing
                "request_timeout_ms": 305000,  # Slightly higher than max_poll_interval
                "session_timeout_ms": 60000,  # 60 seconds timeout
                "heartbeat_interval_ms": 20000,  # Heartbeat every 20 seconds
            }
        )
