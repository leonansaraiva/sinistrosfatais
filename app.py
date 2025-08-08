import streamlit as st
import time
import datetime

SESSION_TIMEOUT_MINUTES = 10

def mostrar_tempo_sessao_expira(login_time: float, timeout_minutos: int):
    expire_timestamp = login_time + timeout_minutos * 60
    remaining_seconds = int(expire_timestamp - time.time())

    if remaining_seconds > 0:
        expire_dt = datetime.datetime.fromtimestamp(expire_timestamp)
        expire_str = expire_dt.strftime("%d/%m/%Y %H:%M:%S")
        st.markdown(
            f"""
            <div style="position: fixed; top: 10px; right: 10px; 
                        background-color: #f0f0f0; padding: 8px 12px; 
                        border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.1);
                        font-size: 14px; z-index: 9999;">
                Sessão expira em:<br><b>{expire_str}</b>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="position: fixed; top: 10px; right: 10px; 
                        background-color: #f8d7da; color: #721c24; padding: 8px 12px; 
                        border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.1);
                        font-size: 14px; z-index: 9999;">
                Sessão expirada
            </div>
            """,
            unsafe_allow_html=True
        )

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.login_time = 0
    st.session_state.login_failed = False

def is_logged_in():
    if not st.session_state.logged_in:
        return False
    if time.time() - st.session_state.login_time > SESSION_TIMEOUT_MINUTES * 60:
        st.session_state.logged_in = False
        return False
    return True

def login_callback():
    user = st.session_state.user_input
    pwd = st.session_state.password_input
    if user == st.secrets["APP_USER"] and pwd == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_time = time.time()
        st.session_state.login_failed = False
    else:
        st.session_state.logged_in = False
        st.session_state.login_failed = True
    st.experimental_rerun()  # Chama o rerun dentro do callback, ok!

def logout_callback():
    st.session_state.logged_in = False
    st.session_state.login_failed = False
    st.experimental_rerun()  # Também dentro do callback

if not is_logged_in():
    st.title("Login")
    st.text_input("Usuário", key="user_input")
    st.text_input("Senha", type="password", key="password_input")
    st.button("Entrar", on_click=login_callback)
    if st.session_state.login_failed:
        st.error("Usuário ou senha inválidos")
else:
    st.success("Você está logado!")
    st.write("Conteúdo protegido aqui...")
    st.button("Logout", on_click=logout_callback)
    mostrar_tempo_sessao_expira(st.session_state.login_time, SESSION_TIMEOUT_MINUTES)
