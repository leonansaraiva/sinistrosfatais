import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

def get_scopes():
    return [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

def check_login():
    return st.session_state.get("logged_in", False)

def do_logout():
    st.session_state["logged_in"] = False
    st.session_state["login_failed"] = False
    st.session_state["user_input"] = ""
    st.session_state["password_input"] = ""

def get_google_sheet_data():
    creds = Credentials.from_service_account_info(
        st.secrets["google_service_account"],
        scopes=get_scopes()
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(st.secrets["SHEET_ID"])
    sheet = spreadsheet.worksheet("dados")
    data = sheet.get_all_records()
    return data

def show_login():
    st.title("Login")
    with st.form("login_form"):
        user = st.text_input("Usuário", key="user_input")
        password = st.text_input("Senha", type="password", key="password_input")
        submitted = st.form_submit_button("Entrar")
        if submitted:
            if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
                st.session_state["logged_in"] = True
                st.session_state["login_failed"] = False
            else:
                st.session_state["logged_in"] = False
                st.session_state["login_failed"] = True

    if st.session_state.get("login_failed", False):
        st.error("Usuário ou senha inválidos")

def show_protected_content():
    st.success("Você está logado!")

    with st.spinner("Carregando dados da planilha..."):
        data = get_google_sheet_data()

    st.dataframe(data, use_container_width=True)

    if st.button("Logout"):
        do_logout()
        st.experimental_rerun()

def main():
    if check_login():
        show_protected_content()
    else:
        show_login()

if __name__ == "__main__":
    main()
