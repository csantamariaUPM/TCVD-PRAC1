# Importamos las librerias necesarias
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# El script está preparado para extraer información de las viviendas de Fotocasa para Madrid Capital
# Usaremos un bucle for en el cual elegimos el rango de páginas a mostrar (las primeras 70 páginas).

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


for t in range(1, 71):
    print("página: ", t)
    # Al ser la primera página distinta del resto, hacemos uso de un if-else
    if t < 2:
        url = 'https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/todas-las-zonas/l'
        driver.get(url)
        time.sleep(2)
        # Maximizamos la página
        driver.maximize_window()
        time.sleep(1)
        # Cerramos el pop up que aparece al entrar en fotocasa
        driver.find_element_by_xpath('//*[@id="App"]/div[2]/div/div/div/footer/div/button[2]').click()
    else:
        url = 'https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/todas-las-zonas/l/' + format(t, )
        driver.get(url)
        time.sleep(1)
    
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
    for product in bs4_html.find_all('article'):

        # Precio:
        price = product.find('span', {'class': 're-CardPrice'})
        precio = price.text if price else "Sin información"
        lista_precios.append(precio)

        # m2:
        size = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon--surface'})
        m2 = size.text if size else "Sin información"
        lista_m2.append(m2)

        # Planta:
        floor = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--floor'})
        planta = floor.text if floor else "Sin información"
        lista_planta.append(planta)

        # Baños:
        bath = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--bathrooms'})
        baños = bath.text if bath else "Sin información"
        lista_baños.append(baños)

        # Habitaciones:
        rooms = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--rooms'})
        habitaciones = rooms.text if rooms else "Sin información"
        lista_habitaciones.append(habitaciones)

        # Calefacción:
        heating = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--heating'})
        calefacción = heating.text if heating else "Sin calefacción"
        lista_calefaccion.append(calefacción)

        # Aire acondicionado:
        air_conditioner = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--air_conditioner'})
        AC = air_conditioner.text if air_conditioner else "Sin AC"
        lista_aireAC.append(AC)
        
        # Ascensor:
        elevator = product.find('span', {
            'class': 're-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--elevator'})
        ascensor = elevator.get_text() if elevator else "Sin ascensor"
        lista_ascensor.append(ascensor)
        
        # Título:
        title = product.find('span', {
            'class': 're-CardTitle re-CardTitle--big'})
        titulo = title.text if title else "Sin título"
        titulo = titulo.replace(',', '/') # Para evitar la posterior confusión al usar la coma como separador de campo
        lista_titulos.append(titulo) 

        # Enlace
        href = product.find('a', href=True)
        lista_enlaces.append('https://www.fotocasa.es' + href['href'])  
        
# Cerramos la ventana que abrimos con selenium
driver.close()


# Creamos un DF con las listas de datos extraidas             
df_pisos = pd.DataFrame(list(zip(lista_titulos, lista_precios, lista_m2, lista_planta, lista_baños, lista_habitaciones, lista_calefaccion, lista_aireAC, lista_ascensor, lista_enlaces)), 
               columns =['Títulos', 'Precios', 'M2', 'Planta', 'Baños', 'Habitaciones', 'Calefacción', 'AireAC', 'Ascensor', 'Enlace']) 

# Guardamos el dataframe en un archivo csv
df_pisos.to_csv('Inmuebles en venta en Madrid Capital.csv', index=False)