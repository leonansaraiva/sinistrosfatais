import streamlit as st
import streamlit_authenticator as stauth
import datetime
import time
import pytz

SESSION_TIMEOUT_MINUTES = 10

users = {
    "user1": {"name": "Usuário 1"},
}

hashed_passwords = [
    "$2b$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # troque pelo hash gerado da senha do user1
]

credentials = {
    "usernames": {
        "user1": {
            "name": "Usuário 1",
            "password": hashed_passwords[0],
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    cookie_name="app_cookie_name",
    key="app_signature_key",
    cookie_expiry_days=1,
)

def mostrar_tempo_sessao_expira(login_time: float, timeout_minutos: int):
    br_tz = pytz.timezone("America/Sao_Paulo")
    expire_timestamp = login_time + timeout_minutos * 60
    remaining_seconds = int(expire_timestamp - time.time())

    if remaining_seconds > 0:
        expire_dt_utc = datetime.datetime.utcfromtimestamp(expire_timestamp)
        expire_dt = expire_dt_utc.replace(tzinfo=pytz.utc).astimezone(br_tz)
        expire_str = expire_dt.strftime("%d/%m/%Y %H:%M:%S")
        st.markdown(
            f"""
            <div style="
                position: fixed; 
                top: 50px; 
                left: 50%; 
                transform: translateX(-50%);
                background-color: white; 
                color: black; 
                padding: 8px 20px; 
                border-radius: 8px; 
                box-shadow: 0 0 8px rgba(0,0,0,0.15);
                font-size: 16px; 
                font-weight: 600;
                z-index: 9999;
                text-align: center;
                min-width: 220px;
                ">
                Sessão expira em:<br><b>{expire_str} (Horário de Brasília)</b>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="
                position: fixed; 
                top: 50px; 
                left: 50%; 
                transform: translateX(-50%);
                background-color: #f8d7da; 
                color: #721c24; 
                padding: 8px 20px; 
                border-radius: 8px; 
                box-shadow: 0 0 8px rgba(0,0,0,0.15);
                font-size: 16px; 
                font-weight: 600;
                z-index: 9999;
                text-align: center;
                min-width: 220px;
                ">
                Sessão expirada
            </div>
            """,
            unsafe_allow_html=True,
        )

name, authentication_status, username = authenticator.login(name="Login", location="main")

if authentication_status:
    st.success(f"Você está logado como {name}!")

    if "login_time" not in st.session_state:
        st.session_state.login_time = time.time()

    st.write("Conteúdo protegido aqui...")

    mostrar_tempo_sessao_expira(st.session_state.login_time, SESSION_TIMEOUT_MINUTES)

    if st.button("Logout"):
        authenticator.logout("Logout", location="main")
        st.session_state.pop("login_time", None)

elif authentication_status is False:
    st.error("Usuário ou senha inválidos")

else:
    st.info("Por favor, faça login")
