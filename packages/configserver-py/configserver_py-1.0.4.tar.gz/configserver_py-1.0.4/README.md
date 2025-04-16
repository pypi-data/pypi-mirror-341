# ConfigServer-Py

ConfigServer-Py es una biblioteca de Python para consumir Spring Cloud Config Server y gestionar configuraciones.

## Características
- Carga configuraciones locales desde archivos YAML.
- Obtiene configuraciones remotas desde un Config Server.
- Inyecta configuraciones como variables de entorno.

## Instalación
Puedes instalar el paquete desde PyPI con:
```bash
pip install configserver-py
```

## Uso
Ejemplo básico de uso:
```python
from configserver_py import ConfigLoader

loader = ConfigLoader()
config = loader.get_config()
print(config)
```

## Contribuir
Si deseas contribuir al proyecto, por favor abre un issue o envía un pull request en [GitHub](https://github.com/your-repo/backstage-lib).

## Licencia
Este proyecto está licenciado bajo la Licencia MIT.
