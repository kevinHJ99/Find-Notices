from Prueba_tecnica_NEQUI.utils.selenium_functions import AutomationFunctions as af
from Prueba_tecnica_NEQUI.utils.config_variables import *
from Prueba_tecnica_NEQUI.utils.imports import *

## cargar excel
def to_load_excel():
    if os.path.exists(INPUT_DATA_PATH):
        wb = load_workbook(INPUT_DATA_PATH)
        logging.info("Conectado a la fuenta de informacion de Excel")
    else:
        logging.critical("El archivo no se encuentra o no existe")
        return

    sheet = wb.active
    person_id = sheet['B']
    names = sheet['A']
    return person_id, names


def start_driver(id, names):
    options = Options()

    # Desactivar geolocalización con las preferencias
    prefs = {
        "profile.default_content_setting_values.geolocation": 2  # Bloquea todas las solicitudes de geolocalización
    }
    
    options.add_argument('--incognito') # execute chrome in incognito mode
    options.add_argument("--disable-webrtc")
    options.add_argument('--no-sandbox') # disable sandbox
    options.add_argument("--disable-gpu")  # disable use to GPU for better velocity
    options.add_argument('--disable-infobars') # disable inforbars
    options.add_argument('--disable-web-security') # reduce web page security
    options.add_argument("--disable-geolocation") # inhabilite geolocalotion
    options.add_argument("--disable-popup-blocking") # inhabilite pop-up blocking
    options.add_argument('--ignore-certificate-errors') # disable prevention certificates in web page 
    options.add_argument(f"--user-agent={USER_AGENT}") # inicialite driver with preferal user-agent
    options.add_argument('--disable-blink-features=AutomationControlled') # disable chrome automation notification
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", prefs)
    
    driver = af.set_up_Chrome(PROCURADURIA_URL, options) # set driver

    to_find_report(driver, id, names) # find notice in this function


def resolve_captcha(driver):

    flag = True 
    while flag == True: 
        text_captcha = driver.find_element(By.XPATH, '//*[@id="lblPregunta"]').text
    
        if '¿ Cuanto es' in text_captcha and not "X" in text_captcha:
            num = re.findall(r'\d+', text_captcha)
    
            if '+' in text_captcha: 
                result = int(num[0]) + int(num[1])
                af.do_stringByName(driver, PROCURADURIA_ASK, result)
                flag = False
            elif '-' in text_captcha: 
                result = int(num[0]) - int(num[1])
                af.do_stringByName(driver, PROCURADURIA_ASK, result)
                flag = False
        else:
            sleep(1)
            af.do_clickByName(driver, 'ImageButton1')


def to_find_report(driver, id, names):
    notices_list = list() # save data
    iframe = driver.find_element(By.XPATH, '//iframe[@class="embed-responsive-item"]')
    driver.switch_to.frame(iframe)
    
    for cella, cellb in zip(names, id):
        if "nombre_completo" in cella.value and "Numero_documento" in cellb.value:
            continue
        else:
            sleep(3)
            type_id = driver.find_element(By.XPATH, '//select[@id="ddlTipoID"]')
            # Crear un objeto Select
            select = Select(type_id)
            # Seleccionar una opción por el texto visible
            select.select_by_visible_text("Cédula de ciudadanía - NUIP")
            
            af.do_stringByName(driver, PROCURADURIA_ID, Keys.CONTROL+"a"+Keys.DELETE)
            af.do_stringByName(driver, PROCURADURIA_ID, cellb.value)
            resolve_captcha(driver)

            af.do_clickByName(driver, "btnConsultar")
            input("algo...: ")
            break


def execute():
    items = to_load_excel()
    start_driver(items[0], items[1])


if __name__ == "__main__":
    execute()