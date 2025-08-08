import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- Login simples ---
st.title("Login do Sistema")

user = st.text_input("Usuário")
password = st.text_input("Senha", type="password")

if st.button("Entrar"):
    if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
        st.success("Login realizado com sucesso!")

        # --- Conexão Google Sheets ---
        creds = Credentials.from_service_account_info(st.secrets["google_service_account"])
        client = gspread.authorize(creds)

        # Abrir a planilha pelo ID
        spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])

        # Abrir a aba "dados"
        sheet = spreadsheet.worksheet("dados")

        # Pegar todos os registros
        data = sheet.get_all_records()

        # Mostrar os dados, ajustando para ocupar largura da tela
        st.dataframe(data, use_container_width=True)

    else:
        st.error("Usuário ou senha inválidos")
