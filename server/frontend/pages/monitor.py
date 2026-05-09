import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from code_editor import code_editor

st.header("Monitor your infrastructure")


st.html("<h2>Choose a device </h2>")
choice = ui.select(options=["Apple", "Banana", "Orange"])


st.html(f"<h2>Current {choice} metrics </h2>")

v = 5


cols = st.columns(3)
with cols[0]:
    ui.metric_card(title="CPU Usage", content=v, description="Current CPU usage", key="cpu")
with cols[1]:
    ui.metric_card(title="Memory Usage", content=v, description="Current memory usage", key="ram")
with cols[2]:
    ui.metric_card(title="Boot time", content=v, description=f"When {choice} was last started", key="ladev")


data = [
    {"Users": "Paid", "Disks": "INV001", "Processes Count": "500", "OS": "Credit Card"},
]


df = pd.DataFrame(data)

st.table(df)

st.html(f"<h3>Networking</h3>")

networking = [
    {"Network Interfaces": "Paid", "IP Addresses": "INV001"},
]


df2 = pd.DataFrame(networking)

st.table(df2)

st.html(f"<h2>Execute shell commands on {choice}</h2>")
response = code_editor("# Write You commands here", response_mode="debounce")

if st.button("Execute"):
    st.code(response['text'])

st.html(f"<h2>Open a remote session on {choice}</h2>")

if st.button("Open a session"):
    st.write("Why hello there")