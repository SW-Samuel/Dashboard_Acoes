import streamlit as st

left_column, right_column = st.columns([1,1.5])

user = st.session_state
name_user = None
if 'username' in user:
    name_user = user.name

left_column.title('SW&Co')

if name_user:
    left_column.write(f'#### Bem vindo, {name_user}')

dashboard_button = left_column.button('Dashboards Pojetos')
indicators_button = left_column.button('Principais Indicadores')

if dashboard_button:
    st.switch_page('dashboard.py')
if indicators_button:
    st.switch_page('indicators.py')

container = right_column.container(border=True)
container.image('assets/log.png')