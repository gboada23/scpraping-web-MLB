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

    df = pd.DataFrame({"EQUIPO": teams, "LIGA": leagues, "AVERAGE": avgs})
    df.AVERAGE = df.AVERAGE.astype(float)
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
                'EQUIPO': team_name,
                'VICTORIAS': wins,
                'DERROTAS': losses,
                'PORCENTAJE_VICTORIAS': win_percentage,
                'RECORD HOMECLUB': home_record,
                'RECORD VISITANTE': away_record})
    df_recor = pd.DataFrame(data)
    df_recor = df_recor.drop_duplicates()
    df_equipo_avg = equipo_avg()
    MLB = pd.merge(df_recor,df_equipo_avg, on="EQUIPO", how="inner")
    return MLB


DF_TEAM_STATS = records()
print(DF_TEAM_STATS)