import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Home",
    page_icon="",
    layout="wide"
)

#image_path='Documents/repos/analise_dados/'
image=Image.open ('logo.png')

st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in town')
st.sidebar.markdown("""---""")

st.write ('# Curry Company Growth Dashboard')

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e dos restaurantes.
    Como utilizar?
    - Visão empresa:
        - Visão Gerencial
        - Visão Tática
        - Visão demográfica
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais do crescimento dos restaurantes
        
    ### Ask for help
        - Time de Data Science
      
""")
    
        
