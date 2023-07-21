import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import numpy as np
class equipos:
    def __init__(self) -> None:
        pass
    def equipo_avg(self):
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

    def stats(self):
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
        DF1 = self.equipo_avg()
        DF = pd.merge(MLB, DF1, on="TEAM", how="left")
        DF = DF[["TEAM","LIGA","WINS","LOSES","%WIN","%WIN-HC","%WIN-V","%CA","%CP","AVG_TEAM","RACHA","LAST-10"]]
        DF = DF.rename(columns={'%CA': 'SCORED/GAME', '%CP': 'ALLOWED/GAME'})
        return DF

    def resultados(self):
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

    def juegos_del_dia(self):
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
        if len(resultados)>0:
            comenzados = pd.DataFrame(resultados)
            comenzados["Titulo"] = comenzados['Titulo'].str.replace('Free Game of the Day', '')
            comenzados["Titulo"] = comenzados['Titulo'].str.replace('Top', 'Alta')
            return comenzados
        elif len(resultados1)>0:
            sin_empezar = pd.DataFrame(resultados1)        
            sin_empezar["Hora"] = sin_empezar['Hora'].str.replace('Free Game of the Day', '')
            return sin_empezar

    def lanzadores_del_dia(self):
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
        if df.empty == False:
            df['Era 1'] = df['Era 1'].str.replace(' ERA', '').str.replace('|', '')
            df['Era 2'] = df['Era 2'].str.replace(' ERA', '').str.replace('|', '')
            numericas = ["Era 1","Era 2"]
            for i in numericas:
                df[i] = df[i].astype(float)
            return df
        else:
            return "Ya comenzaron los juegos"

    def visitantes_homeclub(self):
        if self.lanzadores_del_dia() != "Ya comenzaron los juegos":
            df_concatenado = pd.concat([self.sin_empezar, self.lanzadores_del_dia()], axis=1)
            df_concatenado = df_concatenado[["Fecha","Hora","Visitante","Pitcher V","W-L V","Era 1","VS","Home Club","Pitchers HC","W-L HC","Era 2"]]
            visitante = df_concatenado[["Fecha","Hora","Visitante","Pitcher V","W-L V","Era 1"]]
            home_club = df_concatenado[["Fecha","Hora","Home Club","Pitchers HC","W-L HC","Era 2"]]
            return visitante, home_club
        else:
            return "Ya comenzaron los juegos"

    def get_team_logos(self):
        url = "https://www.mlb.com/team"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        team_logos = {}
        # buscamos todos los elementos de imagen en la página
        for img in soup.find_all("img"):
            # Solo considero las imágenes que son logotipos de equipos
            if "Team Logo" in img.get("alt", ""):
                team_name = img["alt"].replace(" Team Logo", "")
                logo_url = "https:" + img["src"]
                team_logos[team_name] = logo_url
        return team_logos
    
class jugadores:
    def __init__(self, url="https://www.espn.com/mlb/stats"):
        self.url = url

    def lideres(self, lado):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        stat_table = soup.find("div", class_=f"InnerLayout__child {lado}")
        stat_rows = stat_table.find_all("tr")
        rankin = list()
        players = list()
        teams = list()
        stats = list()
        for row in stat_rows:
            player_ranks = row.find_all('span', class_='leaderCell__playerRank')
            for rank in player_ranks:
                rankin.append(rank.text)
            player_images = row.find_all('img')
            for img in player_images:
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

    def get_batting_leaders(self):
        df = self.lideres("leftColumn")
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
        leaders_batting.append(lead_avg)
        leaders_batting.append(lead_hr)
        leaders_batting.append(lead_rbi)
        leaders_batting.append(lead_h)
        leaders_batting.append(lead_sb)
        return leaders_batting

    def get_pitching_leaders(self):
        df = self.lideres("rightColumn")
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
        leaders_pitching.append(lead_wins)
        leaders_pitching.append(lead_era)
        leaders_pitching.append(lead_sv)
        leaders_pitching.append(lead_k)
        leaders_pitching.append(lead_qs)
        return leaders_pitching