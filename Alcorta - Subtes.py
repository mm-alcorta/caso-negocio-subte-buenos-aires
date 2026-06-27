#----------------------------------------
# Librerias
#----------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
sns.set_theme(style="whitegrid")

#----------------------------------------
# Carga de datos 
#----------------------------------------

cronograma = pd.read_csv("cronograma-invierno.csv", sep=";", encoding="latin1")
demanda = pd.read_csv("historico_2018.csv", sep=",", encoding="utf-8")
boleto = pd.read_csv("registro-historico-del-precio-del-boleto.csv", sep=",", encoding="utf-8")

#---------------------------------------
# Análisis exploratorio de datos (EDA)
#---------------------------------------


# Identificación de registros duplicados en cada dataset
print("\n--- DUPLICADOS ---")
print("Demanda:", demanda.duplicated().sum())
print("Cronograma:", cronograma.duplicated().sum())
print("Boleto:", boleto.duplicated().sum())

# Eliminación de registros duplicados
cronograma = cronograma.drop_duplicates()
boleto = boleto.drop_duplicates()
demanda = demanda.drop_duplicates()

# Estandarización del formato de las variables de texto
demanda["linea"] = demanda["linea"].astype(str).str.lower().str.strip()
cronograma["LINEA"] = cronograma["LINEA"].astype(str).str.strip()
cronograma["DIA"] = cronograma["DIA"].astype(str).str.strip()

# Revisión de valores faltantes
print("\n--- VALORES NULOS ---")
print("\nDemanda:")
print(demanda.isnull().sum())

print("\nCronograma:")
print(cronograma.isnull().sum())

print("\nBoleto:")
print(boleto.isnull().sum())

# Conversión de fechas y eliminación de registros con fechas inválidas
demanda["fecha"] = pd.to_datetime(
    demanda["fecha"], errors="coerce"
    )
demanda = demanda.dropna(subset=["fecha"])

# Filtrado de la demanda correspondiente al período marzo-noviembre de 2018
demanda_2018 = demanda.loc[
    (demanda["fecha"] >= "2018-03-01") &
    (demanda["fecha"] <= "2018-11-30")
].copy()

# Selección de registros del cronograma correspondientes al año 2018
cronograma["PERIODO"] = pd.to_numeric(
    cronograma["PERIODO"],
    errors="coerce"
)
cronograma = cronograma[
    cronograma["PERIODO"] == 2018
].copy()

# Filtrado de las tarifas del boleto para el mismo período analizado
boleto = boleto[
    (boleto["año"] == 2018) &
    (boleto["mes_numero"].between(3, 11))
].copy()

#------------------------------------------------
# Configuración general para todos los gráficos
#------------------------------------------------

# Definición del estilo visual utilizado en las visualizaciones
plt.rcParams["font.family"] = "Segoe UI"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.titleweight"] = "semibold"
plt.rcParams["axes.labelsize"] = 10
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10

#-----------------------------------------
# Limpieza y transformación de los datos
#-----------------------------------------

# Conversión de la demanda a formato numérico
demanda_2018["total"] = pd.to_numeric(
    demanda_2018["total"],
    errors="coerce"
)

# Eliminación de valores nulos y demandas negativas o iguales a cero
demanda_2018 = demanda_2018.dropna(subset=["total", "linea"])
demanda_2018 = demanda_2018[demanda_2018["total"] > 0]

#--------------------------------
# Detección de valores atípicos
#--------------------------------

# Cálculo del rango intercuartílico (IQR)
Q1 = demanda_2018["total"].quantile(0.25)
Q3 = demanda_2018["total"].quantile(0.75)
IQR = Q3 - Q1

# Definición de límites para identificar outliers
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

# Identificación de registros atípicos sin eliminarlos
outliers = demanda_2018[
    (demanda_2018["total"] < limite_inferior) |
    (demanda_2018["total"] > limite_superior)
]

# Resumen de los valores extremos detectados
print("\n--- ANÁLISIS DE OUTLIERS ---")
print(f"Cantidad de outliers: {len(outliers)}")
print(
    f"Porcentaje: {len(outliers) / len(demanda_2018) * 100:.2f}%"
)

print("\nResumen estadístico de los outliers:")
print(outliers["total"].describe())

# Visualización de los registros con mayor demanda
print("\n20 registros con mayor demanda:")
print(
    demanda_2018[
        ["fecha", "linea", "estacion", "total"]
    ]
    .sort_values("total", ascending=False)
    .head(20)
)

# Boxplot para observar la distribución y los valores extremos

plt.figure(figsize=(10,4))
sns.boxplot(
    x=demanda_2018["total"],
    color="yellow"
)
plt.title("Distribución de la demanda y valores extremos (Marzo - Noviembre 2018)")
plt.xlabel("Pasajeros")
plt.tight_layout()
plt.show()

#----------------------------------
# Creación de variables derivadas
#----------------------------------

# Generación de la variable mes
demanda_2018["mes"] = demanda_2018["fecha"].dt.to_period("M").astype(str)

# Diccionario para traducir los días de la semana al español
dias_es = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Creación de la variable día de la semana
demanda_2018["dia_semana"] = (
    demanda_2018["fecha"]
    .dt.day_name()
    .map(dias_es)
)

demanda_2018 = demanda_2018.dropna(subset=["dia_semana"])

#--------------------------------------
# Normalización de la variable total
#--------------------------------------

# Escalamiento de la demanda al rango entre 0 y 1
scaler = MinMaxScaler()

demanda_2018["total_normalizado"] = scaler.fit_transform(
    demanda_2018[["total"]]
)

# Resumen descriptivo de la nueva variable
print("\nVariable normalizada creada: total_normalizado")
print("\nResumen de la variable normalizada:")
print(demanda_2018["total_normalizado"].describe())
print(
    "\nRango de la variable normalizada:",
    demanda_2018["total_normalizado"].min(),
    "a",
    demanda_2018["total_normalizado"].max()
)

# Histograma de la distribución normalizada
fig, ax = plt.subplots(figsize=(8,4))
sns.histplot(
    demanda_2018["total_normalizado"],
    bins=30,
    color="gold",
    ax=ax
)

ax.set_xlim(0, 1)
ax.set_title("Distribución de la demanda normalizada (Marzo - Noviembre 2018)")
ax.set_xlabel("Total normalizado")
ax.set_ylabel("Frecuencia")
ax.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.show()


# Distribución porcentual por intervalos
frecuencias = (
    pd.cut(
        demanda_2018["total_normalizado"],
        bins=10
    )
    .value_counts(normalize=True)
    .sort_index()
    * 100
)

# Visualización del porcentaje de observaciones en cada intervalo de la variable normalizada
print("\nDistribución porcentual:")
for intervalo, porcentaje in frecuencias.items():
    print(f"{intervalo}: {porcentaje:.2f}%")

#-----------------------------------
# Exportación de los datos limpios
#-----------------------------------

# Guardado de los datasets finales para su posterior análisis en Power BI
demanda_2018.to_csv(
    "demanda_2018_limpia.csv",
    index=False,
    encoding="utf-8-sig"
)

cronograma.to_csv(
    "cronograma_limpio.csv",
    index=False,
    encoding="utf-8-sig"
)

boleto.to_csv(
    "boleto_limpio.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nDatasets limpios exportados correctamente.")

#-------------------------------------------
# Estadística descriptiva y visualización
#-------------------------------------------

# Cálculo de medidas descriptivas de la demanda
print("\n--- ESTADÍSTICA DEMANDA ---")
print("Media:", round(demanda_2018["total"].mean(), 2))
print("Mediana:", round(demanda_2018["total"].median(), 2))
print("STD:", round(demanda_2018["total"].std(), 2))

# Agrupación de pasajeros por mes
demanda_mensual = (
    demanda_2018
    .groupby("mes")["total"]
    .sum()
    .sort_index()
)

meses = [
    "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre",
    "Octubre", "Noviembre"
]

# Gráfico de líneas de la evolución mensual de pasajeros
plt.figure(figsize=(12,10))
plt.plot(
    meses,
    demanda_mensual.values,
    color="gold",
    marker="o",
    linewidth=2
)

# Etiquetas con la cantidad de pasajeros en millones
for x, y in zip(meses, demanda_mensual.values):
    plt.annotate(
        f"{y/1e6:.1f} M",
        (x, y),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=9
    )

plt.title("Evolución mensual de la demanda (Marzo - Noviembre 2018)")
plt.ylabel("Pasajeros")
plt.xlabel("Meses")
plt.xticks(rotation=0)
plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda x, p: f"{x/1e6:.0f} M")
)
plt.tight_layout()
plt.subplots_adjust(bottom=0.12)
plt.show()

# Total de pasajeros analizados en el período
print(
    f"\nTotal de pasajeros analizados: "
    f"{demanda_2018['total'].sum()/1e6:.1f} millones"
)

#-------------------------------------------
# Distribución de la demanda según el día
#-------------------------------------------

# Agrupación y suma de pasajeros según el día de la semana
demanda_dia = (
    demanda_2018.groupby("dia_semana")["total"]
    .sum()
    .sort_values(ascending=False)
)

# Gráfico de barras horizontales de la demanda por día
fig, ax = plt.subplots(figsize=(10,5))
demanda_dia.plot(
    kind="barh",
    color="yellow",
    ax=ax
)

ax.invert_yaxis()
plt.xlim(0, demanda_dia.max()*1.15)
plt.title("Distribución de la demanda según el día (Marzo - Noviembre 2018)")
plt.xlabel("Pasajeros")
plt.ylabel("Días")

ax.xaxis.set_major_formatter(
    FuncFormatter(lambda x, p: f"{x/1e6:.0f} M")
)

for i, valor in enumerate(demanda_dia):
    ax.text(
        valor + demanda_dia.max()*0.005,
        i,
        f"{valor/1e6:.1f} M",
        va="center"
    )

plt.tight_layout()
plt.show()

#---------------------------------------
# Distribución de pasajeros por línea
#---------------------------------------

# Agrupación de pasajeros por línea de subte
pasajeros_linea = (
    demanda_2018.groupby("linea")["total"]
    .sum()
    .sort_values()
)

# Adaptación de los nombres de las líneas para la visualización
pasajeros_linea.index = [
    f"Línea {x[-1].upper()}"
    for x in pasajeros_linea.index
]

# Gráfico de barras horizontales de pasajeros por línea
plt.figure(figsize=(12,6))
bars = plt.barh(
    pasajeros_linea.index,
    pasajeros_linea.values,
    color="yellow",
    )

for bar in bars:
    valor = bar.get_width()

    plt.text(
        valor + pasajeros_linea.max()*0.005,
        bar.get_y() + bar.get_height()/2,
        f"{valor/1e6:.1f} M",
        va="center"
    )

plt.xlim(0, pasajeros_linea.max()*1.15)
plt.title("Distribución de pasajeros por línea (Marzo - Noviembre 2018)")
plt.xlabel("Pasajeros")
plt.ylabel("Línea")
plt.gca().xaxis.set_major_formatter(
    FuncFormatter(lambda x, p: f"{x/1e6:.0f} M")
)

plt.tight_layout()
plt.show()

#----------------------------------------
# Las 10 estaciones con mayor demanda
#----------------------------------------

# Selección de las diez estaciones con mayor cantidad de pasajeros
top_estaciones = (
    demanda_2018.groupby("estacion")["total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Gráfico de barras horizontales de las estaciones con mayor demanda
plt.figure(figsize=(12,6))
bars = plt.barh(
    top_estaciones.index[::-1],
    top_estaciones.values[::-1],
    color="yellow",
    )

for bar in bars:
    valor = bar.get_width()

    plt.text(
        valor + top_estaciones.max()*0.005,
        bar.get_y() + bar.get_height()/2,
        f"{valor/1e6:.1f} M",
        va="center"
    )

plt.xlim(0, top_estaciones.max()*1.15)
plt.title("Las 10 estaciones con mayor demanda (Marzo - Noviembre 2018)")
plt.xlabel("Pasajeros")
plt.ylabel("Estaciones")
plt.gca().xaxis.set_major_formatter(
    FuncFormatter(lambda x, p: f"{x/1e6:.0f} M")
)

plt.tight_layout()
plt.show()

#--------------------------------------------------------
# Cantidad de coches utilizados por línea según el día
#--------------------------------------------------------

# Verificación de los períodos disponibles en el cronograma
print(cronograma["PERIODO"].value_counts())
print(
    cronograma.groupby("LINEA")["PERIODO"]
    .unique()
)

# Homogeneización de los nombres de los tipos de día
cronograma["DIA"] = cronograma["DIA"].replace({
    "HABIL": "Lunes a Viernes",
    "SABADO": "Sábado",
    "DOMINGO": "Domingo"
})

# Construcción de la tabla utilizada para el mapa de calor
heatmap_data = pd.pivot_table(
    cronograma,
    index="DIA",
    columns="LINEA",
    values="TREN",
    aggfunc="count"
)

# Reordenamiento de los días de la semana
orden_dias = ["Lunes a Viernes", "Sábado", "Domingo"]
heatmap_data = heatmap_data.reindex(orden_dias)

# Mapa de calor de la cantidad de servicios por línea y tipo de día
plt.figure(figsize=(10,6))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".0f",
    cmap="YlGnBu",
    cbar_kws={"label": "Cantidad de coches"}
)

plt.title("Cantidad de coches utilizados por línea según el día (Marzo - Noviembre 2018)")
plt.xlabel("Línea")
plt.ylabel("Días")
plt.yticks(rotation=0)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#--------------------------------------
# Correlación entre tarifa y demanda
#--------------------------------------

# Conversión de la demanda mensual a DataFrame
demanda_mensual_df = demanda_mensual.reset_index()

# Construcción de una variable mes para unir ambos datasets
boleto["mes"] = (
    boleto["año"].astype(str) + "-" +
    boleto["mes_numero"].astype(int).astype(str).str.zfill(2)
)

# Integración de la información de demanda y tarifas
df_merge = demanda_mensual_df.merge(
    boleto,
    on="mes",
    how="inner"
)

# Cálculo del coeficiente de correlación entre precio y demanda
correlacion = df_merge["total"].corr(df_merge["precio"])

# Diccionario con los nombres de los meses en español
meses_es = {
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre"
}

# Creación de una variable categórica para mantener el orden cronológico
df_merge["nombre_mes"] = (
    pd.to_datetime(
        df_merge["mes"],
        format="%Y-%m"
    )
    .dt.month
    .map(meses_es)
)

orden_meses = [
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre"
]

df_merge["nombre_mes"] = pd.Categorical(
    df_merge["nombre_mes"],
    categories=orden_meses,
    ordered=True
)

# Gráfico de dispersión y línea de tendencia entre tarifa y demanda
plt.figure(figsize=(9,6))
sns.scatterplot(
    data=df_merge,
    x="precio",
    y="total",
    hue="nombre_mes",
    palette="viridis",
    s=120
)

sns.regplot(
    data=df_merge,
    x="precio",
    y="total",
    scatter=False,
    color="black",
    line_kws={"linewidth": 2}
)

plt.title("Correlación entre tarifa y demanda (Marzo - Noviembre 2018)")
plt.xlabel("Precio del boleto")
plt.ylabel("Pasajeros")
plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda x, p: f"{x/1e6:.0f} M")
)

plt.legend(
    title="Meses",
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)

plt.tight_layout()
plt.show()

# Interpretación del coeficiente de correlación obtenido
print(f"Correlación: {correlacion:.3f}")
if correlacion > 0.7:
    print("Existe una correlación positiva fuerte.")
elif correlacion > 0.3:
    print("Existe una correlación positiva moderada.")
elif correlacion > -0.3:
    print("Existe una correlación débil o nula.")
elif correlacion > -0.7:
    print("Existe una correlación negativa moderada.")
else:
    print("Existe una correlación negativa fuerte.")