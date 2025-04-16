import os

class ConfigProperty:
    def __init__(self, key, default=None, value_type=str):
        self.key = key
        self.default = default
        self.value_type = value_type

    def __get__(self, instance, owner):
        value = os.getenv(self.key.upper(), self.default)
        try:
            return self.value_type(value) if value is not None else None
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert environment variable '{self.key}' to {self.value_type.__name__}")

    def __set__(self, instance, value):
        raise AttributeError("Cannot set value for a configuration property")

def Property(key: str, default=None, value_type=str):
    """
    Decorador o descriptor para asociar un atributo o método con una clave de configuración.
    :param key: Clave de la configuración (nombre de la variable de entorno).
    :param default: Valor predeterminado si la variable de entorno no está configurada.
    :param value_type: Tipo al que se debe convertir el valor (por defecto, str).
    """
    def decorator(target):
        if isinstance(target, property):
            # Decorador para propiedades
            return property(lambda self: _get_env_value(key, default, value_type))
        elif callable(target):
            # Decorador para funciones
            def wrapper(*args, **kwargs):
                config_value = _get_env_value(key, default, value_type)
                return target(*args, config_value=config_value, **kwargs)
            return wrapper
        else:
            # Usar como descriptor
            return ConfigProperty(key, default, value_type)
    return decorator

def _get_env_value(key: str, default=None, value_type=str):
    """
    Obtiene el valor de una variable de entorno y lo convierte al tipo especificado.
    :param key: Clave de la variable de entorno.
    :param default: Valor predeterminado si la variable de entorno no está configurada.
    :param value_type: Tipo al que se debe convertir el valor.
    :return: Valor convertido o None.
    """
    value = os.getenv(key.upper(), default)
    try:
        return value_type(value) if value is not None else None
    except (ValueError, TypeError):
        raise ValueError(f"Cannot convert environment variable '{key}' to {value_type.__name__}")