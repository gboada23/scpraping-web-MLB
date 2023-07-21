# USANDO PROGRAMACION MODULAR IMPORTAMOS LAS CLASSES DE EL ARCHIVO scrap.py
from scrap import equipos
from scrap import jugadores


# LLAMAMOS LA CLASE EQUIPOS Y SUS METODOS
teams = equipos()
stats_by_teams = teams.stats()
games_results = teams.resultados()
days_games = teams.juegos_del_dia()
days_pitchers = teams.lanzadores_del_dia()
before_game = teams.visitantes_homeclub()

# LLAMAMOS LAS CLASES JUGADORES CON SUS METODOS
lideres_bateadores = jugadores().get_batting_leaders()
lideres_lanzadores = jugadores().get_pitching_leaders()

# OBTENEMOS CADA DF DE LIDERATO INDIVIDUAL para los bateadores
lead_avg = lideres_bateadores[0]
lead_hr= lideres_bateadores[1]
lead_rbi = lideres_bateadores[2]
lead_hits = lideres_bateadores[3]
lead_sb = lideres_bateadores[4]

# OBTENEMOS CADA DF DE LIDERATO INDIVIDUAL para los lanzadores
# cada variable creada  posee un DF de 5 filas que contiene los lideres de cada estadistica
lead_wins = lideres_lanzadores[0]
lead_era = lideres_lanzadores[1]
lead_sv = lideres_lanzadores[2]
lead_k = lideres_lanzadores[3]
lead_qs = lideres_lanzadores[4]

# aqui iremos realizando analisis sobre la marcha
