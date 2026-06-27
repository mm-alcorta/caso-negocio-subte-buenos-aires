# Análisis de la Demanda del Subte de la Ciudad de Buenos Aires (Marzo-Noviembre 2018)

Este proyecto fue desarrollado como **Trabajo Final** para la certificación en **Data Analytics de Digital House**.

El objetivo consistió en preparar, limpiar, transformar y analizar datos históricos de la red de Subterráneos de la Ciudad Autónoma de Buenos Aires correspondientes al período **marzo–noviembre de 2018**, con el propósito de identificar patrones de movilidad, analizar el comportamiento de la demanda y desarrollar un dashboard interactivo que facilitara la interpretación de los resultados.

Para ello se utilizó **Python** en las etapas de extracción, limpieza, transformación y análisis exploratorio de datos (ETL y EDA), mientras que **Power BI** se empleó para el modelado de datos y la construcción del dashboard.

---

# Contenido del repositorio

* **`notebooks/`** – Código fuente en Python (`.ipynb`) correspondiente al proceso de limpieza, transformación y análisis exploratorio de datos.
* **`dashboard/`** – Archivo de Power BI (`.pbix`) con el dashboard interactivo.
* **`data/`** – Datasets procesados utilizados para el análisis.
* **`reports/`** – Informe técnico con la metodología, resultados, conclusiones y recomendaciones del proyecto.

---

# Tecnologías utilizadas

* **Python**

  * Pandas
  * Matplotlib
  * Seaborn
  * Scikit-learn

* **Power BI**

  * Modelado de datos
  * Medidas DAX
  * Visualizaciones interactivas

### Fuentes de datos

Se trabajó con tres conjuntos de datos abiertos de la Ciudad Autónoma de Buenos Aires:

1. Demanda histórica de pasajeros por estación y molinete.
2. Cronograma operativo invernal de la red.
3. Registro histórico del precio del boleto.

---

# Proceso de trabajo

## 1. Extracción y preparación de datos (ETL)

Se desarrolló un proceso de limpieza y transformación que incluyó:

* Eliminación de registros duplicados.
* Tratamiento de valores nulos.
* Estandarización de variables categóricas.
* Conversión de tipos de datos.
* Filtrado temporal correspondiente al período de estudio.
* Detección y validación de valores atípicos (*outliers*).
* Creación de variables derivadas (mes y día de la semana).
* Normalización de variables mediante **Min-Max Scaling**.

Una vez finalizada la preparación de los datos, los datasets fueron exportados para su utilización en Power BI.

---

## 2. Análisis Exploratorio de Datos (EDA)

Se realizaron análisis descriptivos para estudiar distintos aspectos del funcionamiento de la red, entre ellos:

* Evolución mensual de la demanda.
* Distribución de pasajeros según el día de la semana.
* Demanda por línea.
* Estaciones con mayor afluencia.
* Cantidad de coches programados según línea y tipo de día.
* Relación exploratoria entre el precio del boleto y la demanda.

---

## 3. Dashboard en Power BI

Se construyó un modelo relacional que integró la información tarifaria y de demanda para desarrollar un dashboard interactivo.

El reporte incorpora filtros dinámicos y navegación entre distintas páginas, permitiendo explorar indicadores como:

* Total de pasajeros.
* Media.
* Mediana.
* Desviación estándar.

---

# Principales hallazgos

El análisis permitió identificar que:

* Se analizaron aproximadamente **276 millones de viajes** durante el período comprendido entre marzo y noviembre de 2018.
* Las **líneas B y D** concentraron la mayor cantidad de pasajeros de la red.
* Las estaciones **Constitución** y **Retiro** se consolidaron como los principales nodos de transferencia.
* La demanda presentó una fuerte concentración durante los días hábiles, especialmente los miércoles y jueves.
* Agosto registró el mayor volumen de pasajeros del período analizado.
* El análisis exploratorio mostró una relación débil entre el precio del boleto y la cantidad de pasajeros transportados. Este resultado sugiere que la demanda podría estar influenciada por otros factores además del precio, por lo que serían necesarios estudios complementarios para comprender esa relación con mayor precisión.

---

# Recomendaciones

A partir de los resultados obtenidos se propusieron las siguientes recomendaciones:

* Reforzar la capacidad operativa de las líneas con mayor demanda, especialmente las líneas B y D.
* Priorizar tareas de mantenimiento, seguridad y circulación de pasajeros en las estaciones Constitución y Retiro.
* Profundizar el análisis de la Línea E para comprender las causas de su menor utilización.
* Complementar las políticas tarifarias con mejoras en la calidad y regularidad del servicio.
* Continuar utilizando herramientas de análisis y visualización de datos para apoyar la planificación y la toma de decisiones basadas en evidencia.

---
# Datos

Los datos utilizados en este proyecto provienen del Portal de Datos Abiertos de la Ciudad Autónoma de Buenos Aires.

Por restricciones de tamaño de GitHub, los datasets originales y los datasets procesados no se incluyen en este repositorio.

Para reproducir el análisis, descargue los datos desde la fuente oficial y ejecute el notebook correspondiente.

---
# Documentación

El repositorio incluye un informe técnico donde se describen en detalle:

* La metodología utilizada.
* El proceso de limpieza y transformación de los datos.
* El análisis exploratorio realizado.
* El desarrollo del dashboard en Power BI.
* Las conclusiones y recomendaciones derivadas del estudio.

> *(Se recomienda incluir aquí una o dos capturas del dashboard para ofrecer una vista previa del proyecto.)*

