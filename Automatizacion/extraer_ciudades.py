# CAPA 1 : IMPORTACIONES DE LIBRERIAS

import pandas as pd
from selenium import webdriver
import time

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


import os #se comunique con el sistema

# CAPA 2 : CONFIGURACION DEL DRIVER DE SELENIUM
# 1.configuracion del driver de Selenium
options = webdriver.ChromeOptions()
## agrandar la pantalla para cargar todos los elementos correctamente
options.add_argument("--start-maximized")

## driver de Selenium es para abrir el navegador y realizar la automatización
### service es para instalar el driver de Chrome automáticamente por que no es necesario descargarlo manualmente
### options es para configurar el driver de Selenium el que ya se definió en lineas anteriores
driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
# 2. Login manual en la pagina web
try:
    print("Se abrirá el navegador para iniciar sesión en la página web.")
    ## aqui se pone el login o la pagina web que se quiere automatizar
    driver.get("https://center.nurvans.com/")
    ## Se espera a que el usuario inicie sesión manualmente
    print("\n" + "="*50)
    print("INICIA SESIÓN EN LA VENTANA DEL NAVEGADOR.")
    ## aqui se espera a que el usuario inicie sesión manualmente y en este input es para almacer el enter
    input("Cuando ya estés dentro del sistema, presiona ENTER aquí para empezar la extracción...")
    print("="*50 + "\n")

    # CAPA 3: EXTRACCION DE DATOS

    #este arreglo es para almacenar los datos extraidos de la pagina web
    datos_extraidos = []

    #poner el inicio y el fin de los ids que se quieren extraer
    id_inicio = 1
    id_fin = 574

    #esperar a que se cargue la pagina web para extraer los datos
    wait = WebDriverWait(driver, 5)

    # 3. Generacion de URLS dinamicas para cada ciudad

    for perfil_id in range(id_inicio, id_fin + 1) : ##esta linea es para generar las urls dinamicas de cada ciudad
        url = f"https://center.nurvans.com/conductor/perfil/{perfil_id}" ##esta linea es para generar la url dinamica de cada ciudad
        driver.get(url) ##esta linea es para abrir la url dinamica de cada ciudad

        ##esta linea es para inicializar la variable ciudad
        ciudad = ""

        # -------------extraccion de la ciudad de cada URL----------------
        try :
            ciudad_elem = driver.find_element(
                By.XPATH,
                "//div[contains(@class, 'info-item') and .//i[contains(@class, 'fa-map-marker')]]//span"
            )
            #Extremos texto completo y borramos el "Conduce en:" que aparece antes de la ciudad
            texto_completo = ciudad_elem.text.strip()
            ciudad = texto_completo.replace("Conduce en: ", "").strip()
        except :
            try:
                ciudad_elem = driver.find_element(
                # 5. Xpath para extraer la ciudad de cada URL
                    By.XPATH,
                    "//div[contains(@class, 'info-item')]//i[contains(@class, 'fa-map-marker')]/following-sibling::span"
                )
                texto_completo = ciudad_elem.text.strip()
                ciudad = texto_completo.replace("Conduce en: ", "").strip()
            except:
                ciudad = ""

        # Si encontró al menos  (o puedes guardar todos los IDs)
        if ciudad:
            print(f"[OK] ID {perfil_id}: {ciudad}")
        else:
            print(f"[SIN DATOS] ID {perfil_id}: Sin ciudad")

        ## se creo un arreglo se agregan los datos extraidos de cada ciudad en el arreglo datos_extraidos
        datos_extraidos.append({
            "N°": perfil_id,
            "CIUDAD": ciudad
        })

        # Pequeña pausa opcional para no saturar peticiones
        time.sleep(0.3)

    # 4. Guardar los resultados directamente en un archivo Excel
    df = pd.DataFrame(datos_extraidos)
    # Definimos la ruta de la carpeta y el nombre del archivo
    carpeta_destino = r"D:\Descargas"
    nombre_archivo = "ciudad.xlsx"

    # Unimos la carpeta con el nombre del archivo (D:\Descargas\ciudad.xlsx)
    ruta_completa = os.path.join(carpeta_destino, nombre_archivo)

    try:
        # Guardamos el Excel en la ruta completa
        df.to_excel(ruta_completa, index=False)

        print("\n" + "="*50)
        print(f"¡EXTRACCIÓN COMPLETADA! Archivo guardado en: {ruta_completa}")
        print("="*50)
    except Exception as e:
        print(f"Error al guardar el archivo. Verifica que la carpeta D:\\Descargas exista y que el archivo no esté abierto. Detalle: {e}")

finally:
    driver.quit()  # Cierra el navegador al finalizar la extracción de datos
