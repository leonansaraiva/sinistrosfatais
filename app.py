import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("Login do Sistema")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
            st.session_state.logged_in = True
            st.experimental_rerun()  # Só aqui, dentro do if do botão
        else:
            st.error("Usuário ou senha inválidos")

else:
    st.success("Login realizado com sucesso!")

    with st.spinner("Carregando dados da planilha..."):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(
            st.secrets["google_service_account"],
            scopes=scopes
        )
        client = gspread.authorize(creds)

        spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])
        sheet = spreadsheet.worksheet("dados")
        data = sheet.get_all_records()

    st.dataframe(data, use_container_width=True)

    if st.button("Sair"):
        st.session_state.logged_in = False
        st.experimental_rerun()
