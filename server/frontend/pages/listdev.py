import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
import requests


cert = "server.crt"

st.header("Available Devices")

rcmp = requests.get("https://127.0.0.1:8000/api/computers", verify=cert)
if rcmp.status_code == 200:
    computers = rcmp.json()

data = []

for computer in computers:
	if computer["location_id"]:
		r = requests.get(f"https://127.0.0.1:8000/api/locations/getlocbyid?location_id={computer['location_id']}", verify=cert)
		loc = r.json()
		data.append({"Computer Name": computer["computername"], "Location": loc, "OS": computer["os"], "Status": "Online" if computer["is_alive"] else "Offline"})
	else:
		data.append({"Computer Name": computer["computername"], "Location": "NULL", "OS": computer["os"], "Status": "Online" if computer["is_alive"] else "Offline"})

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
