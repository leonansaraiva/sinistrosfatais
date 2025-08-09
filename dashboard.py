import streamlit as st
import pandas as pd
import base64
from google.oauth2.service_account import Credentials
import gspread
import numpy as np
from mapa import show_map

BPTRAN_LOGO_PATH = "bptran_logo.png"

def get_scopes():
    return [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

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

def _get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

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
        df["Número (KM)"] = df["Número (KM)"].astype(str).replace('-', '')
        df["Número (KM)"] = pd.to_numeric(df["Número (KM)"], errors='coerce')

    return df

def get_fake_map_data():
    # Dados fake no formato esperado pelo mapa
    data = [
        {
            "id": 1, "bairro": "Centro", "data": "2024-03-10", "genero": "Masculino", "tipo": "Colisão",
            "latitude": -25.4284, "longitude": -49.2733,
            "envolvidos": [
                {"tipo": "Condutor", "nome": "João Silva", "veiculo": "Ford Ka", "placa": "ABC-1234", "resultado": "Óbito"},
                {"tipo": "Condutor", "nome": "Carlos Souza", "veiculo": "Fiat Uno", "placa": "XYZ-5678", "resultado": "Ferimentos"}
            ]
        },
        {
            "id": 8, "bairro": "São Francisco", "data": "2025-09-25", "genero": "Masculino", "tipo": "Colisão Frontal",
            "latitude": -25.3900, "longitude": -49.2800,
            "envolvidos": [
                {"tipo": "Condutor", "nome": "Rodrigo Silva", "veiculo": "Toyota Hilux", "placa": "KLM-7777", "resultado": "Óbito"},
                {"tipo": "Condutor", "nome": "Juliana Souza", "veiculo": "Honda HRV", "placa": "NOP-8888", "resultado": "Ferimentos"}
            ]
        }
    ]
    return pd.DataFrame(data)

def show_dashboard(logout_callback):
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

        escolha = st.radio("Selecione a visualização:", ["Tabela", "Mapa"], index=0)

    if escolha == "Tabela":
        data = get_google_sheet_data()
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
        st.dataframe(data, use_container_width=True, height=800)

    elif escolha == "Mapa":
        data = get_fake_map_data()
        show_map(data)
