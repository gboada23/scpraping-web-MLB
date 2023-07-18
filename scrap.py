import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image

def equipo_avg():
    url = "https://www.mlb.com/es/stats/team"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    teams = [span.text for span in soup.select('span.full-3fV3c9pF')]
    leagues = [td.text for td in soup.select('td.col-group-end-2UJpJVwW.number-aY5arzrB.align-left-3L2SU-Mk.is-table-pinned-1WfPW2jT')]
    avg_elements = soup.select('td.col-group-start-sa9unvY0.number-aY5arzrB.align-right-3nN_D3xs.is-table-pinned-1WfPW2jT') 
    avgs = []
    for avg in avg_elements:
        if avg.get('data-col') == '14':
            avgs.append(avg.text)  
    df = pd.DataFrame({"TEAM": teams, "LIGA": leagues, "AVG_TEAM": avgs})
    team_mapping = {"Tampa Bay Rays": "TB",
    "Texas Rangers": "TEX",
    "Baltimore Orioles": "BAL",
    "Arizona Diamondbacks": "ARI",
    "Los Angeles Dodgers": "LAD",
    "Atlanta Braves": "ATL",
    "Houston Astros": "HOU",
    "New York Yankees": "NYY",
    "Minnesota Twins": "MIN",
    "New York Mets": "NYM",
    "Toronto Blue Jays": "TOR",
    "Boston Red Sox": "BOS",
    "Milwaukee Brewers": "MIL",
    "Seattle Mariners": "SEA",
    "Los Angeles Angels": "LAA",
    "Pittsburgh Pirates": "PIT",
    "Miami Marlins": "MIA",
    "San Francisco Giants": "SF",
    "Detroit Tigers": "DET",
    "Cincinnati Reds": "CIN",
    "San Diego Padres": "SD",
    "Cleveland Guardians": "CLE",
    "Philadelphia Phillies": "PHI",
    "St. Louis Cardinals": "STL",
    "Chicago Cubs": "CHC",
    "Washington Nationals": "WSH",
    "Colorado Rockies": "COL",
    "Chicago White Sox": "CHW",
    "Kansas City Royals": "KC",
    "Oakland Athletics": "OAK"}
    df["TEAM"] = df["TEAM"].map(team_mapping)
    df.AVG_TEAM = df.AVG_TEAM.astype(float)
    return df

def ESPN():
    url = "https://www.espn.com/mlb/standings/_/group/overall"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tds = soup.find("tbody", {"class": "Table__TBODY"})

    span = tds.find_all("a", {"class":"AnchorLink"})
    data = [i.text for i in span]
    new_data = []
    for elemento in data:
        if len(elemento)>=2 and len(elemento)<=3:
            new_data.append(elemento)
    df1 = pd.DataFrame({"TEAM":new_data})
    # Encontrar todos los elementos span con clase stat-cell
    spans = soup.findAll('span', {'class': 'stat-cell'})

    # Extraer el texto de cada span y almacenarlo en una lista
    span_data = [span.text for span in spans]

    # Dividir la lista span_data en sublistas de longitud 11
    team_data = [span_data[i:i + 11] for i in range(0, len(span_data), 11)]

    # Crear un DataFrame con los datos recopilados
    columns = ["WINS", "LOSES", "%WIN", "DIFERENCIA", "RECORD HOMECLUB", "RECORD VISITANTE", "CA", "CP", "DIFERENCIA 2", "RACHA", "LAST-10"]
    df2 = pd.DataFrame(team_data, columns=columns)
    df2.drop(columns=['DIFERENCIA','DIFERENCIA 2'],inplace=True)
    MLB = pd.concat([df1, df2], axis=1)
    MLB[['win_hc', 'lost_hc']] = MLB['RECORD HOMECLUB'].str.split('-', expand=True)
    # Convertimos las nuevas columnas a enteros
    MLB['win_hc'] = MLB['win_hc'].astype(int)
    MLB['lost_hc'] = MLB['lost_hc'].astype(int)
    # Calcular el porcentaje de victorias
    MLB['%WIN-HC'] = round(MLB['win_hc'] / (MLB['win_hc'] + MLB['lost_hc']),3)
    MLB[['win_v', 'lost_v']] = MLB['RECORD VISITANTE'].str.split('-', expand=True)
    # volvemos a transformar a enteros
    MLB['win_v'] = MLB['win_v'].astype(int)
    MLB['lost_v'] = MLB['lost_v'].astype(int)
    MLB["CA"] = MLB['CA'].astype(int)
    MLB['CP'] = MLB["CP"].astype(int)
    MLB['WINS'] = MLB["WINS"].astype(int)
    MLB['%WIN'] = MLB["%WIN"].astype(float)
    MLB['LOSES'] = MLB["LOSES"].astype(int)
    # Calcular el porcentaje de victorias
    MLB['%WIN-V'] = round(MLB['win_v'] / (MLB['win_v'] + MLB['lost_v']),3)
    MLB["%CA"] = round(MLB['CA'] / (MLB['WINS'] + MLB['LOSES']),2)
    MLB["%CP"] = round(MLB['CP'] / (MLB['WINS'] + MLB['LOSES']),2)
    MLB.drop(columns=['CA','CP', "win_hc","lost_hc","win_v","lost_v","RECORD HOMECLUB","RECORD VISITANTE"],inplace=True)
    DF1 = equipo_avg()
    DF = pd.merge(MLB, DF1, on="TEAM", how="left")
    DF = DF[["TEAM","LIGA","WINS","LOSES","%WIN","%WIN-HC","%WIN-V","%CA","%CP","AVG_TEAM","RACHA","LAST-10"]]
    DF = DF.rename(columns={'%CA': 'SCORED/GAME', '%CP': 'ALLOWED/GAME'})
    return DF

def resultados():
    # URL de búsqueda base
    base_url = "https://www.mlb.com/scores/"
    # Obtener la fecha de hoy
    fecha_actual = datetime.today()

    resultados = []
    resultados1 = []

    for i in range(1,6,1):
        # Obtener la fecha de búsqueda
        fecha_busqueda = fecha_actual - timedelta(days=i)
        busqueda_url = fecha_busqueda.strftime("%Y-%m-%d")
        
        # Realizar GET
        url_completa = base_url + busqueda_url
        respuesta = requests.get(url_completa)
        data = BeautifulSoup(respuesta.content, "html.parser")
        
        # Extraer info de la página
        buscar_resultados = data.find_all("div", class_="grid-itemstyle__GridItemWrapper-sc-cq9wv2-0 gmoPjI")

        for resultado in buscar_resultados:
            texto = resultado.find("div", class_="StatusLayerstyle__StatusLayerWrapper-sc-1s2c2o8-1 jkfZwE")
            equipos = resultado.find_all("div", class_="TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 fdaoCu")
            puntajes = resultado.find_all("td", class_="table-cellstyle__StyledTableCell-sc-xpntj7-2 ljCIPI")
            if texto is not None:
                if len(equipos) >= 2 and len(puntajes) >= 6:
                    equipo1 = equipos[0]
                    equipo2 = equipos[1]
                    resultados.append({
                        'Fecha': busqueda_url,
                        'Titulo': texto.text.strip(),
                        'Visitante': equipo1.text.strip(),
                        'R1': puntajes[0].text.strip(),
                        'H1': puntajes[1].text.strip(),
                        'E1': puntajes[2].text.strip(),
                        'Home Club': equipo2.text.strip(),
                        'R2': puntajes[3].text.strip(),
                        'H2': puntajes[4].text.strip(),
                        'E2': puntajes[5].text.strip()
                    })
                else:
                    equipo1 = equipos[0]
                    equipo2 = equipos[1]
                    resultados1.append({
                        'Fecha': busqueda_url,
                        'Hora del juego': texto.text.strip(),
                        'Visitante': equipo1.text.strip(),
                        'R1': 0,
                        'H1': 0,
                        'E1': 0,
                        'Home Club': equipo2.text.strip(),
                        'R2': 0,
                        'H2': 0,
                        'E2': 0
                    })
            else:
                resultados.append({
                    'Fecha': busqueda_url,
                    'Titulo': 'Sin juegos para el dia de hoy',
                    'Equipo 1': None,
                    'R1': None,
                    'H1': None,
                    'E1': None,
                    'Equipo 2': None,
                    'R2': None,
                    'H2': None,
                    'E2': None
                })

    return pd.DataFrame(resultados), pd.DataFrame(resultados1)
resultados()


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
    resultados1 = []

    for resultado in buscar_resultados:
        texto = resultado.find("div", class_="StatusLayerstyle__StatusLayerWrapper-sc-1s2c2o8-1 jkfZwE")
        equipos = resultado.find_all("div", class_="TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 fdaoCu")
        puntajes = resultado.find_all("td", class_="table-cellstyle__StyledTableCell-sc-xpntj7-2 ljCIPI")
        if texto is not None:
            if len(equipos) >= 2 and len(puntajes) >= 6:
                equipo1 = equipos[0]
                equipo2 = equipos[1]
                resultados.append({
                    'Fecha': busqueda_url,
                    'Titulo': texto.text.strip(),
                    'Visitante': equipo1.text.strip(),
                    'R1': puntajes[0].text.strip(),
                    'H1': puntajes[1].text.strip(),
                    'E1': puntajes[2].text.strip(),
                    'Home Club': equipo2.text.strip(),
                    'R2': puntajes[3].text.strip(),
                    'H2': puntajes[4].text.strip(),
                    'E2': puntajes[5].text.strip()
                })
            else:
                equipo1 = equipos[0]
                equipo2 = equipos[1]
                resultados1.append({
                    'Fecha': busqueda_url,
                    'Hora': texto.text.strip(),
                    'Visitante': equipo1.text.strip(),
                    'VS': "vs",
                
                    'Home Club': equipo2.text.strip()
                })
        else:
            resultados.append({
                'Fecha': busqueda_url,
                'Titulo': 'Sin juegos para el dia de hoy',
                'Equipo 1': None,
                'R1': None,
                'H1': None,
                'E1': None,
                'Equipo 2': None,
                'R2': None,
                'H2': None,
                'E2': None
            })
    comenzados, sin_empezar = pd.DataFrame(resultados), pd.DataFrame(resultados1)
    sin_empezar["Hora"] = sin_empezar['Hora'].str.replace('Free Game of the Day', '')
    return comenzados, sin_empezar
comenzados, sin_empezar = juegos_del_dia()

def lanzadores_del_dia():
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

def concat():
    df_concatenado = pd.concat([sin_empezar, lanzadores_del_dia()], axis=1)
    df_concatenado = df_concatenado[["Fecha","Hora","Visitante","Pitcher V","W-L V","Era 1","VS","Home Club","Pitchers HC","W-L HC","Era 2"]]
    visitante = df_concatenado[["Fecha","Hora","Visitante","Pitcher V","W-L V","Era 1"]]
    home_club = df_concatenado[["Fecha","Hora","Home Club","Pitchers HC","W-L HC","Era 2"]]
    return visitante, home_club
visitante, homeclub = concat()
print(concat())
def get_team_logos():
    url = "https://www.mlb.com/team"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    team_logos = {}
    # Buscar todos los elementos de imagen en la página
    for img in soup.find_all("img"):
        # Solo considerar las imágenes que son logotipos de equipos
        if "Team Logo" in img.get("alt", ""):
            team_name = img["alt"].replace(" Team Logo", "")
            logo_url = "https:" + img["src"]
            team_logos[team_name] = logo_url
    return team_logos


