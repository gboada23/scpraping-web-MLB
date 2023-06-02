import requests
from requests_html import HTMLSession
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
    df.AVG_TEAM = df.AVG_TEAM.astype(float)
    return df


def records():
    fecha = datetime.today().strftime("%Y-%m-%d")
    session = HTMLSession()
    url = f'https://www.mlb.com/standings/mlb/{fecha}'
    response = session.get(url)
    response.html.render(timeout=10)
    teams = response.html.find('tr')
    data = []
    for team in teams:
        team_link = team.find('span.team--name a.team.p-text-link--mlb', first=True)
        if team_link is not None:
            team_name = team_link.attrs['data-team-name']
            wins = team.find('td.col-1', first=True).text
            losses = team.find('td.col-2', first=True).text
            win_percentage = team.find('td.col-3', first=True).text
            home_record = team.find('td.col-12', first=True).text
            away_record = team.find('td.col-13', first=True).text
            data.append({
                'TEAM': team_name,
                'WINS': wins,
                'LOSSES': losses,
                '%WIN': win_percentage,
                'RECORD HOMECLUB': home_record,
                'RECORD VISITANTE': away_record})
    df_recor = pd.DataFrame(data)
    df_recor = df_recor.drop_duplicates()
    df_equipo_avg = equipo_avg()
    MLB = pd.merge(df_recor,df_equipo_avg, on="TEAM", how="inner")
    # Mapeo de nombres completos a disminutivos
    team_mapping = {
    "Tampa Bay Rays": "TB",
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
    "Chicago White Sox": "CWS",
    "Kansas City Royals": "KC",
    "Oakland Athletics": "OAK"
}
    # Supongamos que tu DataFrame se llama df y la columna se llama 'VISITANTE'
    MLB[['win_hc', 'lost_hc']] = MLB['RECORD HOMECLUB'].str.split('-', expand=True)
    # Convertir las nuevas columnas a números enteros
    MLB['win_hc'] = MLB['win_hc'].astype(int)
    MLB['lost_hc'] = MLB['lost_hc'].astype(int)
    # Calcular el porcentaje de victorias
    MLB['%WIN-HC'] = round(MLB['win_hc'] / (MLB['win_hc'] + MLB['lost_hc']),3)

    MLB[['win_v', 'lost_v']] = MLB['RECORD VISITANTE'].str.split('-', expand=True)
    # Convertir las nuevas columnas a números enteros
    MLB['win_v'] = MLB['win_v'].astype(int)
    MLB['lost_v'] = MLB['lost_v'].astype(int)
    # Calcular el porcentaje de victorias
    MLB['%WIN-V'] = round(MLB['win_v'] / (MLB['win_v'] + MLB['lost_v']),3)
    # Reemplazar los nombres completos por los disminutivos en el dataframe
    MLB.drop(columns=['RECORD HOMECLUB','RECORD VISITANTE', "win_hc","lost_hc","win_v","lost_v"],inplace=True)
    MLB["TEAM"] = MLB["TEAM"].map(team_mapping)

    return MLB


DF_TEAM_STATS = records()
print(DF_TEAM_STATS)