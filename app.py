import streamlit as st
import streamlit_authenticator as stauth
import datetime
import time
import pytz

SESSION_TIMEOUT_MINUTES = 10

# Usuários e senhas para exemplo - substitua pelos seus ou configure melhor
users = {
    "user1": {"name": "Usuário 1"},
    "user2": {"name": "Usuário 2"},
}

hashed_passwords = [
    "<hash_da_senha_do_user1_aqui>",
    "<hash_da_senha_do_user2_aqui>"
]

credentials = {
    "usernames": {
        username: {
            "name": users[username]["name"],
            "password": hashed_passwords[i]
        }
        for i, username in enumerate(users.keys())
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "app_cookie_name",
    "app_signature_key",  # Use uma chave secreta forte aqui
    cookie_expiry_days=1
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
            unsafe_allow_html=True
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
            unsafe_allow_html=True
        )

# Login
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Você está logado como {name}!")

    # Marca o tempo do login na session_state, se não existir ainda
    if "login_time" not in st.session_state:
        st.session_state.login_time = time.time()

    # Conteúdo protegido
    st.write("Conteúdo protegido aqui...")

    # Mostrar aviso de expiração
    mostrar_tempo_sessao_expira(st.session_state.login_time, SESSION_TIMEOUT_MINUTES)

    # Botão logout
    if st.button("Logout"):
        authenticator.logout("Logout", "main")
        st.session_state.pop("login_time", None)

elif authentication_status is False:
    st.error("Usuário ou senha inválidos")
else:
    st.info("Por favor, faça login")
