import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = 'browser'

consolas_dataset = pd.read_csv("C:/Users/dante/OneDrive/Escritorio/PYTHON/MODULO_3/PROYECTO_FINAL/DATA_SET_PF/Console_Data.csv",
    encoding='utf-8'
    ,na_values=['\\N']
)

scrapped_dataset = pd.read_csv("C:/Users/dante/OneDrive/Escritorio/PYTHON/MODULO_3/PROYECTO_FINAL/DATA_SET_PF/scrapped_data.csv",
    encoding='utf-8'
    ,na_values=['\\N']
)

print("\n")
print("--------TABLA CONSOLAS----------")
print(consolas_dataset)
consolas_dataset.info()
print("\n")
print("--------TABLA SCRAPPED----------")
print(scrapped_dataset)
scrapped_dataset.info()
print("\n")

print("--------SHAPE DE CONSOLAS----------")
print(consolas_dataset.shape)
print(consolas_dataset.dtypes)
print(consolas_dataset.head(10))
print(consolas_dataset.describe())
print(consolas_dataset.isna().sum())
print("\n")
print("--------SHAPE DE SCRAPPED----------")
print(scrapped_dataset.shape)
print(scrapped_dataset.dtypes)
print(scrapped_dataset.head(10))
print(scrapped_dataset.describe())
print(scrapped_dataset.isna().sum())
print("\n")

print("--------REVISAR DUPLICADOS----------")
print("Consolas:")
print(consolas_dataset.duplicated().sum())
print("Scrapped:")
print(scrapped_dataset.duplicated().sum())

#HISTOGRAMA DE CONSOLAS
plt.hist(consolas_dataset['Company'], bins=30, edgecolor='black', alpha=0.7)
plt.title('Total de Consolas por Compañía')
plt.xlabel('Compañías')
plt.ylabel('Cantidad de Consolas')
plt.show()

'''Cual seria la cantidad de consolas por compañía?
La compañía con más consolas es Nintendo, seguida por Sony y Microsoft. 
Otras compañías como Sega, Atari, SNK, NEC, Bandai, entre otras, tienen 
una cantidad menor de consolas en comparación con las tres principales.
'''


#MODA DE VENTAS POR GENERACIÓN
moda_por_gen = consolas_dataset.groupby("Gen")["Units sold (million)"].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan).reindex(consolas_dataset["Gen"].unique())
print("--- Moda de Ventas por Generación (Millones) ---")   
print(moda_por_gen.to_string())
print("\n")

#MEDIA DE VENTAS POR GENERACIÓN
media_company_gen = consolas_dataset.groupby("Gen")["Units sold (million)"].mean().reindex(consolas_dataset["Gen"].unique())
print("--- Media de Ventas por Generación (Millones) ---")
print(media_company_gen.to_string())
print("\n")

#MEDIANA DE VENTAS POR GENERACIÓN
mediana_por_gen = (
    consolas_dataset.groupby("Gen")["Units sold (million)"].median().reindex(consolas_dataset["Gen"].unique())
)
# Mostrar los valores numéricos en consola
print("--- Mediana de Ventas por Generación (Millones) ---")
print(mediana_por_gen.to_string())
plt.figure(figsize=(10, 5))
mediana_por_gen.plot(kind="bar", color="purple", edgecolor="black")
plt.title("Mediana de Unidades Vendidas por Generación")
plt.xlabel("Generación")
plt.ylabel("Mediana de Ventas (Millones de unidades)")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

'''¿Cuál es la mediana de ventas por generación?
La mediana de ventas por generación varía, con algunas generaciones como la 7ª y 8ª mostrando medianas más altas debido a la popularidad de consolas como PlayStation 4 y Xbox One. Otras generaciones, como la 5ª, 
tienen medianas más bajas, lo que refleja una menor cantidad de consolas exitosas en esa época. En general, la mediana de ventas por generación muestra una tendencia de crecimiento a lo largo del tiempo, aunque 
con algunas fluctuaciones dependiendo de la popularidad y el éxito de las consolas lanzadas en cada generación.
'''

#VENTAS DE HARDWARE POR NOMBRE DE CONSOLA
df_ordenado = consolas_dataset.sort_values(by="Units sold (million)", ascending=True)
plt.figure(figsize=(12, 10))
barras = plt.barh(
    df_ordenado["Console Name"],
    df_ordenado["Units sold (million)"],
    color="crimson",
    edgecolor="black",
)
for barra in barras:
    ancho = barra.get_width()
    plt.text(
        ancho + 1,  # Posición X ligeramente a la derecha del final de la barra
        barra.get_y() + barra.get_height() / 2,  # Posición Y centrada en la barra
        f"{ancho:.2f} M",  # Texto formateado
        va="center",
        ha="left",
        fontsize=9,
        fontweight="bold",
    )
plt.title(
    "Ventas de Hardware por Nombre de Consola (Millones de Unidades)",
    fontsize=14,
    fontweight="bold",
    pad=20,
)
plt.xlabel("Unidades vendidas (Millones)", fontsize=11, labelpad=10)
plt.ylabel("Nombre de la Consola", fontsize=11, labelpad=10)
plt.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

'''¿Cuál es la consola con más ventas?
La consola con más ventas es el Nintendo Entertainment System (NES), seguida por el Sony PlayStation 2 y 
el Microsoft Xbox. Otras consolas como el Sega Genesis, el Atari 2600 y el Commodore 64 tienen ventas 
menores en comparación con las principales.
'''

#PARTE 5 Requisitos de gráficos

#Gráfico 1: Matplotlib (Análisis de Dominio de Mercado)
plt.figure(figsize=(10, 6))
market_share = consolas_dataset.groupby("Company")["Units sold (million)"].sum().sort_values(ascending=False)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
bars = plt.bar(market_share.index, market_share.values, color=colors, edgecolor='black', alpha=0.9)
# Añadir etiquetas sobre las barras
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 15, f"{yval:.1f}M", ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("Volumen Total de Ventas de Hardware por Compañía (1972 - 2026)", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Fabricante / Compañía", fontsize=11, labelpad=10)
plt.ylabel("Unidades Vendidas (Millones)", fontsize=11, labelpad=10)
plt.ylim(0, market_share.max() * 1.15)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()


#Grafico 2 Seaborn (Análisis Estadístico de Dispersión y Rendimiento)
plt.figure(figsize=(12, 6))
# Ordenar cronológicamente las generaciones en el eje X
gen_order = sorted(consolas_dataset["Gen"].unique(), key=lambda x: int(''.join(filter(str.isdigit, x))))
sns.boxplot(data=consolas_dataset, x="Gen", y="Units sold (million)", hue="Gen", palette="vlag", legend=False, linewidth=1.5)
sns.stripplot(data=consolas_dataset, x="Gen", y="Units sold (million)", color="black", alpha=0.6, size=6, jitter=0.15)
plt.title("Dispersión y Distribución de Ventas de Hardware por Generación", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Generación Tecnológica", fontsize=11, labelpad=10)
plt.ylabel("Unidades Vendidas por Consola (Millones)", fontsize=11, labelpad=10)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

#Gráfico 3 Plotly (Análisis de Tendencias y Comparaciones)
top_10 = scrapped_dataset.nlargest(10, 'Units(m)')
fig = go.Figure(data=[
    go.Bar(
        x=top_10['Units(m)'],
        y=top_10['Game Name'],
        orientation='h',
        marker_color='teal',
        text=top_10['Units(m)'],
        textposition='outside'
    )
])
fig.update_layout(
    title='Top 10 Juegos Más Vendidos de la Historia',
    xaxis_title='Ventas (en millones)',
    yaxis_title='Juego',
    yaxis=dict(autorange="reversed"),
    template='plotly_white',
    margin=dict(l=150) 
)
fig.show()
'''¿Cuál es el juego más vendido de la historia?
el juego mas vendido seria el Wii sports con 82.9 millones de unidades vendidas.
'''



#Gráfico 4 Matplotlib (Análisis de Series Temporales)
scrapped_dataset['Release Date'] = pd.to_datetime(scrapped_dataset['Release Date'], errors='coerce', dayfirst=True)
df = scrapped_dataset.dropna(subset=['Release Date', 'Units(m)'])
scrapped_dataset['YearMonth'] = scrapped_dataset['Release Date'].dt.to_period('M')
monthly = scrapped_dataset.groupby('YearMonth')['Units(m)'].sum().reset_index()
monthly['YearMonth'] = monthly['YearMonth'].dt.to_timestamp()
monthly['MA_3'] = monthly['Units(m)'].rolling(window=3).mean()

plt.figure(figsize=(12,6))
plt.plot(monthly['YearMonth'], monthly['Units(m)'], label='Ventas mensuales')
plt.plot(monthly['YearMonth'], monthly['MA_3'], label='Promedio móvil (3 meses)', linestyle='--')
plt.title('Serie de tiempo: ventas de videojuegos')
plt.xlabel('Fecha')
plt.ylabel('Unidades (millones)')
plt.legend()
plt.grid()
plt.show()

'''
La pregunta eleccionada es:
¿Cuál es la consola con más ventas?

•	¿Por qué esta pregunta es relevante o interesante?
Es relevante porque nos permite identificar cuál ha sido la consola más exitosa en términos de ventas a lo largo de la historia,
lo que puede reflejar su popularidad, impacto en la industria y preferencia del consumidor. Esta información es valiosa para 
entender las tendencias del mercado y el éxito de diferentes fabricantes.

•	¿Qué columnas del dataset permiten responderla?
Las columnas relevantes para responder esta pregunta son "Console Name" y "Units sold (million)". 
La columna "Console Name" nos permite identificar el nombre de cada consola, mientras que la columna 
"Units sold (million)" nos proporciona la cantidad de unidades vendidas en millones, lo que es esencial 
para determinar cuál consola ha tenido más ventas.

•	¿Requiere comparar grupos? ¿Cuáles?
Sí, requiere comparar grupos, específicamente las diferentes consolas listadas en la columna "Console Name".
Comparar las ventas de cada consola nos permitirá identificar cuál ha sido la más vendida.

•	¿Tiene una dimensión temporal que puedas analizar?
Sí, aunque la pregunta se centra en la consola con más ventas, también se puede analizar 
la dimensión temporal al observar las ventas a lo largo de diferentes generaciones de consolas. 
Esto nos permitiría ver cómo han evolucionado las ventas de las consolas a lo largo del tiempo y si alguna generación ha tenido un impacto significativo en las ventas totales.

•	¿Qué tipo de gráfico comunicaría mejor la respuesta?
Un gráfico de barras horizontales sería ideal para comunicar la respuesta a esta pregunta, ya que permite 
comparar fácilmente las ventas de diferentes consolas.
'''