# Importamos las librerías necesarias
from datetime import time
# from selenium.webdriver.chrome.service import Service
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium.webdriver.chrome.options import Options
import whois
# El programa está preparado para extraer información de las 5 primeras páginas de Fotocasa para el distrito centro
# de Madrid. Usaremos un bucle for en el cual elegimos el rango de páginas a mostrar.

print("El propietario de la web es: ")
print(whois.whois('fotocasa.es'))
# Creamos una lista vacía por cada atributo que nos interesa guardar de los pisos
lista_precios = []
lista_m2 = []
lista_planta = []
lista_baños = []
lista_habitaciones = []
lista_calefaccion = []
lista_aireAC = []
lista_ascensor = []
lista_enlaces = []
lista_titulos = []

# Guardamos en una variable el path del chrome driver
chromedriver_path = "C:\\Users\\santa\\PycharmProjects\\TCV\\PEC1\\chromedriver.exe"
# Indicamos al webdriver que el navegador elegido es Chrome y le pasamos el path guardado antes por parámetro.
driver = webdriver.Chrome(chromedriver_path)

for t in range(1, 2):
    print("página: ", t)
    # Al ser la primera página distinta del resto, hacemos uso de un if-else
    if t < 2:
        url = 'https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/centro/l'
        driver.get(url)
        time.sleep(0.5)
        # Maximizamos la página
        driver.maximize_window()
        time.sleep(2)
        # Cerramos el pop up que aparece al entrar en fotocasa
        driver.find_element_by_xpath('//*[@id="App"]/div[2]/div/div/div/footer/div/button[2]').click()
    else:
        url = 'https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/centro/l/' + format(t, )
        driver.get(url)
        time.sleep(0.5)

    # Hacemos scroll hasta el final de la página para que se carguen todos los elementos
    length = 500

    for i in range(26):
        driver.execute_script("window.scrollTo(0, " + str(length) + ")")
        time.sleep(0.5)
        length += 500

    # Guardamos el código HTML de la página de interés en html_code
    html_code = driver.page_source

    # Lo parseamos a BeautifulSoup
    bs4_html = BeautifulSoup(html_code, "html.parser")

    # hacemos un bucle con la clase contenedora de cada anuncio, la cual agrupa la información de cada anuncio.

    for product in bs4_html.find_all('div', {'class': 're-CardPackPremium-info'}):

        # Precio:
        price = product.find('span', {'class': 're-CardPrice'})
        precio = price.get_text() if price else "Sin información"
        lista_precios.append(precio)

        # m2:
        size = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon--surface'})
        m2 = size.get_text() if size else "Sin información"
        lista_m2.append(m2)

        # Planta:
        floor = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--floor'})
        planta = floor.get_text() if floor else "Sin información"
        lista_planta.append(planta)

        # Baños:
        bath = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--bathrooms'})
        baños = bath.get_text() if bath else "Sin información"
        lista_baños.append(baños)

        # Habitaciones:
        rooms = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--rooms'})
        habitaciones = rooms.get_text() if rooms else "Sin información"
        lista_habitaciones.append(habitaciones)

        # Calefacción:
        heating = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--heating'})
        calefacción = heating.get_text() if heating else "Sin calefacción"
        lista_calefaccion.append(calefacción)

        # Aire acondicionado:
        air_conditioner = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--air_conditioner'})
        AC = air_conditioner.get_text() if air_conditioner else "Sin AC"
        lista_aireAC.append(AC)

        # Ascensor:
        elevator = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--elevator'})
        ascensor = elevator.get_text() if elevator else "Sin ascensor"
        lista_ascensor.append(ascensor)

        # Título:
        title = product.find('span', {
            'class': 're-CardTitle re-CardTitle--big'})
        titulo = title.get_text() if title else "Sin título"
        lista_titulos.append(titulo)

        # Extraemos el enlace de cada anuncio que se encuentra en otra clase diferente:
        for elemento in bs4_html.find_all('a', class_='re-CardPackPremium-carousel', href=True):
            lista_enlaces.append('https://www.fotocasa.es' + elemento['href'])

# Imprimimos el user agent
a = driver.execute_script("return navigator.userAgent")
print("User agent: ", a)

# Cerramos la ventana que abrimos con selenium
driver.close()

# Creamos un DF con las listas de datos extraidas             
df_pisos = pd.DataFrame(list(
    zip(lista_titulos, lista_precios, lista_m2, lista_planta, lista_baños, lista_habitaciones, lista_calefaccion,
        lista_aireAC, lista_ascensor, lista_enlaces)),
                        columns=['Títulos', 'Precios', 'M2', 'Planta', 'Baños', 'Habitaciones', 'Calefacción', 'AireAC',
                                 'Ascensor', 'Enlace'])

# Guardamos el dataframe en un archivo excel
df_pisos.to_csv('Pisos en venta en Madrid Capital.csv', index=False)
