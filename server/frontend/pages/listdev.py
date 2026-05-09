import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui




st.header("Available Devices")



data = [
    {"Computer Name": "Paid", "Location": "INV001", "OS": 500, "Status": "Credit Card"},
]


df = pd.DataFrame(data)

ui.table(data=df, maxHeight=200)

if st.button("Monitor your devices"):
	st.switch_page("pages/monitor.py")



st.html("""<h3>Note</h3>
	<ul>
		<li>If a computer appears unavailable, please verify your administrator credentials and restart the agent software on the affected machine.</li>
	</ul>""")

st.html("""<h3>Report issues</h3>
<p>Encountered a bug? Please open an issue on GitHub so we can track and resolve it.</p>""")


ui.link_button(text="Issues - Github", url="https://github.com/Ecruz0x/Project-Ernevil/issues/", key="link_btn")
