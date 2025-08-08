import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# --- Login simples ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login do Sistema")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
            st.session_state.logged_in = True
            # Rerun para atualizar o estado da sessão
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")
    st.stop()

# --- Configurar credenciais ---
creds = Credentials.from_service_account_info(st.secrets["google_service_account"])
client = gspread.authorize(creds)

# --- Abrir planilha ---
spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])
sheet = spreadsheet.worksheet("dados")

# --- Ler dados ---
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- Ajustar layout para largura total ---
st.markdown(
    """
    <style>
    .css-1d391kg {
        max-width: 100% !important;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("📊 Dados da aba 'dados'")

st.dataframe(df, use_container_width=True)
