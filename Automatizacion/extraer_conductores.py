import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. Configuración de Chrome Driver
options = webdriver.ChromeOptions()
# Maximizar pantalla para cargar todos los elementos correctamente
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    # 2. Abrir la página inicial para iniciar sesión manualmente una sola vez
    print("Abriendo el sistema...")
    driver.get("https://center.nurvans.com/")
    print("\n" + "="*50)
    print("INICIA SESIÓN EN LA VENTANA DEL NAVEGADOR.")
    input("Cuando ya estés dentro del sistema, presiona ENTER aquí para empezar la extracción...")
    print("="*50 + "\n")

    datos_extraidos = []

    # 3. Define el rango de IDs que deseas extraer (ejemplo: del 1 al 569)
    id_inicio = 1
    id_fin = 569

    wait = WebDriverWait(driver, 5)

    for perfil_id in range(id_inicio, id_fin + 1):
        url = f"https://center.nurvans.com/conductor/perfil/{perfil_id}"
        driver.get(url)

        nombre = ""
        celular = ""

        # --- Extracción del Nombre ---
        try:
            # Selector exacto por la clase .driver-name
            nombre_elem = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3.driver-name"))
            )
            # Limpiamos espacios en blanco o saltos de línea
            nombre = nombre_elem.text.strip()
        except:
            nombre = ""

        # --- Extracción del Celular ---
        try:
            # Busca el span hermano del icono del teléfono fa-phone dentro de info-item
            celular_elem = driver.find_element(
                By.XPATH, 
                "//div[contains(@class, 'info-item')]//i[contains(@class, 'fa-phone')]/following-sibling::span"
            )
            celular = celular_elem.text.strip()
        except:
            try:
                # Alternativa si el span está dentro del mismo bloque directamente
                celular_elem = driver.find_element(
                    By.XPATH, 
                    "//div[contains(@class, 'info-item') and .//i[contains(@class, 'fa-phone')]]//span"
                )
                celular = celular_elem.text.strip()
            except:
                celular = ""

        # Si encontró al menos nombre o celular (o puedes guardar todos los IDs)
        if nombre or celular:
            print(f"[OK] ID {perfil_id}: {nombre} | Tel: {celular}")
        else:
            print(f"[SIN DATOS] ID {perfil_id}: Perfil vacío o inexistente")

        datos_extraidos.append({
            "N°": perfil_id,
            "NOMBRE": nombre,
            "NUMERO DE CELULAR": celular
        })

        # Pequeña pausa opcional para no saturar peticiones
        time.sleep(0.3)

    # 4. Guardar los resultados directamente en un archivo Excel
    df = pd.DataFrame(datos_extraidos)
    nombre_archivo = "conductores_nurvans_resultado.xlsx"
    df.to_excel(nombre_archivo, index=False)

    print("\n" + "="*50)
    print(f"¡EXTRACCIÓN COMPLETADA! Archivo guardado como: {nombre_archivo}")
    print("="*50)

finally:
    driver.quit()