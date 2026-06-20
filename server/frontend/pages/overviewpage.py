import streamlit as st
from streamlit_extras.resizable_columns import resizable_columns
from streamlit_extras.card_selector import *
import streamlit_shadcn_ui as ui
import requests

st.header("General Overview")
st.text("""
Ernevil is an open-source monitoring platform designed to help administrators manage and monitor devices across a Local Area Network, with cloud support planned for future releases. It focuses on simplicity, automation, and centralized system management while remaining fully transparent and community-driven.""")


ui.link_button(text="Github", url="https://github.com/Ecruz0x/Project-Ernevil/", key="link_btn")


st.header("How To Use")

selected = card_selector(
    [
        dict(
            icon=":material/computer:",
            title="Server",
            description="Deploy the server's software on the administration machine",
        ),
        dict(
            icon=":material/security:",
            title="Account",
            description="Create your administrator account",
        ),
        dict(
            icon=":material/hub:",
            title="Agents",
            description="Deploy the agent software to your computers or servers and login using your administration credentials",
        ),
        dict(
            icon=":material/dns:",
            title="Monitor",
            description="Monitor your infrastructure",
        ),
    ],
    key="demo_basic",
)

st.header("Current metrics")

try:
    rcmp = requests.get("http://127.0.0.1:8000/api/computers")
    rloc = requests.get("http://127.0.0.1:8000/api/locations")
    ralerts = requests.get("http://127.0.0.1:8000/api/get_alerts")
    alerts = ralerts.json()
    if rcmp.status_code == 200 and rloc.status_code == 200:
        cmps = rcmp.json()
        if len(cmps) >= 1:

            last_added = cmps[-1]["computername"]

            loc = len(rloc.json())
            cols = st.columns(3)
            with cols[0]:
                ui.metric_card(title="Devices", content=len(cmps), description="Detected devices", key="devices")
            with cols[1]:
                ui.metric_card(title="Locations", content=loc, description="Available locations", key="locations")
            with cols[2]:
                ui.metric_card(title="Last added Device", content=last_added, description="Last added device", key="ladev")

            nxtcols = st.columns(1)
            with nxtcols[0]:
                name = None
                if alerts:
                    name = [computer["computername"] for computer in cmps if alerts[-1]["computer_id"] == computer["computer_id"]]
                ui.metric_card(title="Last Alert", content=f"{alerts[-1]['event'] if alerts else 'No recent alert detected'} on {name[0] if name else 'None'}", description="Last detected alert", key="laalert")

        else:
            st.error(
                "No devices are currently detected. Please verify that your agents are running and that the credentials are configured correctly."
            )

except Exception as e:
    st.html(e)
    st.error(
        "Failed to communicate with the web server. This may be caused by an invalid configuration, network issue, or server unavailability. Please verify your settings and retry."
    )
