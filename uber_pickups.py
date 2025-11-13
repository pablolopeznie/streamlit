import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

## Vamos a importar datos para el ejemplo
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com'
            '/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

## Definimos una función para importar datos - load_data()
@st.cache_data
def load_data(nrows:int) -> pd.DataFrame:
    # Leemos el CSV hosteado en el DATA_URL
    data = pd.read_csv(DATA_URL, nrows=nrows)

    # Definimos una función lambda para transformar a minúsculas
    lowercase_tr = lambda x: str(x).lower()

    # Usamos el método pd.rename() para mapear el lambda anterior
    data.rename(lowercase_tr, axis='columns', inplace=True) # inplace: bool (copia o modificación del df)

    # Transformamos las fechas de txt a formato fecha
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

    return data

## Probaremos la función creada
# Usamos st.text() para sacar información al usuario
st.subheader('Importación de datos crudos')
data_load_state = st.text('Loading data...')

# Cargamos 10k filas del csv al df
data = load_data(10000)

# Notificamos al usuario que se ha completado la tarea
data_load_state.text('Done! (now, using @st.data_cache)')

# Tras ejecutar esta parte del script, vemos que es un trabajo pesado
# Ha tardado un tiempo considerable en devolver el data.frame
# No nos interesa que se vuelva a generar este bloque de cero si reejecutamos el código
# Por ello, podemos usar @st.cache_data delante de load_data() para almacenar este output

# Vamos a visualizar el data.frame
if st.checkbox('Mostrar los datos crudos'):
    st.subheader('Raw data')
    st.write(data)

# Ahora podemos trabajar con los datos, generaremos un histograma
st.subheader('Number of Uber pickups by hour')
hist = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24)
    )[0]

# Usamos la función bar_chart() para representar el histograma
color_select = st.color_picker(
    label='**Selecciona el color de las barras**', 
    value = '#4047B3', 
    label_visibility='collapsed'
    )
st.bar_chart(hist, color=color_select) 

# Es importante remarcar que Streamlit soporta librerias potentes para charting (matplotlib, Altair, Bokeh, etc.)

# Si quisiéramos ver un mapa de los lugares donde se hacen pickups
st.subheader('Map of Uber pickups')
st.map(data) # No hace falta nada más! st.map() detecta las coordenadas directamente

# ¿Y si solo queremos ver a las 17h, la hora más concurrida?
date_to_filter = st.slider(
    'Hora de recogida de Uber',
    0, 23, 17, step=1)
st.subheader(f'Map of all pickups at {date_to_filter}:00')
st.map(data[data[DATE_COLUMN].dt.hour == date_to_filter], color=color_select)

