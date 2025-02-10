import streamlit as st
from data_loader import loadData, loadSelect
import plotly.express as px
import pandas as pd

st.title('Indicadores')

def card_create(icon, number, text, column_card):
    container = column_card.container(border=True)
    left_column, right_column = container.columns([1,2.5])
    left_column.image(f'assets/{icon}')
    right_column.write(number)
    right_column.write(text)

selctBase = loadSelect()

left_column, right_column = st.columns([3,3])

sector = left_column.selectbox('Setor', selctBase)

if sector:
    base = loadData(sector, '1')
    
    if len(base) != 0:

        left_column, middle_column, right_column = st.columns([1,1,1])
        
        data = pd.Timestamp(base.index.max())
        card_create('oportunidades.png', f'{data.strftime('%d-%m-%Y')}', 'Data', left_column)
        
        max_index = base.index.max() 
        open_value = base.loc[max_index, 'Open']
        card_create('projetos_fechados.png', f'{open_value:,.2f}', 'Open', middle_column)
        
        open_value = base.loc[max_index, 'High']
        card_create('projetos_fechados.png', f'{open_value:,.2f}', 'High', right_column)
        
        open_value = base.loc[max_index, 'Low']
        card_create('projetos_fechados.png', f'{open_value:,.2f}', 'Low', left_column)
        
        open_value = base.loc[max_index, 'Close']
        card_create('projetos_fechados.png', f'{open_value:,.2f}', 'Close', middle_column)
        
        open_value = base.loc[max_index, 'Volume']
        card_create('total_orcado.png', f'{open_value:,.2f}', 'Volume', right_column)
