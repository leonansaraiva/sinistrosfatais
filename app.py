import streamlit as st

# Inicializa as variáveis de sessão caso não existam
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "password_input" not in st.session_state:
    st.session_state.password_input = ""

def login_callback():
    user = st.session_state.user_input
    pwd = st.session_state.password_input
    if user == st.secrets["APP_USER"] and pwd == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_failed = False
    else:
        st.session_state.logged_in = False
        st.session_state.login_failed = True
    st.experimental_rerun()

def logout_callback():
    st.session_state.logged_in = False
    st.session_state.login_failed = False
    st.session_state.user_input = ""
    st.session_state.password_input = ""
    st.experimental_rerun()

def show_login():
    st.title("Login")
    st.text_input("Usuário", key="user_input")
    st.text_input("Senha", type="password", key="password_input")
    st.button("Entrar", on_click=login_callback)

    if st.session_state.login_failed:
        st.error("Usuário ou senha inválidos")

def show_protected_content():
    st.success("Você está logado!")
    st.write("Aqui vai o conteúdo protegido.")
    st.button("Logout", on_click=logout_callback)

def main():
    if st.session_state.logged_in:
        show_protected_content()
    else:
        show_login()

if __name__ == "__main__":
    main()
