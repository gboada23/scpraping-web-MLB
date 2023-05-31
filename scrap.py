import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def equipo_avg():
    # Realizar la solicitud HTTP a la página
    url = "https://www.mlb.com/es/stats/team"
    response = requests.get(url)

    # Crear el objeto BeautifulSoup para analizar el contenido HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar todos los elementos <span> con la clase "full-3fV3c9pF"
    span_elements = soup.find_all("span", class_="full-3fV3c9pF")
    equipo = []
    promedio = []
    liga = []
    
    for span in span_elements:
        equipo.append(span.text)
    league = soup.find_all("td", {"scope": "row", "class": "col-group-end-2UJpJVwW number-aY5arzrB align-left-3L2SU-Mk is-table-pinned-1WfPW2jT"})

    for td in league:
        liga.append(td.text)

    avg = soup.find_all("td", {"scope": "row","data-col":14,"class": "col-group-start-sa9unvY0 number-aY5arzrB align-right-3nN_D3xs is-table-pinned-1WfPW2jT"})
    # Imprimir los datos
    for dato in avg:
        promedio.append(dato.text)   
    df = pd.DataFrame({"EQUIPO": equipo, "LIGA":liga, "AVERAGE":promedio})
    df.AVERAGE = df.AVERAGE.astype(float)
    return df

def records():
    fecha = datetime.today().strftime("%Y-%m-%d")
    session = HTMLSession()
    url = f'https://www.mlb.com/standings/mlb/{fecha}'
    response = session.get(url)
    response.html.render()
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
    df_recor = df_recor.head(30)
    return df_recor
promedio = equipo_avg()
posiciones = records()
print(promedio)
print(posiciones)
