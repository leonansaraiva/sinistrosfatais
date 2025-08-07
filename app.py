import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# -------- LOGIN --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login do Sistema")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
            st.session_state.logged_in = True
        else:
            st.error("Usuário ou senha inválidos")
    st.stop()

# -------- CONEXÃO GOOGLE SHEETS --------
creds = Credentials.from_service_account_info(st.secrets["google_service_account"])
client = gspread.authorize(creds)

# Abrir a planilha usando o ID
spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])

# Abrir a aba chamada "dados"
sheet = spreadsheet.worksheet("dados")

# Pegar todas as linhas da aba como lista de dicionários
data = sheet.get_all_records()

# Mostrar os dados no app
st.title("📊 Dados da aba 'dados'")
st.dataframe(data)
