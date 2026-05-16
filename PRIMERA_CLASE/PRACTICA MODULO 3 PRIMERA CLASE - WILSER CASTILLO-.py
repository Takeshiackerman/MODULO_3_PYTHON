import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json

aeropuertos_dataset = pd.read_csv("C:/Users/dante/Downloads/travel/DATA/airports_data.csv",
    encoding='utf-8'
    ,na_values=['\\N']
)

vuelos_dataset = pd.read_csv("C:/Users/dante/Downloads/travel/DATA/flights.csv",
    encoding='utf-8',
    na_values=['\\N']
)


print(aeropuertos_dataset)
print(vuelos_dataset)

vuelos_aeropuerto=vuelos_dataset.merge(
    aeropuertos_dataset,
    left_on='arrival_airport',
    right_on='airport_code',
    how='left'
)

print("-------------------------------------------------------------------------------")

print(vuelos_aeropuerto)

print("----------------------------------¿Cuáles son los 10 aeropuertos de destino con más vuelos llegados?-- bar chart horizontal --------------------------------------------")
def obtener_nombre_en(nombre_json):
    try:
        return json.loads(nombre_json)['en']
    except:
        return nombre_json

top_destinos = vuelos_aeropuerto['arrival_airport'].value_counts().head(10).reset_index()
top_destinos.columns = ['airport_code', 'vuelos']

top_destinos = top_destinos.merge(aeropuertos_dataset[['airport_code', 'airport_name']], on='airport_code')
top_destinos['nombre_limpio'] = top_destinos['airport_name'].apply(obtener_nombre_en)
print(top_destinos)

plt.figure(figsize=(10, 6))
plt.barh(top_destinos['nombre_limpio'], top_destinos['vuelos'], color='skyblue', edgecolor='navy')
plt.xlabel('Cantidad de Vuelos Llegados', fontsize=12)
plt.title('Top 10 Aeropuertos de Destino con más Tráfico', fontsize=14)
plt.gca().invert_yaxis()  
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.show()

print("-----------------------------------¿Cuántos minutos de retraso tuvo cada vuelo al llegar? histogram--------------------------------------------")

vuelos_dataset['actual_arrival'] = pd.to_datetime(vuelos_dataset['actual_arrival'])
vuelos_dataset['scheduled_arrival'] = pd.to_datetime(vuelos_dataset['scheduled_arrival'])

vuelos_dataset['retraso_minutos'] = (vuelos_dataset['actual_arrival'] - vuelos_dataset['scheduled_arrival']).dt.total_seconds() / 60

plt.figure(figsize=(10, 6))
sns.histplot(vuelos_dataset['retraso_minutos'].dropna(), bins=100, color='teal', kde=True)
plt.axvline(0, color='red', linestyle='--', label='A tiempo')
plt.title('Distribución de Retrasos al Llegar (Todos los vuelos)', fontsize=14)
plt.xlabel('Minutos de Retraso (Valores negativos = Llegada anticipada)', fontsize=12)
plt.ylabel('Cantidad de Vuelos', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.show()


print("--------------------------------------¿Cuál es el promedio de retraso por aeropuerto de destino? bar chart-----------------------------------------")


#Que las fechas sean datetime y calcular el retraso
vuelos_aeropuerto['actual_arrival'] = pd.to_datetime(vuelos_aeropuerto['actual_arrival'])
vuelos_aeropuerto['scheduled_arrival'] = pd.to_datetime(vuelos_aeropuerto['scheduled_arrival'])
vuelos_aeropuerto['delay'] = (vuelos_aeropuerto['actual_arrival'] - vuelos_aeropuerto['scheduled_arrival']).dt.total_seconds() / 60


def clean_name(x):
    try: return json.loads(x.replace("'", '"'))['en']
    except: return x

vuelos_aeropuerto['airport_name_en'] = vuelos_aeropuerto['airport_name'].apply(clean_name)

promedio_retraso = vuelos_aeropuerto.groupby('airport_name_en')['delay'].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 7))
promedio_retraso.plot(kind='bar', color='salmon', edgecolor='black')
plt.title('Top 10 Aeropuertos con Mayor Promedio de Retraso al Llegar', fontsize=14)
plt.ylabel('Promedio de Minutos de Retraso', fontsize=12)
plt.xlabel('Aeropuerto de Destino', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

print("-----------------------------------¿A qué hora del día llegan más vuelos? histogram--------------------------------------------")


vuelos_dataset['scheduled_arrival'] = pd.to_datetime(vuelos_dataset['scheduled_arrival'])
vuelos_dataset['hora_llegada'] = vuelos_dataset['scheduled_arrival'].dt.hour


plt.figure(figsize=(12, 6))
sns.histplot(vuelos_dataset['hora_llegada'], bins=24, kde=True, color='orange', edgecolor='black')
plt.title('Distribución de Llegadas por Hora del Día', fontsize=15)
plt.xlabel('Hora del Día (Formato 24h)', fontsize=12)
plt.ylabel('Cantidad de Vuelos', fontsize=12)
plt.xticks(range(0, 24))  # Mostrar todas las horas en el eje X
plt.grid(axis='y', alpha=0.3)
plt.show()

print("---------------------------------¿Cuáles son las rutas más frecuentes? bar chart----------------------------------------------")

vuelos_dataset['ruta'] = vuelos_dataset['departure_airport'] + ' ➔ ' + vuelos_dataset['arrival_airport']
top_rutas = vuelos_dataset['ruta'].value_counts().head(10)

plt.figure(figsize=(12, 6))
top_rutas.plot(kind='bar', color='mediumpurple', edgecolor='black')
plt.title('Top 10 Rutas con Mayor Frecuencia de Vuelos', fontsize=15)
plt.xlabel('Ruta (Aeropuerto Origen ➔ Destino)', fontsize=12)
plt.ylabel('Cantidad de Vuelos Realizados', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()  