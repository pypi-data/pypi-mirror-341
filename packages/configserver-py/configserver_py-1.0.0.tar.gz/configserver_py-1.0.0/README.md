# ConfigServer-Py

ConfigServer-Py es una biblioteca de Python para consumir Spring Cloud Config Server y gestionar configuraciones.

## Características
- Carga configuraciones locales desde archivos YAML.
- Obtiene configuraciones remotas desde un Config Server.
- Inyecta configuraciones como variables de entorno.

## Instalación
```bash
pip install configserver-py
```

## Uso
```python
from configserver_py import ConfigLoader

loader = ConfigLoader()
config = loader.get_config()
```

## Licencia
Este proyecto está licenciado bajo la Licencia MIT.
