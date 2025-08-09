import streamlit as st
import time
import gspread
import pandas as pd
import numpy as np
from google.oauth2.service_account import Credentials
import base64

st.set_page_config(layout="wide")

SESSION_TIMEOUT_MINUTES = 10
BPTRAN_LOGO_PATH = "bptran_logo.png"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_time" not in st.session_state:
    st.session_state.login_time = 0
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False

def get_scopes():
    return [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

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
    st.experimental_set_query_params(logout=str(time.time()))
    # Não chame st.experimental_rerun() para evitar erro

def get_google_sheet_data():
    creds = Credentials.from_service_account_info(
        st.secrets["google_service_account"],
        scopes=get_scopes()
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])
    sheet = spreadsheet.worksheet("dados")
    records = sheet.get_all_records()
    df = pd.DataFrame(records)

    if "Número (KM)" in df.columns:
        df["Número (KM)"] = df["Número (KM)"].replace('-', np.nan)
        df["Número (KM)"] = pd.to_numeric(df["Número (KM)"], errors='coerce')

    return df

def _get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def inject_css():
    st.markdown(
        """
        <style>
        .header-container {
            width: 100%;
            padding: 0 1rem;
            margin: 20px auto;
            text-align: justify;
            line-height: 1.4;
            font-weight: normal;
            font-size: 1rem;
        }
        .header-container img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 12px;
            width: 120px;
            object-fit: contain;
            margin-top: 0;
        }
        .header-container h2 {
            text-align: center;
            margin-top: 0;
            margin-bottom: 8px;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def show_login():
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

def show_protected_content():
    inject_css()

    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 10px 0;">
                <img src="data:image/png;base64,{_get_base64(BPTRAN_LOGO_PATH)}" 
                     style="width:100px; margin-bottom:10px; object-fit:contain;">
                <h3 style="margin-bottom: 20px;">Menu</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.button("🚪 Sair", on_click=logout_callback, use_container_width=True)

        st.markdown("---")
        st.markdown("### 📊 Relatórios")
        st.markdown("- Óbitos")
        st.markdown("- Comparativo 2024/2025")
        st.markdown("- Mapa de Ocorrências")

    st.markdown(
        f"""
        <div class="header-container">
            <img src="data:image/png;base64,{_get_base64(BPTRAN_LOGO_PATH)}" alt="Logo BPTran" />
            <h2>Sinistros de Trânsito - BPTran</h2>
            <p>
                Este relatório apresenta os óbitos em sinistros fatais atendidos pelo Batalhão de Polícia de Trânsito - BPTran em Curitiba.<br>
                Os dados são extraídos do sistema BATEU e filtrados para mostrar apenas os óbitos registrados pelo BPTran na cidade.<br>
                Serve de apoio para a elaboração do GDO (Gestão de Desempenho Operacional) e análise comparativa entre os anos 2024 e 2025.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("Carregando dados da planilha..."):
        data = get_google_sheet_data()
    st.dataframe(data, use_container_width=True, height=800)

def main():
    if is_logged_in():
        show_protected_content()
    else:
        show_login()

if __name__ == "__main__":
    main()
