import os

class ConfigProperty:
    """
    Descriptor para obtener valores de configuración desde variables de entorno.
    """
    def __init__(self, key: str, default=None, value_type=str):
        self.key = key.upper()
        self.default = default
        self.value_type = value_type

    def __get__(self, instance, owner):
        config_value = os.getenv(self.key, self.default)
        if config_value is None:
            raise ValueError(f"Environment variable '{self.key}' is not set and no default value is provided.")
        try:
            return self.value_type(config_value)
        except ValueError:
            raise ValueError(f"Environment variable '{self.key}' could not be converted to {self.value_type.__name__}.")


def Property(key: str, default=None, value_type=str):
    """
    Decorador para asociar un atributo de clase con una clave de configuración.
    :param key: Clave de la configuración (nombre de la variable de entorno).
    :param default: Valor predeterminado si la variable de entorno no está configurada.
    :param value_type: Tipo al que se debe convertir el valor (por defecto, str).
    """
    return ConfigProperty(key, default, value_type)
