import requests
import json
import pandas as pd

url = "https://covid19.patria.org.ve/api/v1/summary"

response = requests.get(url)

if response.status_code == 200:
    print("Conexión realizada con éxito")
else:
    print("Error al conectar a la API")

api = json.loads(response.text)

# Desnormalizar el diccionario "ByState"
df_states = pd.json_normalize(api[3])
"""
# Agregar la fila "Count" como otra fila en el DataFrame
df_states = df_states.append(api['Count'], ignore_index=True)

# Concatenar el DataFrame "ByGender" con el DataFrame de estados
df = pd.concat([pd.DataFrame(api['ByGender'], index=[0]), df_states], axis=1)

# Eliminar columnas innecesarias
df = df[['male', 'female', 'Confirmed', 'Recovered', 'Deaths', 'Active']]
"""
print(df_states)
