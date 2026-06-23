import streamlit as st
import requests


st.markdown("""
<style>
section[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Ernevil", layout="centered")

cert = "server.crt"

users_exist = False

try:
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }
    r = requests.get(
        "https://127.0.0.1:8000/api/users/count",
        verify=cert,
        headers=headers
    )

    if r.ok:
        users_exist = r.json()["count"] > 0

except Exception:
    st.error("Unable to check user database")

if "token" not in st.session_state:
    st.session_state.token = None

st.title("🛡️ Ernevil")
if not users_exist:
    login_tab, register_tab = st.tabs(["Login", "Create Account"])


    with login_tab:
        with st.form("login"):
            username = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Login")

            if submitted:
                r = requests.post(
                    "https://127.0.0.1:8000/api/users/token", headers=headers,
                    data={
                        "username": username,
                        "password": password
                    },
                    verify=cert
                )

                if r.status_code == 200:
                    st.session_state.token = r.json()["access_token"]
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    with register_tab:
        with st.form("register"):
            new_username = st.text_input("Username", key="reg_username")
            new_email = st.text_input("Email")
            new_password = st.text_input(
                "Password",
                type="password",
                key="reg_password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            create = st.form_submit_button("Create Account")

            if create:

                if new_password != confirm_password:
                    st.error("Passwords do not match")

                else:
                    r = requests.post(
                        "https://127.0.0.1:8000/api/users", headers=headers,
                        json={
                            "username": new_username,
                            "email": new_email,
                            "password": new_password
                        },
                        verify=cert
                    )

                    if r.status_code in [200, 201]:
                        st.success("Account created successfully")
                    else:
                        try:
                            st.error(r.json()["detail"])
                        except:
                            st.error("Failed to create account")
else:
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }
    login_tab = st.container(border=True)
    with login_tab:
        with st.form("login"):
            username = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Login")

            if submitted:
                r = requests.post(
                    "https://127.0.0.1:8000/api/users/token", headers=headers,
                    data={
                        "username": username,
                        "password": password
                    },
                    verify=cert
                )

                if r.status_code == 200:
                    st.session_state.token = r.json()["access_token"]
                    st.rerun()
                else:
                    st.error("Invalid credentials")