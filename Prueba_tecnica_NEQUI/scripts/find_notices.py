# Importamos funciones utilitarias y variables de configuración desde otros módulos
from Prueba_tecnica_NEQUI.utils.selenium_functions import AutomationFunctions as af
from Prueba_tecnica_NEQUI.utils.config_variables import *
from Prueba_tecnica_NEQUI.utils.imports import *

# Configuramos el sistema de logging para registrar información en un archivo log
logging.basicConfig(filename='../logs/notices_log.log', encoding='utf-8', level=logging.INFO)


def to_load_excel():
    """
     Verifica si el archivo de entrada existe y carga los datos de la columna A del archivo Excel.
    """
    
    if os.path.exists(INPUT_DATA_PATH):
        wb = load_workbook(INPUT_DATA_PATH)  # Carga el archivo Excel
        logging.info("Conectado a la fuente de información de Excel")
    else:
        logging.critical("El archivo no se encuentra o no existe")  # Registra un error si el archivo no existe
        return

    sheet = wb.active  # Selecciona la hoja activa del archivo Excel
    column = sheet['A']  # Selecciona la columna A (que contiene los datos)
    return column  # Retorna la columna para ser usada más adelante


def start_driver(column):
    """
    object = column
    
    Configura y arranca el navegador Chrome con varias opciones de privacidad y seguridad,
    como el bloqueo de geolocalización, ejecución en modo incógnito, etc. Luego llama a la función para buscar noticias.
    """
    
    options = Options()  # Crea una instancia de opciones para el navegador

    # Preferencias del navegador para desactivar la geolocalización
    prefs = {
        "profile.default_content_setting_values.geolocation": 2  # Bloquea todas las solicitudes de geolocalización
    }
    
    # Configuraciones adicionales para el navegador Chrome
    options.add_argument('--incognito')  # Ejecuta Chrome en modo incógnito
    options.add_argument("--disable-webrtc")
    options.add_argument('--no-sandbox')  # Desactiva el sandbox de Chrome
    options.add_argument("--disable-gpu")  # Desactiva el uso de la GPU
    options.add_argument('--disable-infobars')  # Desactiva las infobarras de notificación
    options.add_argument('--disable-web-security')  # Reduce la seguridad web
    options.add_argument("--disable-geolocation")  # Desactiva la geolocalización
    options.add_argument("--disable-popup-blocking")  # Desactiva el bloqueo de ventanas emergentes
    options.add_argument('--ignore-certificate-errors')  # Ignora errores de certificados de seguridad
    options.add_argument(f"--user-agent={USER_AGENT}")  # Usa un "user-agent" específico
    options.add_argument('--disable-blink-features=AutomationControlled')  # Desactiva la detección de automatización
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Configuración adicional para ocultar el uso de Selenium
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", prefs)  # Aplica las preferencias definidas

    # Inicia el navegador Chrome con las opciones configuradas
    driver = af.set_up_Chrome(GOOGLE_URL, options)

    # Llama a la función para buscar noticias usando el driver y la columna de datos
    to_find_notice(driver, column)


def to_find_notice(driver, column):
    """
    object = driver
    object = column
    
    Realiza búsquedas en Google basadas en los nombres obtenidos del archivo Excel, 
    agrega los resultados de las búsquedas a una lista.
    """
    
    notices_list = list()  # Lista para almacenar la información obtenida
    
    # Itera sobre cada celda de la columna
    for cell in column:
        if "nombre_completo" in cell.value:  # Omite la primera fila que puede ser el encabezado
            continue
        else:
            sleep(3)  # Espera 3 segundos entre iteraciones
            # Limpia el campo de búsqueda de Google y realiza una nueva búsqueda con el nombre y la palabra "criminal"
            af.do_stringByXpath(driver, G_SEARCH, Keys.CONTROL+"a"+Keys.DELETE)
            af.do_stringByXpath(driver, G_SEARCH, f"{cell.value} criminal"+Keys.ENTER)
            # Guarda la información obtenida de la noticia en la lista
            notices_list.append(to_get_notice(driver, cell.value))  
            logging.info("")

    # Transforma la lista de datos en un archivo Excel
    transform_list(notices_list)


def to_get_notice(driver, NAME): 
    """
    object = driver
    string = NAME
    
    Obtiene las noticias de cada búsqueda, incluyendo la URL, el título y la descripción, y las almacena.
    """
    
    sleep(5)  # Espera 5 segundos para que cargue la página
    try:
        # Intenta hacer clic en un botón específico si existe
        af.do_clickByXpath(driver, '//*[@class="mpQYc"]/g-raised-button')
    except: 
        pass

    global description
    # Espera hasta que los elementos de la noticia estén presentes en la página
    items = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, ITEMS))
    )
    
    delimiter = 0
    # Itera sobre los elementos de las noticias
    for item in items:
        sleep(3)
        try:
            # Intenta obtener la descripción de la noticia
            description = item.find_element(By.XPATH, './/*[@class="kb0PBd cvP2Ce A9Y9g"]//span[2]').text
            print(NAME, "||", description.upper())
        except NoSuchElementException:
            logging.warning("No se encontró el elemento.")  # Loguea si el elemento no existe
        except TimeoutException:
            logging.warning("No se encontró el elemento a tiempo.")  # Loguea si el tiempo de espera se excedió
        finally:
            # Si el nombre aparece en la descripción, se guarda la información de la noticia
            if NAME.upper() in description.upper(): 
                logging.info("Se encontraron noticias sobre esta Persona!")
                url = item.find_element(By.XPATH, './/a[@jsname="UWckNb"]').get_attribute('href')
                notice = item.find_element(By.XPATH, './/a/h3').text 
                name = NAME
                logging.info("Se tomaron los datos encontrados!")
                return [NAME, url, notice, description]
            else:
                delimiter += 1
                # Si no se encuentran noticias relevantes después de 6 intentos, se loguea la ausencia de noticias
                if delimiter >= 6: 
                    logging.warning("No se encontraron noticias sobre esta persona!")
                    return [NAME, None, None]


def transform_list(data): 
    """
    object = data
    
    Transforma la lista de noticias en un archivo Excel.
    """
    
    # Crea un DataFrame de pandas con los datos obtenidos
    data_frame = pd.DataFrame(data, columns=["Nombre Persona", "URL", "Noticia", "Descripción"])
    # Guarda los datos en un archivo Excel
    data_frame.to_excel(OUTPUT_DATA_PATH, index=False)
    logging.info("Información almacenada correctamente.")


def execute():
    """
    Función principal que coordina todo el flujo de trabajo.
    """
    
    column = to_load_excel()  # Carga los datos del archivo Excel
    start_driver(column)  # Inicia el driver de Selenium con los datos cargados


# Ejecuta el proceso si este script es ejecutado directamente
if __name__ == "__main__":
    execute()
