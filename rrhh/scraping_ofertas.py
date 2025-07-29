from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configuración del navegador en modo headless
options = Options()
options.add_argument('--headless')  # No abre ventana
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Inicializa el driver
driver = webdriver.Chrome(options=options)
driver.get('https://www.iis-princesa.org/fundacion/ofertas-de-empleo/')

try:
    # Esperamos hasta que haya al menos una fila en la tabla de ofertas
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.convocat-table table tbody tr"))
    )

    # Parseamos el HTML renderizado
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tabla = soup.find('div', class_='convocat-table').find('table')
    filas = tabla.find_all('tr')[1:]  # Saltamos la cabecera

    ofertas = []
    print(f"[DEBUG] Nº de filas: {len(filas)}")
    for i, fila in enumerate(filas, start=1):
        celdas = fila.find_all('td')
        print(f"[DEBUG] Fila {i} - Nº celdas: {len(celdas)}")
        for j, celda in enumerate(celdas, start=1):
            print(f"  - Celda {j}: {celda.get_text(strip=True)}")


except Exception as e:
    print("[❌] Error durante el scraping:", str(e))

finally:
    driver.quit()
