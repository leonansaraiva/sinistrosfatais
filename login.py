import streamlit as st
import time

SESSION_TIMEOUT_MINUTES = 10

def is_logged_in():
    if not st.session_state.get("logged_in", False):
        return False
    if time.time() - st.session_state.get("login_time", 0) > SESSION_TIMEOUT_MINUTES * 60:
        st.session_state.logged_in = False
        return False
    return True

def login_callback():
    user = st.session_state.get("user_input", "")
    pwd = st.session_state.get("password_input", "")
    if user == st.secrets["APP_USER"] and pwd == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_time = time.time()
        st.session_state.login_failed = False
    else:
        st.session_state.logged_in = False
        st.session_state.login_failed = True

def logout_callback():
    st.session_state.logged_in = False
    st.session_state.login_failed = False
    st.session_state.user_input = ""
    st.session_state.password_input = ""
    st.query_params = {"logout": str(time.time())}


def show_login(login_callback):
    import base64

    BPTRAN_LOGO_PATH = "bptran_logo.png"

    def _get_base64(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style="max-width: 400px; margin: 0 auto 20px auto; text-align: center;">
                <img src="data:image/png;base64,{_get_base64(BPTRAN_LOGO_PATH)}" width="120" style="object-fit: contain;" />
            </div>
            <h2 style="text-align: center; margin-bottom: 10px;">Sinistros de Trânsito - BPTran</h2>
            """,
            unsafe_allow_html=True,
        )

        st.text_input("Usuário", key="user_input")
        st.text_input("Senha", type="password", key="password_input")
        st.button("Entrar", on_click=login_callback)
        if st.session_state.get("login_failed", False):
            st.error("Usuário ou senha inválidos")
