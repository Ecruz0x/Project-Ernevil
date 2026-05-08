import streamlit as st
from streamlit_extras.resizable_columns import resizable_columns
from streamlit_extras.card_selector import *
import streamlit_shadcn_ui as ui


st.header("General Overview")
st.text("""
Ernevil is an open-source monitoring platform designed to help administrators manage and monitor computers across a Local Area Network, with cloud support planned for future releases. It focuses on simplicity, automation, and centralized system management while remaining fully transparent and community-driven.""")


ui.link_button(text="Github", url="https://github.com/Ecruz0x/Project-Ernevil/", key="link_btn")


st.header("How To Use")

selected = card_selector(
    [
        dict(
            icon=":material/hub:",
            title="Agents",
            description="Deploy the agent software to your computers",
        ),
        dict(
            icon=":material/computer:",
            title="Server",
            description="Run the server's software on the administration machine",
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

v = 30

cols = st.columns(3)
with cols[0]:
    ui.metric_card(title="Devices", content=v, description="Detected computers", key="computers")
with cols[1]:
    ui.metric_card(title="Locations", content=v, description="Available locations", key="locations")
with cols[2]:
    ui.metric_card(title="Last Device", content=v, description="Last added computer", key="lacomputer")

nxtcols = st.columns(1)
with nxtcols[0]:
	ui.metric_card(title="Last Alert", content=v, description="Last detected alert", key="laalert")
