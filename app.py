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
            st.experimental_rerun()  # Recarrega a página para iniciar sessão autenticada
        else:
            st.error("Usuário ou senha inválidos")
    st.stop()

# -------- CONEXÃO GOOGLE SHEETS --------
creds = Credentials.from_service_account_info(st.secrets["google_service_account"])
client = gspread.authorize(creds)

spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])
sheet = spreadsheet.worksheet("dados")
data = sheet.get_all_records()

# -------- MOSTRAR DADOS --------
st.title("📊 Dados da aba 'dados'")
st.dataframe(data, use_container_width=True)
