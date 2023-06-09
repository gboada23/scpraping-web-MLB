import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

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
    MLB['LOSES'] = MLB["LOSES"].astype(int)
    # Calcular el porcentaje de victorias
    MLB['%WIN-V'] = round(MLB['win_v'] / (MLB['win_v'] + MLB['lost_v']),3)
    MLB["%CA"] = round(MLB['CA'] / (MLB['WINS'] + MLB['LOSES']),2)
    MLB["%CP"] = round(MLB['CP'] / (MLB['WINS'] + MLB['LOSES']),2)
    MLB.drop(columns=['CA','CP', "win_hc","lost_hc","win_v","lost_v","RECORD HOMECLUB","RECORD VISITANTE"],inplace=True)
    DF1 = equipo_avg()
    DF = pd.merge(MLB, DF1, on="TEAM", how="left")
    return DF

print(ESPN())

