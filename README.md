# Find-Notices

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Estructura](#Estructura)
- [Organización](#Organizacion)
- [Tecnologías](#Tecnologías)
- [Instalación](#Instalacion)
- [chromedriver](#chromedriver)
- [Contacto](#contacto)

## Descripción

Este proyecto es un scraper desarrollado como parte de una prueba tecnica. Su objetivo es extraer datos estructurados de el sitio web especificado y almacenarlos en un excel para su posterior análisis. El scraper está diseñado para ser simple y eficiente, demostrando habilidades básicas de web scraping y manipulación de datos.

## Características Clave

- Extracción de Datos Específicos: Recupera información relevante de la página web objetivo, como encabezados, descripciones y enlaces.
- Almacenamiento en excel: Guarda los datos extraídos en un archivo de excel para facilitar su análisis y manipulación.
- Fácil de Usar: Implementación sencilla y directa que permite ejecutar el scraper con comandos mínimos, o incluso solo haciendo doble click en el archivo find_notices.py.

## Estructura
Prueba_tecnica_NEQUI/
│
├── AWS/
│   └── connection_to_db.py
│
├── data/
│   ├── resultados.xlsx
│   └── solicitudes_informacion.xlsx
│
├── logs/
|  ├── notices_log.log
│
├── utils/
│   ├── config_variables.py
│   ├── imports.py
│   └── selenium_functions.py
│
├── scripts/
│   ├── find_notices.py
│   └── find_procuraduria.py
│
└── requirements.txt

## Descripción de Carpetas y Archivos
AWS/
  connection_to_db.py: Aqui se encuentra el codigo para resolver la conexion y la query para conectarse a redshift a traves de postgressSQL.

data/
    data.json: Datos almacenados en formato JSON después de ser procesados por el scraper.

logs/
    test_scraper.log: Archivo de registro para pruebas del scraper.

utils/
  config_variables.py: Archivo que contiene variables globales de configuración utilizadas en el proyecto.
  imports.py: Archivo con las importaciones necesarias para los scripts del proyecto.
  selenium_functions.py: Archivo que contiene funciones relacionadas con Selenium para el proyecto.

scripts/
  find_notices.py: Archivo principal para la ejecución principal del proyecto.
  find_procuraduria.py: archivo de prueba para ejecutar consultas automatizadas, en la pagina de la procuraduria y resolver captcha

requirements.txt: Archivo que lista las dependencias de Python necesarias para el proyecto.

## Uso y Organización
Organización: La estructura está diseñada para separar claramente diferentes aspectos del proyecto, como prueba de base de datos, datos, utilidades y scripts principales.

Acceso a Datos: Los archivos de datos de salida (resultados.xlsx) se encuentran en la carpeta específica (data), al igual que los datos de entrada (selicitudes_informacion.xlsx), mientras que los archivos (*.log) están organizados dentro de la carpeta logs/ según el entorno de prueba y producción.

Utilidades: Los archivos utils/ proporcionan funciones adicionales necesarias para el proyecto.


## Tecnologías
- Lenguaje: Python v3.10
- Librerías: Selenium, pycopg2, openpyxl, pandas
  - estas librerias estan listas para ser instaladas, y se encuentran en el archivo requeriments.txt
  - Comando: pip install -r requeriments.txt
- Sistema: Any
- venv: opcional

## Instalación y Uso
1. Clona este repositorio:
git clone https://github.com/kevinHJ99/Find-Notices
cd scripts
2. ejecuta el script de scraping:
   python find_notices.py
3. Los datos extraidos se almacenaran en un resultados.xlsx en el siguiente directorio ./data/resultados.xlsx

## NOTA
El scraper de la procuraduria solo esta como prueba para resolver el captcha, esto debido a que gran parte de los datos tienen un numero de documento erroneo, haciendo que la informacion no coincida con la tabla solicitudes de informacion o aparezcan errores como informacion no existente en el registro, al momento de realizar la consulta.
