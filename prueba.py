from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de búsqueda base
def juegos_del_dia():
    # URL de búsqueda base
    base_url = "https://www.mlb.com/scores/"
    # Obtener la fecha de hoy
    fecha_actual = datetime.today()
    busqueda_url = fecha_actual.strftime("%Y-%m-%d")
    # Realizar GET
    url_completa = base_url + busqueda_url
    respuesta = requests.get(url_completa)
    data = BeautifulSoup(respuesta.content, "html.parser")
    # Extraer info de la página
    buscar_resultados = data.find_all("div", class_="grid-itemstyle__GridItemWrapper-sc-cq9wv2-0 gmoPjI")

    resultados = []

    for resultado in buscar_resultados:
        texto = resultado.find("div", class_="StatusLayerstyle__StatusLayerWrapper-sc-1s2c2o8-1 jkfZwE")
        equipos = resultado.find_all("div", class_="TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 fdaoCu")
        puntajes = resultado.find_all("td", class_="table-cellstyle__StyledTableCell-sc-xpntj7-2 ljCIPI")
        pitchers = resultado.find_all("div", class_="playerMatchupstyle__PlayerNameWrapper-sc-u51t3a-4 dsJFMP trk-playermatchup-name")
        eras = resultado.find_all("span", class_="PlayerMatchupsstyle__PlayeStatsContentWrapper-sc-1l2t29f-0 gYSWCv")
        if texto is not None:
            if len(puntajes) <6:
                efectividad = [era.text for era in eras]
                lanzadores = [pitcher.text for pitcher in pitchers]
                resultados.append({
                    "Pitcher V":lanzadores[0],
                    "W-L V":efectividad[0],
                    "Era 1": efectividad[1],
                    "Pitchers HC": lanzadores[1],
                    "W-L HC":efectividad[2],
                    "Era 2": efectividad[3]
                })
    df = pd.DataFrame(resultados)
    df['Era 1'] = df['Era 1'].str.replace(' ERA', '').str.replace('|', '')
    df['Era 2'] = df['Era 2'].str.replace(' ERA', '').str.replace('|', '')
    numericas = ["Era 1","Era 2"]
    for i in numericas:
        df[i] = df[i].astype(float)
    return df
                
print(juegos_del_dia())