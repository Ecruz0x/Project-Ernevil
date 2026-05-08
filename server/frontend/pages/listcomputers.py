import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
from streamlit_extras.stateful_button import *



st.header("Available Computers")



data = [
    {"Computer Id": "INV001", "Computer Name": "Paid", "OS": 500, "Status": "Credit Card"},
]


df = pd.DataFrame(data)

ui.table(data=df, maxHeight=200)

if button("Monitor your computers", key="button1"):
	pass



st.html("""<h3>Note</h3>
	<ul> If a computer isn't available, please check your administration credentails and restart the agent's software in the unavailable computer.</ul>""")

