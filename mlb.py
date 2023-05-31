import requests
from bs4 import BeautifulSoup
import pandas as pd

# Definir la URL de la página web a scrapear
url = 'https://www.baseball-reference.com/'

# Hacer una petición HTTP GET a la URL
response = requests.get(url)

# Parsear el contenido HTML de la página web con BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Obtener las estadísticas de los equipos
team_stats = soup.find_all('div', {'class': 'standings__table--expanded'})

# Obtener las estadísticas de los jugadores
player_stats = soup.find_all('table', {'id': 'players_standard_batting'})

# Obtener las estadísticas de los lanzadores
pitcher_stats = soup.find_all('table', {'id': 'players_standard_pitching'})

# Obtener las clasificaciones de la liga
league_standings = soup.find_all('table', {'id': 'standings-upto-AL'})

# Obtener los resultados de los juegos
game_results = soup.find_all('table', {'class': 'teams'})

print(player_stats)

# Convertir los datos obtenidos a un formato adecuado para el análisis
"""team_stats_df = pd.read_html(str(team_stats))[0]
player_stats_df = pd.read_html(str(player_stats))[0]
pitcher_stats_df = pd.read_html(str(pitcher_stats))[0]
league_standings_df = pd.read_html(str(league_standings))[0]
game_results_df = pd.read_html(str(game_results))[0]

# Imprimir los resultados
print(team_stats_df.head())
print(player_stats_df.head())
print(pitcher_stats_df.head())
print(league_standings_df.head())
print(game_results_df.head())"""
