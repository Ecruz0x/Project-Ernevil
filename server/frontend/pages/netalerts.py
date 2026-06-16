import streamlit as st
from streamlit_extras.resizable_columns import resizable_columns
from streamlit_extras.card_selector import *
import streamlit_shadcn_ui as ui
import requests, random
from streamlit_autorefresh import st_autorefresh

count = st_autorefresh(interval=10000, key="bootstraptimer")

st.header("Detected Alerts")
st.html("<h3>System-generated alerts appear here in real time.</h3>")
st.html("<h5>Review, track, and manage security events and agent notifications.</h5>")


try:
    r = requests.get("http://127.0.0.1:8000/api/get_alerts")
    alerts = r.json()
    if alerts:
        for i in range(len(alerts)):
            if alerts[i]["type"] == "USB alert":
                with st.container(border=True):
                    st.markdown(f"##### {alerts[i]['type']}")
                    st.write(alerts[i]["event"])

                    col1, col2 = st.columns(2)
                    idx = alerts[i]["computer_id"]

                    with col1:
                        st.caption(f"Category: {alerts[i]['category']}")
                        st.caption(f"Manufacturer: {alerts[i]['manufacturer']}")

                    with col2:
                        st.caption(f"Product: {alerts[i]['product']}")
                        st.caption(f"Expires: {alerts[i]['expires_at']}")
            elif alerts[i]["type"] == "Network Alert":
                with st.container(border=True):
                    st.markdown(f"##### {alerts[i]['type']}")
                    st.write("Suspected network attack detected")

                    col1, col2 = st.columns(2)
                    idx = alerts[i]["computer_id"]

                    with col1:
                        st.caption(f"Source Port: {alerts[i]['src_port']}")
                        st.caption(f"Protocol: {alerts[i]['protocol']}")

                    with col2:
                        st.caption(f"Suspected Attack type: {alerts[i]['event']}")
                        st.caption(f"Expires: {alerts[i]['expires_at']}")

                    
except Exception as e:
    print(e)
    st.error(
        "Failed to communicate with the web server. This may be caused by an invalid configuration, network issue, or server unavailability. Please verify your settings and retry."
    )