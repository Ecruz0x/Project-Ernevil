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


##### Login and access tokens....####


rcmp = requests.get("http://127.0.0.1:8000/api/computers")
if rcmp.status_code == 200:
    cmps = len(rcmp.json())
    last_added = rcmp.json()[-1]["computername"]


rloc = requests.get("http://127.0.0.1:8000/api/locations/get_locations")
if rloc.status_code == 200:
    loc = len(rloc.json())

cols = st.columns(3)
with cols[0]:
    ui.metric_card(title="Devices", content=cmps, description="Detected devices", key="devices")
with cols[1]:
    ui.metric_card(title="Locations", content=loc, description="Available locations", key="locations")
with cols[2]:
    ui.metric_card(title="Last added Device", content=last_added, description="Last added device", key="ladev")

nxtcols = st.columns(1)
with nxtcols[0]:
	ui.metric_card(title="Last Alert", content=5, description="Last detected alert", key="laalert")
