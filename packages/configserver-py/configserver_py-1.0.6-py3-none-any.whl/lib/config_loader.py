import os
import yaml
import requests
import re
import logging

# Configurar el logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ConfigLoader:
    def __init__(self, config_server_env_var: str = "CONFIG_PROFILE", base_path: str = None):
        """
        Inicializa el ConfigLoader.
        :param config_server_env_var: Nombre de la variable de entorno que define el perfil activo.
        :param base_path: Ruta base donde se encuentran los archivos de configuración YAML.
        """
        self.profile = os.getenv(config_server_env_var)
        if not self.profile:
            raise EnvironmentError(f"Environment variable '{config_server_env_var}' is not set.")
        
        # Ajustar la ruta base para que sea relativa al directorio raíz del proyecto
        self.base_path = base_path or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/resources/properties"))
        self.local_config = {}
        self.config_server_url = None

    def load_local_config(self):
        """
        Carga el archivo YAML correspondiente al perfil activo.
        Si no se encuentra, utiliza el archivo 'py-default.yaml' como fallback.
        """
        file_name = f"py-{self.profile}.yaml"
        file_path = os.path.join(self.base_path, file_name)

        # Si el archivo específico no existe, usa 'py-default.yaml'
        if not os.path.exists(file_path):
            logger.warning(f"File {file_path} not found. Falling back to 'py-default.yaml'.")
            file_path = os.path.join(self.base_path, "py-default.yaml")
            if not os.path.exists(file_path):
                logger.error(f"Configuration file not found: {file_path}")
                raise FileNotFoundError(f"Configuration file not found: {file_path}")
        else:
            logger.info(f"Configuration file found: {file_path}")

        logger.info(f"Loading configuration file: {file_path}")
        with open(file_path, "r") as file:
            self.local_config = yaml.safe_load(file)

        logger.info(f"Loaded configuration: {self.local_config}")  # Agregado para depuración

        # Validar que 'application.name' esté presente
        if not self.local_config.get("application", {}).get("name"):
            logger.error(f"'application.name' is missing in the configuration file: {file_path}")
            raise ValueError(f"'application.name' is missing in the configuration file: {file_path}")
        else:
            logger.info(f"'application.name' found in the configuration file: {file_path}")

        # Obtener la URL del Config Server desde el archivo YAML
        self.config_server_url = self.local_config.get("config_server_url")
        if not self.config_server_url:
            raise ValueError("Config server URL is missing in the local configuration.")

    def fetch_remote_config(self):
        """
        Consume el Config Server para obtener las propiedades remotas.
        """
        application_name = self.local_config.get("application", {}).get("name")
        if not application_name:
            raise ValueError("Application name is missing in the local configuration.")

        url = f"{self.config_server_url}/{application_name}/{self.profile}"
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            raise ConnectionError(f"Failed to fetch remote config: {response.status_code}")

        config_data = response.json()

        # Procesar el campo "propertySources"
        remote_config = {}
        for source in config_data.get("propertySources", []):
            properties = source.get("source", {})
            for key, value in properties.items():
                # Convierte el valor a str y reemplaza placeholders
                value = str(value)
                if "${" in value:
                    value = self._replace_placeholders(value)
                remote_config[key] = value

        return remote_config

    def _replace_placeholders(self, value: str) -> str:
        """
        Reemplaza placeholders en el formato ${VAR:default}.
        """
        pattern = r"\$\{(.*?):(.*?)\}"
        matches = re.findall(pattern, value)
        for match in matches:
            env_var, default = match
            replacement = os.getenv(env_var, default)
            value = value.replace(f"${{{env_var}:{default}}}", replacement)
        return value

    def inject_as_env_variables(self, config: dict):
        """
        Inyecta las propiedades como variables de entorno.
        """
        for key, value in config.items():
            if isinstance(value, dict):
                # Aplana las propiedades anidadas
                for sub_key, sub_value in value.items():
                    env_key = f"{key.upper()}_{sub_key.upper()}"
                    os.environ[env_key] = str(sub_value)
            else:
                os.environ[key.upper()] = str(value)

    def get_config(self):
        """
        Combina las propiedades locales y remotas e inyecta como variables de entorno.
        """
        remote_config = self.fetch_remote_config()
        combined_config = {**remote_config, **self.local_config}
        self.inject_as_env_variables(combined_config)
        return combined_config


def inject_config(key: str):
    """
    Decorador para inyectar valores de configuración en atributos o métodos.
    """
    def decorator(target):
        if isinstance(target, property):
            # Decorador para propiedades
            return property(lambda self: os.getenv(key.upper()))
        elif callable(target):
            # Decorador para funciones
            def wrapper(*args, **kwargs):
                config_value = os.getenv(key.upper())
                return target(*args, config_value=config_value, **kwargs)
            return wrapper
        else:
            raise TypeError("Unsupported target for @inject_config")
    return decorator
