import streamlit as st
import os
import hashlib
import secrets

# Lê as variáveis de ambiente
APP_USER = os.getenv("APP_USER")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def check_login(username, password):
    # Compara usuário
    if username != APP_USER:
        return False
    
    # Compara senha via hash SHA256
    hash_input = hashlib.sha256(password.encode()).hexdigest()
    hash_real = hashlib.sha256(APP_PASSWORD.encode()).hexdigest()
    
    return hash_input == hash_real

def login():
    st.title("🔐 Login")
    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        if check_login(user, pwd):
            st.session_state["auth_token"] = secrets.token_hex(16)
            st.session_state["usuario"] = user
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

# Se não tiver token, mostra tela de login
if "auth_token" not in st.session_state:
    login()
    st.stop()

# Conteúdo protegido
st.success(f"Bem-vindo, {st.session_state['usuario']}!")
st.write("🎯 Você está logado com segurança usando variáveis de ambiente.")

# Botão para sair
if st.button("Sair"):
    st.session_state.clear()
    st.rerun()
