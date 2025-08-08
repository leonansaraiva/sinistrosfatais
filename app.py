import streamlit as st
import streamlit.components.v1 as components

def login_callback():
    user = st.session_state.user_input
    password = st.session_state.password_input
    if user == st.secrets["APP_USER"] and password == st.secrets["APP_PASSWORD"]:
        st.session_state.logged_in = True
        st.session_state.login_failed = False
    else:
        st.session_state.logged_in = False
        st.session_state.login_failed = True
    st.experimental_rerun()

def show_login():
    st.title("Login")
    st.text_input("Usuário", key="user_input")
    st.text_input("Senha", type="password", key="password_input", max_chars=8)
    st.button("Entrar", key="login_button", on_click=login_callback)

    # Código JS para focar botão quando senha tiver 8 caracteres
    js = """
    <script>
    const pwdInput = window.parent.document.querySelector('input[type="password"]');
    const btn = window.parent.document.querySelector('button[kind="primary"]');

    if (pwdInput && btn) {
        pwdInput.addEventListener('input', function() {
            if(this.value.length >= 8){
                btn.focus();
            }
        });
    }
    </script>
    """

    components.html(js)

    if st.session_state.get("login_failed", False):
        st.error("Usuário ou senha inválidos")

def show_protected_content():
    st.success("Você está logado!")
    st.write("Conteúdo protegido")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.login_failed = False
        st.experimental_rerun()

def main():
    if st.session_state.get("logged_in", False):
        show_protected_content()
    else:
        show_login()

if __name__ == "__main__":
    main()
