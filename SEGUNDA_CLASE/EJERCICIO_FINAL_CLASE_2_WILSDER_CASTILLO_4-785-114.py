import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json as js
import plotly.io as pio
pio.renderers.default = 'browser'


airports_dataset = pd.read_csv("C:/Users/dante/Downloads/travel/DATA/airports_data.csv",
    encoding='utf-8'
    ,na_values=['\\N']
)

bookings_dataset = pd.read_csv("C:/Users/dante/Downloads/travel/DATA/bookings.csv",
    encoding='utf-8'
    ,na_values=['\\N']
)
bookings_dataset['book_date'] = pd.to_datetime(bookings_dataset['book_date'], utc=True)

tickets_flights_dataset = pd.read_csv("C:/Users/dante/Downloads/travel/DATA/ticket_flights.csv",
    encoding='utf-8'
    ,na_values=['\\N']
)

flights_dataset = pd.read_csv("C:/Users/dante/Downloads/travel/DATA/flights.csv",
    encoding='utf-8',
    na_values=['\\N']
)

aircraft_dataset = pd.read_csv("C:/Users/dante/Downloads/travel/DATA/aircrafts_data.csv",
    encoding='utf-8',
    na_values=['\\N']
)

print("--------TABLA airports----------")
print(airports_dataset)
print("--------TABLA BOOKINGS----------")
print(bookings_dataset)
print("--------TABLA TICKETS----------")
print(tickets_flights_dataset)
print("--------TABLA FLIGHTS----------")
print(flights_dataset)
print("--------TABLA AIRCRAFTS----------")
print(aircraft_dataset)

'''
Parte A — Matplotlib (25 pts)
A1 (10 pts)
Crea un gráfico de barras vertical que muestre la cantidad de vuelos por aircraft_code.
Requisitos:

Ordena de mayor a menor
Muestra el valor encima de cada barra
Elimina los bordes superior y derecho
Pon un título descriptivo

'''

tabla_aircraft = aircraft_dataset.sort_values(by='range', ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(tabla_aircraft['aircraft_code'], tabla_aircraft['range'], color='#99d4fe')
ax.set_title('Cantidad de Vuelos por Modelo de Aeronave', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Código de Aeronave', fontsize=14, fontweight='bold')
ax.set_ylabel('Cantidad de Vuelos', fontsize=14, fontweight='bold')
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=10)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.show()


'''
A2 (15 pts)
Crea un histograma de los montos de reserva (total_amount en bookings).

Requisitos:

Usa bins=40
Agrega una línea vertical con el promedio
Agrega otra línea vertical con la mediana (usa un color diferente)
Incluye leyenda que identifique ambas líneas
Añade grid suave en el eje Y'''

tabla_bookings = bookings_dataset
mean_amount = tabla_bookings['total_amount'].mean()
median_amount = tabla_bookings['total_amount'].median()
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(tabla_bookings['total_amount'], bins=40, color='#996d57', edgecolor='white', alpha=0.8)
ax.axvline(mean_amount, color='red', linestyle='--', linewidth=2,label=f'Mean: {mean_amount:,.2f}')
ax.axvline(median_amount, color='green', linestyle='-', linewidth=2,label=f'Median: {median_amount:,.2f}')
ax.set_title('Distribucion del Total de Bookings', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Total x cantidad', fontsize=12)
ax.set_ylabel('Rango de Bookings', fontsize=12)
ax.grid(axis='y', linestyle=':', alpha=0.6)
ax.legend(fontsize=11, loc='upper right')
plt.tight_layout()
plt.show()


'''
Parte B — Seaborn (25 pts)
B1 (10 pts)
Usa sns.boxplot para comparar la distribución de total_amount en bookings por mes.
Pista: necesitas crear una columna mes con dt.month_name() o dt.to_period('M').
'''

tabla_bookings['book_date'] = pd.to_datetime(bookings_dataset['book_date'])
tabla_bookings['month'] = tabla_bookings['book_date'].dt.month_name()

plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")
sns.boxplot(
    data=tabla_bookings,
    x='month',
    y='total_amount',
    order=tabla_bookings['month'].value_counts().index,
    palette='Set2'
)
plt.title('Distribucion Mensual por Cantidad de Reservas', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Meses', fontsize=12)
plt.ylabel('Cantidad Total', fontsize=12)
plt.tight_layout()
plt.show()

'''B2 (15 pts)
Usa sns.barplot para mostrar el precio promedio de ticket por fare_conditions.
Luego superpón en el mismo gráfico un sns.stripplot para ver los puntos individuales.
Pista: ambos deben usar ax= para compartir el mismo eje.'''

tabla_tickets = tickets_flights_dataset
fig, ax = plt.subplots(figsize=(10, 6))
sns.set_theme(style="whitegrid")
sns.barplot(
    data=tabla_tickets,
    x='fare_conditions',
    y='amount',
    ax=ax,
    alpha=0.4,
    ci=None,
    palette='Blues_d'
)

sns.stripplot(
    data=tabla_tickets,
    x='fare_conditions',
    y='amount',
    ax=ax,
    jitter=0.25,
    size=4,
    alpha=0.7,
    palette='deep'
)
ax.set_title('Distribucion de Precios por Tipo de Tarifa', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Tipo de vuelo segun Tarifa  ', fontsize=12)
ax.set_ylabel('Cantidad de Tickets', fontsize=12)
plt.tight_layout()
plt.show()

'''
C1 (15 pts)
Crea un px.scatter interactivo que muestre:

Eje X: flight_id
Eje Y: amount
Color por fare_conditions
En el hover debe aparecer también el ticket_no
Título descriptivo
'''

fig = px.scatter(
    tabla_tickets,
    x='flight_id',
    y='amount',
    color='fare_conditions',
    hover_data={'ticket_no': True, 'flight_id': True, 'amount': True, 'fare_conditions': True},
    title='Cantidad de Tickets vs. Condiciones de Tarifa',
    labels={
        'flight_id': 'ID del Vuelo',
        'amount': 'Cantidad de Tickets',
        'fare_conditions': 'Tipo de Tarifa',
        'ticket_no': 'Numero de Ticket'
    },
    template='plotly_white'
)

fig.update_layout(
    title_font_size=16,
    title_font_family='Arial',
    hoverlabel=dict(font_size=12)
)
fig.show()



'''C2 (10 pts)
Crea un px.line con los ingresos diarios de bookings (agrupa por día, suma total_amount).
Agrega markers=True y personaliza el color de la línea.'''

tabla_bookings['book_date'] = pd.to_datetime(tabla_bookings['book_date'])
tabla_bookings['dia'] = tabla_bookings['book_date'].dt.date
ingresos_diarios = tabla_bookings.groupby('dia')['total_amount'].sum().reset_index()
fig = px.line(
    ingresos_diarios,
    x='dia',
    y='total_amount',
    markers=True,
    title='Tendencia de Ingresos Diarios por Reservas',
    labels={
        'dia': 'Fecha de Reserva',
        'total_amount': 'Ingresos Totales ($)'
    },
    template='plotly_white'
)
fig.update_traces(
    line_color='#0284c7',       
    marker=dict(
        size=8, 
        color='#f43f5e',       
        line=dict(width=1, color='white')
    )
)
fig.show()


'''
D1 (25 pts)
Toma uno de los gráficos que ya hiciste (cualquiera de las partes A, B o C) y rehazlo aplicando todos los principios de diseño vistos en clase:

 Título que dice la conclusión (no solo el tema)
 Color con propósito (destacar un valor o diferenciar categorías)
 Al menos una anotación que señale el punto más importante
 Eliminación de bordes / ruido innecesario
 Fuente de datos en el gráfico (puede ser en el subtítulo o pie)
En la celda de texto debajo explica qué decisiones tomaste y por qué.'''

mean_amount = tabla_bookings['total_amount'].mean()
median_amount = tabla_bookings['total_amount'].median()

fig, ax = plt.subplots(figsize=(11, 6.5), facecolor='white')
n, bins, patches = ax.hist(tabla_bookings['total_amount'], bins=40, 
                           color='#94a3b8', edgecolor='white', alpha=0.85)
ax.axvline(median_amount, color='#1e3a8a', linestyle='-', linewidth=2.5, 
           label=f'Mediana: ${median_amount:,.0f}')
ax.axvline(mean_amount, color='#b91c1c', linestyle=':', linewidth=2.5, 
           label=f'Promedio: ${mean_amount:,.0f}')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#cbd5e1')
ax.grid(axis='y', linestyle='--', alpha=0.4, color='#cbd5e1')
ax.annotate(
    'La gran mayoría de las reservas se concentran\npor debajo de los $50,000.',
    xy=(25000, max(n) * 0.7),
    xytext=(85000, max(n) * 0.8),
    arrowprops=dict(arrowstyle="->", color='#475569', lw=1.5, connectionstyle="arc3,rad=-0.2"),
    fontsize=11, color='#334155', fontweight='medium'
)
plt.suptitle('La mitad de las reservas se realizan por montos menores a los $40,000', 
             fontsize=15, fontweight='bold', color='#0f172a', x=0.125, ha='left')
ax.set_title('Distribución de montos totales en reservas de vuelos (total_amount) con asimetría positiva.', 
             fontsize=11, color='#64748b', pad=20, loc='left')
ax.set_xlabel('Monto Total de la Reserva (USD)', fontsize=11, color='#334155', labelpad=10)
ax.set_ylabel('Frecuencia de Reservas', fontsize=11, color='#334155', labelpad=10)
plt.figtext(0.125, -0.02, "Fuente: Base de datos histórica del sistema de reservas de aerolíneas (bookings).", 
            fontsize=9, style='italic', color='#64748b')
ax.legend(loc='upper right', frameon=False, fontsize=11)
plt.tight_layout()
plt.show()