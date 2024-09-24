import psycopg2 as pg
from openpyxl import workbook

if os.path.exists("../data/solicitudes de información.xlsx"): #verificar si el excel existe
    wb = load_workbook("../data/solicitudes de información.xlsx")


sheet = wb.active # obtener hoja de calculo
id_persona = [cell.value for cell in sheet['B'] if cell.value is not None] # obtener numeros de documento de la lista

# conectar a la base de datos
connect = pg.connect(
    dbname='db_test',
    user='User1999',
    password="123456.",
    host="redshift-cluster",
    port="9000"
)

## definir el objeto que permitira interactuar con la db
cursor = connect.cursor()

## definir una variable con la query
query = f"""
SELECT
    Numero_documento
    Nombre
    Edad
    Ingresos
    Fecha_nacimiento
    Tipo_cuenta_nequi
FROM
    finacle_demografico.clientes
WHERE
    Numero_documento IN {id_persona}
"""

cursor.execute(query) ## ejecutar consulta
results = cursor.fetchall() ## obtener resultados

# iterar por cada resultado
for field in results:
    print(field)

## cerrar el cursor y la conexion
cursor.close()
connect.close()