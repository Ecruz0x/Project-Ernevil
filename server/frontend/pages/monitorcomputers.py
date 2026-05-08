import streamlit as st
import streamlit_shadcn_ui as ui


st.header("Monitor your infrastructure")


st.text("Choose a device :")
choice = ui.select(options=["Apple", "Banana", "Orange"])



v = 5


cols = st.columns(3)
with cols[0]:
    ui.metric_card(title="CPU Usage", content=v, description="Current CPU usage", key="cpu")
with cols[1]:
    ui.metric_card(title="Memory Usage", content=v, description="Current memory usage", key="ram")
with cols[2]:
    ui.metric_card(title="Boot time", content=v, description="When the computer was last started", key="lacomputer")