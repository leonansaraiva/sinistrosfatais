import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# -------- Configurações --------

def get_scopes():
    """Retorna escopos necessários para acessar Google Sheets e Drive."""
    return [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

# -------- Funções de Autenticação --------

def check_login():
    """Verifica se usuário está logado no session_state."""
    return st.session_state.get("logged_in", False)

def do_login(user, password):
    """
    Tenta autenticar usuário. 
    Retorna True se login válido, False caso contrário.
    """
    if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
        st.session_state["logged_in"] = True
        return True
    else:
        st.session_state["logged_in"] = False
        return False

def do_logout():
    """Realiza logout, limpando estado."""
    st.session_state["logged_in"] = False

# -------- Função para ler dados do Google Sheets --------

def get_google_sheet_data():
    """
    Autentica com Google Sheets via service account,
    abre a planilha e retorna os dados da aba "dados" como lista de dicionários.
    """
    creds = Credentials.from_service_account_info(
        st.secrets["google_service_account"],
        scopes=get_scopes()
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])
    sheet = spreadsheet.worksheet("dados")
    data = sheet.get_all_records()
    return data

# -------- Interface --------

def show_login():
    """Mostra formulário de login."""
    st.title("Login")
    user = st.text_input("Usuário", key="user_input")
    password = st.text_input("Senha", type="password", key="password_input")

    if st.button("Entrar"):
        if do_login(user, password):
            st.experimental_rerun()  # Só aqui, dentro do botão
        else:
            st.error("Usuário ou senha inválidos")

def show_protected_content():
    """Mostra conteúdo protegido após login."""
    st.success("Você está logado!")

    with st.spinner("Carregando dados da planilha..."):
        data = get_google_sheet_data()

    st.dataframe(data, use_container_width=True)

    if st.button("Logout"):
        do_logout()
        st.experimental_rerun()  # Só aqui, dentro do botão

# -------- Execução --------

def main():
    # Nota: O login será perdido ao atualizar a página pois session_state não é persistente.
    if check_login():
        show_protected_content()
    else:
        show_login()

if __name__ == "__main__":
    main()
