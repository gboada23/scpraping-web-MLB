import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def lideres(lado):
    url = "https://www.espn.com/mlb/stats"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    stat_table = soup.find("div", class_=f"InnerLayout__child {lado}")
    stat_rows = stat_table.find_all("tr")
    rankin = list()
    players = list()
    teams = list()
    stats = list()
    for row in stat_rows:
        # Encuentra todos los elementos 'span' con la clase 'leaderCell__playerRank'
        player_ranks = row.find_all('span', class_='leaderCell__playerRank')
        # Ahora puedes hacer algo con cada player_rank en player_ranks
        for rank in player_ranks:
            rankin.append(rank.text)  # Imprime el texto del elemento
        player_images = row.find_all('img')
        # Para cada imagen en las imágenes de los jugadores
        for img in player_images:
        # Imprime el valor del atributo 'title'
            players.append(img.get('title'))
        teams_names = row.find_all('span', class_="pl2 n10 leaderCell__teamAbbrev")

        for team in teams_names:
            teams.append(team.text)
            
        stats_players = row.find_all("td", class_= "Table__TD")
        for stat in stats_players:
            stats.append(stat.text)
            
    stats = [item for item in stats if item.replace('.', '', 1).isdigit()]
    df = pd.DataFrame({"Rank":rankin, "Playes":players, "Teams":teams, "stats":stats})
    return df

def get_batting_leaders():
    df = lideres("leftColumn")
    dfs = np.array_split(df, 5)
    leaders_batting = []
    lead_avg = dfs[0]
    lead_avg = lead_avg.rename(columns={'stats': 'AVG'})
    lead_hr = dfs[1]
    lead_hr = lead_hr.rename(columns={'stats': 'HR'})
    lead_rbi = dfs[2]
    lead_rbi = lead_rbi.rename(columns={'stats': 'RBI'})
    lead_h = dfs[3]
    lead_h = lead_h.rename(columns={'stats': 'HITS'})
    lead_sb = dfs[4]
    lead_sb = lead_sb.rename(columns={'stats': 'SB'})
    # Añadir las variables a la lista
    leaders_batting.append(lead_avg)
    leaders_batting.append(lead_hr)
    leaders_batting.append(lead_rbi)
    leaders_batting.append(lead_h)
    leaders_batting.append(lead_sb)
    return leaders_batting

def get_pitching_leaders():
    df = lideres("rightColumn")
    dfs = np.array_split(df, 5)
    leaders_pitching = []
    lead_wins = dfs[0]
    lead_wins = lead_wins.rename(columns={'stats': 'WINS'})
    lead_era = dfs[1]
    lead_era = lead_era.rename(columns={'stats': 'ERA'})
    lead_sv = dfs[2]
    lead_sv = lead_sv.rename(columns={'stats': 'SV'})
    lead_k = dfs[3]
    lead_k = lead_k.rename(columns={'stats': 'K'})
    lead_qs = dfs[4]
    lead_qs = lead_qs.rename(columns={'stats': 'QS'})
    # Añadir los df a la lista
    leaders_pitching.append(lead_wins)
    leaders_pitching.append(lead_era)
    leaders_pitching.append(lead_sv)
    leaders_pitching.append(lead_k)
    leaders_pitching.append(lead_qs)
    return leaders_pitching

print(get_batting_leaders())
print(get_pitching_leaders())
