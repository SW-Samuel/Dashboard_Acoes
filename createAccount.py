import streamlit as st
from models import session, User
import bcrypt

st.title('Criar Conta')

form = st.form("form_create_acount")
user_name = form.text_input('Nome do usuário')
user_email = form.text_input('Email do usuário')
user_password = form.text_input('Senha do usuário', type='password')
user_admin = form.checkbox('É um admin?')
submit_button = form.form_submit_button('Enviar')

if submit_button:
    list_user = session.query(User).filter_by(email=user_email).all()

    if len(list_user) > 0:
        st.write('Já existe um usuário com esse email cadastrado')
    elif len(user_email) < 5 or len(user_password) < 3:
        st.write('Preencha o campo de email e senha corretamente')
    else:
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
        user = User(name=user_name, password=hashed_password, email=user_email, admin=user_admin)
        session.add(user)
        session.commit()
        st.switch_page('homepage.py')