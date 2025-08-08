import streamlit as st
import time

SESSION_TIMEOUT_MINUTES = 10

def is_logged_in():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        return False
    if time.time() - st.session_state.login_time > SESSION_TIMEOUT_MINUTES * 60:
        st.session_state.logged_in = False
        return False
    return True

def try_login(user, pwd):
    if user == st.secrets["APP_USER"] and pwd == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_time = time.time()
        st.session_state.login_failed = False
        return True
    else:
        st.session_state.logged_in = False
        st.session_state.login_failed = True
        return False

def logout():
    st.session_state.logged_in = False
    st.session_state.login_failed = False
    # limpa query params ao sair
    st.experimental_set_query_params()

def force_rerun():
    # pega os params atuais
    params = st.experimental_get_query_params()
    # alterna valor de um parâmetro dummy para forçar atualização
    dummy = params.get("dummy", ["0"])[0]
    novo_valor = "1" if dummy == "0" else "0"
    st.experimental_set_query_params(dummy=novo_valor)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.login_time = 0
    st.session_state.login_failed = False

if not is_logged_in():
    st.title("Login")
    user = st.text_input("Usuário", key="user_input")
    pwd = st.text_input("Senha", type="password", key="password_input")
    if st.button("Entrar"):
        sucesso = try_login(user, pwd)
        if sucesso:
            force_rerun()  # força atualização da página após login
    if st.session_state.login_failed:
        st.error("Usuário ou senha inválidos")
else:
    st.success("Você está logado!")
    st.write("Conteúdo protegido aqui...")

    if st.button("Logout"):
        logout()
        force_rerun()  # força atualização da página após logout
