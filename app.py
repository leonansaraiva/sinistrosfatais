import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False

def login():
    user = st.session_state.get("user_input", "")
    password = st.session_state.get("password_input", "")
    if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_failed = False
    else:
        st.session_state.logged_in = False
        st.session_state.login_failed = True

if not st.session_state.logged_in:
    st.title("Login do Sistema")
    st.text_input("Usuário", key="user_input")
    st.text_input("Senha", type="password", key="password_input")
    st.button("Entrar", on_click=login)

    if st.session_state.login_failed:
        st.error("Usuário ou senha inválidos")
else:
    st.success("Login realizado com sucesso!")
    st.write("Você está logado!")
