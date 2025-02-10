import streamlit as st
import pandas as pd
import bcrypt
from models import session, User


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt() 
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8') 

def check_password(entered_password: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash.encode('utf-8'))

list_user = session.query(User).all()

credentials = { "usernames" : 
    {user.email : {'name': user.name, 'password': user.password , 'admin': user.admin} for user in list_user}
}

def user_authenticate():
    if 'authenticated' in st.session_state and st.session_state['authenticated']:
        return {'name': st.session_state['name'], 'username': st.session_state['username']}

    email = st.text_input("E-mail", key="login_email")
    password = st.text_input("Senha", type="password", key="login_password")

    if st.button("Entrar"):
        if email in credentials["usernames"]:
            stored_password_hash = credentials["usernames"][email]["password"]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
                st.session_state['authenticated'] = True
                st.session_state['name'] = credentials['usernames'][email]['name']
                st.session_state['username'] = email
                
                st.success(f"Bem-vindo, {credentials['usernames'][email]['name']}!")
                
                st.rerun()
                return {'name': credentials['usernames'][email]['name'], 'username': email}
            else:
                st.error("Senha incorreta")
        else:
            st.error("E-mail não encontrado")
    
    return None

def logout():
    st.session_state['authenticated'] = False
    st.session_state['name'] = None
    st.session_state['username'] = None
    st.success("Você foi desconectado com sucesso!")
    st.markdown(f'<meta http-equiv="refresh" content="2; url={'http://localhost:8501/'}">', unsafe_allow_html=True)

user_data = user_authenticate()

if user_data:
    user_email = user_data['username']
    user = session.query(User).filter_by(email = user_email).first()
    admin = user.admin

    if admin:
        pg = st.navigation(
            {
                'Home': [st.Page('homepage.py', title='Sw&co')],
                'Dashboards': [st.Page('dashboard.py', title='Dashboard'), st.Page('indicators.py', title='Indicadores')],
                'Conta': [st.Page(logout, title='Sair'), st.Page('createAccount.py', title='Criar Conta')]
            }
        )
    else:
        pg = st.navigation(
            {
                'Home': [st.Page('homepage.py', title='Sw&co')],
                'Dashboards': [st.Page('dashboard.py', title='Dashboard'), st.Page('indicators.py', title='Indicadores')],
                'Conta': [st.Page(logout, title='Sair')]
            }
        )

    pg.run()

else:
    st.write("Por favor, faça login para continuar.")