import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("Teste de leitura Google Sheets")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

try:
    creds = Credentials.from_service_account_info(
        st.secrets["google_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])
    sheet = spreadsheet.worksheet("dados")

    data = sheet.get_all_records()
    st.write("Dados lidos da planilha:")
    st.dataframe(data)

except Exception as e:
    st.error(f"Erro ao acessar a planilha: {e}")
