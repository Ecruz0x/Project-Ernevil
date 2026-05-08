import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from code_editor import code_editor

st.header("Monitor your infrastructure")


st.html("<h2>Choose a device </h2>")
choice = ui.select(options=["Apple", "Banana", "Orange"])


st.html("<h2>Current **Device's** metrics </h2>")

v = 5


cols = st.columns(3)
with cols[0]:
    ui.metric_card(title="CPU Usage", content=v, description="Current CPU usage", key="cpu")
with cols[1]:
    ui.metric_card(title="Memory Usage", content=v, description="Current memory usage", key="ram")
with cols[2]:
    ui.metric_card(title="Boot time", content=v, description="When the device was last started", key="ladev")


data = [
    {"Users": "Paid", "Disks": "INV001", "Network Interfaces": "500", "OS": "Credit Card"},
]


df = pd.DataFrame(data)

st.table(df)



st.html("<h2>Execute shell commands on **device**</h2>")
response = code_editor("print('Hello, World!')", lang="bash")

if response['type'] == "submit":
    st.write("Command submitted!")
    st.code(response['text'], language='bash')

st.html("<h2>Open a remote session on **device**</h2>")

if st.button("Open a session"):
    st.write("Why hello there")