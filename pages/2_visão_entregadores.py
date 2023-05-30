from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import folium_static

#from pillow import Image

st.set_page_config( page_title='Visão Entregadores', layout='wide')

import pandas as pd

df = pd.read_csv('train.csv')



df1 = df.copy()

# 1. convertando a coluna Age de texto para numero
linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['City'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Festival'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

# 2. convertando a coluna Ratings de texto para numero decimal ( float )
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

# 3. convertando a coluna order_date de texto para data
df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

# 4. convertendo multiple_deliveries de texto para numero inteiro ( int )
linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

## 5. Removendo os espacos dentro de strings/texto/object
#df1 = df1.reset_index( drop=True )
#for i in range( len( df1 ) ):
#  df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()


# 6. Removendo os espacos dentro de strings/texto/object

df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

# 7. Limpando a coluna de time taken
df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
df1['Time_taken(min)']  = df1['Time_taken(min)'].astype( int )

#Visao Entregadores

#############################
#Barra Lateral
###############################
st.header('Marketplace - Visão Entregadores')

#image_path = ('logo.png')
#image = Image.open('image_path')
#st.sidebar.image(image, width=120)


st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in town')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até que valor?',
    value=pd.datetime(2022,4,13),
    min_value=pd.datetime(2022,2,11),
    max_value=pd.datetime(2022,4,6),
    format = 'DD-MM-YYYY')



st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições de trânsito',
    ['Low','Medium','High','Jam'],
    default = 'Low')
    
st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

#Filtro data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]


#Filtro transito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]


#############################
#Layout no Streamlit
###############################
tab1,tab2,tab3 = st.tabs (['Visão Gerencial','_','_'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            #Maior idade entregadores
            
            maior_idade = df1.loc[: , 'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)
        with col2:
            #A menor idade dos entregadores
            
            menor_idade = df1.loc[: , 'Delivery_person_Age'].min()
            col2.metric('Menor idade', menor_idade)
        with col3:
            #Melhor condição de veículos
          
            melhor_condicao = df1.loc[: , 'Vehicle_condition'].max()
            col3.metric('Melhor condicao', melhor_condicao)
        with col4:
            #Pior condição de veículos
            
            pior_condicao = df1.loc[: , 'Vehicle_condition'].min()
            col4.metric('Pior condicao', pior_condicao)
            
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Avaliação média por entregador')
            df_ratings_delivery = (df1.loc[:, ['Delivery_person_ID','Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index())
            st.dataframe(df_ratings_delivery)
        with col2:
            st.markdown('##### Avaliação média por tipo de trânsito')
            linhas_vazias = df1['Road_traffic_density'] != 'NaN '

            df_ratings_traffic = df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']].groupby('Road_traffic_density').mean().reset_index()

            df_ratings_traffic = df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density']].groupby('Road_traffic_density').std().reset_index()
            st.dataframe(df_ratings_traffic)
            
            st.markdown('##### Avaliação média por clima')
            linhas_vazias = df1['Weatherconditions'] != 'NaN'

            df_rating_weather = (df1.loc[:,          ['Delivery_person_Ratings','Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings' : ['mean','std']}))
            df_rating_weather.columns = ['delivery_mean','delivery_std']
            df_rating_weather = df_rating_weather.reset_index()
            st.dataframe(df_rating_weather)

            
    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de entrega')
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Top entregadores mais rápidos')
            df2 = (df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).mean().sort_values(['City','Time_taken(min)'], ascending=True).reset_index())
                   
            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
                   
            df3 = pd.concat ([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
            st.dataframe(df3)
                   
        with col2:
            st.subheader('Top entregadores mais lentos')
            df2 = (df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).mean().sort_values(['City','Time_taken(min)'], ascending=False).reset_index())
                   
            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
                   
            df3 = pd.concat ([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
            st.dataframe(df3)
                   