import streamlit as st

# Inicializa a variável de estado se não existir
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    user = st.session_state.get("user_input", "")
    password = st.session_state.get("password_input", "")
    if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.success("Login realizado com sucesso!")
        st.experimental_rerun()
    else:
        st.error("Usuário ou senha inválidos")

if not st.session_state.logged_in:
    st.title("Login do Sistema")
    st.text_input("Usuário", key="user_input")
    st.text_input("Senha", type="password", key="password_input")
    st.button("Entrar", on_click=login)
else:
    st.write("Você está logado!")
