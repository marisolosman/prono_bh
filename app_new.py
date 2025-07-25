import streamlit as st
import os
import re
import numpy as np
from PIL import Image
from datetime import datetime, timedelta

# Directorio raíz de las figuras
#DIRECTORIO_FIGURAS = "/home/marisol/Dropbox/investigacion/proyectos/pde_2019/resultados/objetivo_1/figuras_pronosticos/"
DIRECTORIO_FIGURAS = 'FIGURAS'


def get_fechas():
    # Lista para almacenar las fechas
    fechas = []
    # Definir la fecha de inicio
    fecha_inicio = datetime.now().replace(year=datetime.now().year - 1)
    fecha_fin = datetime.now() - timedelta(days=1)
    # Iterar a través de los días desde noviembre de 2021 hasta hoy
    while fecha_inicio <= fecha_fin:
        # Verificar si el día es domingo o miércoles
        if fecha_fin.weekday() == 6: # or fecha_fin.weekday() == 2:
            # Agregar la fecha al vector en formato YYYYMMDD
            fechas.append(fecha_fin.strftime("%Y-%m-%d"))
        # Incrementar la fecha en un día
        fecha_fin -= timedelta(days=1)

    return fechas

# Obtener la lista de fechas disponibles
fechas_disponibles = get_fechas()

# Obtener la lista de estaciones disponibles
estaciones_disponibles = ["junin", "ceres", "resistencia", "vmrs", "tres_arroyos",
                         "tandil", "parana", "trenque_lauquen", "concordia",
                         "venado_tuerto"]  # Reemplaza con tus estaciones reales

# Diccionario para asignar etiquetas a las figuras
etiquetas_figuras = {
    "Corregido": ["_corregido_", "_corregido-"],
    "Sin Corregir": ["_sin_corregir_", "_sin_corregir-"],
    "Climatológico": ["_climatologico_", "_climatologico-"]
}
# Función para obtener la lista de figuras para una fecha y estación dadas
def obtener_figuras(fecha, estacion):
    ruta_fecha = os.path.join(DIRECTORIO_FIGURAS)
    figuras = []
    fecha = datetime.strptime(fecha, "%Y-%m-%d")
    for root, dirs, files in os.walk(ruta_fecha):
        for file in files:
            if np.logical_and(estacion in file, fecha.strftime("%Y%m%d") in file):
               figuras.append(os.path.join(ruta_fecha, file))
    for i in figuras:
        if "EG" in i:
            print(i)
    return figuras

# Función principal de la aplicación
def main():
    st.set_page_config(layout="wide")
    st.title("Pronóstico de Balance Hídrico en estaciones de Argentina")
    col1, col2 = st.columns(2)

    with col1:
        # Agregar explicaciones en la barra lateral
        st.markdown("## Qué vemos?")
        st.write("Los paneles muestran la perspectiva para los próximos 30 días del contenido de agua en el suelo (en milímetros, mm) para diferentes estaciones meteorológicas de Argentina. Esta perspectiva se obtiene a partir del promedio de los pronósticos considerados y los diferentes miembros del ensamble y se actualiza cada lunes y jueves por la tarde.")
        st.markdown("## ¿Cómo se elabora este pronóstico?")
        st.write( "La perspectiva está basada en los pronósticos del Climate Forecast System Version 2 elaborados por la NOAAs National Centers for Environmental Prediction. Se utilizan los 16 pronósticos de las variables diarias que intervienen en el balance hídrico (temperaturas máxima y mínima, humedad relativa, velocidad del viento a 10m, precipitación y evapotranspiración potencial) producidos cada domingo y miércoles.")
        st.write("Los pronósticos de modelo son calibrados por separado para cada variable utilizando la metodología de quantile-quantile mapping. Con excepción de la precipitación, todas las variables se ajustan siguiendo una distribución empírica a partir de los datos del período 1999-2010. En el caso de la lluvia, se asume que las observaciones siguen una distribución gamma cuyos parámetros se obtienen con los datos del período 1999-2010. Las bases de datos de referencia corresponden a los datos de estaciones meteorológicas del Servicio Meteorológico Nacional y del Instituto Nacional de Tecnología Agropecuaria.")

    with col2:
        st.markdown("## Cómo se interpreta?")
        st.write("<p style='margin-bottom: 5px;'>El eje horizontal indica las fechas desde la siembra del cultivo considerado hasta la finalización estimada de su ciclo. El eje vertical indica el contenido de agua en el suelo (mm) hasta 1m de profundidad, o hasta una profundidad menor si el perfil impide la penetración radicular.</p>", unsafe_allow_html=True)
        st.write("<p style='margin-bottom: 5px;'> La línea negra indica la evolución del contenido de agua en el suelo (mm) a lo largo de la campaña en curso, estimado según un modelo propio de balance hídrico diario (ver metodología de balance hídrico) basado en la metodología propuesta por FAO. En este caso, el contenido de agua se estimó según datos meteorológicos medidos en la estación.</p>", unsafe_allow_html=True )
        st.write("<p style='margin-bottom: 5px;'>La línea verde señala la evolución prevista del contenido de agua en el suelo, es decir, el almacenaje pronosticado según el ensamble del modelo meteorológico considerado.</p>", unsafe_allow_html=True)
        st.write("<p style='margin-bottom: 5px;'>Las áreas de color gris oscuro y gris claro muestran la dispersión de 50% y 100%, respectivamente, en los miembros del modelo.</p>", unsafe_allow_html=True)
        st.write("<p style='margin-bottom: 5px;'>La línea punteada azul marca a lo largo del ciclo los niveles más bajos de almacenaje de agua obtenidos en el periodo histórico (1970-actualidad). O sea, si la línea negra desciende tanto como para estar por debajo de la línea punteada, significa que nunca antes se han registrado niveles tan bajos de almacenamiento hídrico en esa fecha.</p>", unsafe_allow_html=True)
        st.write("<p style='margin-bottom: 5px;'>Tanto la evolución del contenido de agua en el suelo en la campaña en curso (línea negra) como los pronósticos deben ser inferiores a la capacidad de campo del suelo característico de la zona, que representa el máximo contenido de agua posible y se visualiza en el gráfico como una línea horizontal azul.</p>", unsafe_allow_html=True)
        st.write("<p style='margin-bottom: 5px;'>Niveles inferiores al punto de marchitez permanente, representado por una línea horizontal roja, indican falta total de agua útil, es decir, sequía severa.</p>", unsafe_allow_html=True)
        st.write("<p style='margin-bottom: 5px;'>Para cada cultivo se han resaltado: el periodo crítico para déficit hídrico (área amarilla) y el periodo crítico para excesos hídricos (área celeste).</p>", unsafe_allow_html=True)

    st.write("Selecciona una fecha y una estación para ver las figuras correspondientes.")

    # Seleccionar etiqueta
    #etiqueta_seleccionada = st.selectbox("Selecciona una etiqueta:", list(etiquetas_figuras.keys()))

    # Seleccionar fecha
    fecha_seleccionada = st.selectbox("Selecciona una fecha:", fechas_disponibles)

    # Seleccionar estación
    estacion_seleccionada = st.selectbox("Selecciona una estación:", estaciones_disponibles)

    # Obtener figuras para la fecha y estación seleccionadas
    figuras = sorted(obtener_figuras(fecha_seleccionada, estacion_seleccionada))
     # Mostrar las figuras
    col1, col2 = st.columns(2)
    
    if figuras:
        for i, figura in enumerate(figuras):
            if 'EG' in figura:
                titulo = 'Pronóstico corregido'
            elif 'SC' in figura:
                titulo = 'Pronóstico sin corregir'
            else:
                titulo = 'Pronóstico a partir de datos históricos'
            if i == 0:
                columna = col1
                with columna:
                    st.subheader(titulo)
                    imagen = Image.open(figura)
                    st.image(imagen, width=600)                   

            elif i ==1:
                columna = col2
                with columna:
                    st.subheader(titulo)
                    imagen = Image.open(figura)
                    st.image(imagen, width=600)
            else:
                st.subheader(titulo)
                imagen = Image.open(figura)
                st.image(imagen, width=600)
    else:
        st.warning("No se encontraron figuras para la fecha y estación seleccionadas.")
    st.write("## Referencias")
    st.write("http://www.ora.gob.ar/informes/Reservas_de_Agua_Metodologia_balance.pdf")
    st.write("Saha, S., ;S. Moorthi, X. Wu, J. Wang, and Coauthors, 2014: The NCEP Climate Forecast System Version 2. Journal of Climate, 27, 2185–2208, doi:10.1175/JCLI-D-12-00823.1.")
    st.write("Jakob Themeßl, M., Gobiet, A. and Leuprecht, A. (2011), Empirical-statistical downscaling and error correction of daily precipitation from regional climate models. Int. J. Climatol., 31: 1530-1544. https://doi.org/10.1002/joc.2168")
    st.write("Amor V.M. Ines, James W. Hansen, Bias correction of daily GCM rainfall for crop simulation studies, Agricultural and Forest Meteorology, Volume 138, Issues 1–4, 2006, Pages 44-53, ISSN 0168-1923, https://doi.org/10.1016/j.agrformet.2006.03.009.")

if __name__ == "__main__":
    main()

