import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("Login do Sistema")

if not st.session_state.logged_in:
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")
else:
    st.write("Você já está logado!")
