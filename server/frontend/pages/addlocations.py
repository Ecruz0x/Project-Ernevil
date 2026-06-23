import streamlit as st
import streamlit_shadcn_ui as ui
import requests


def addLoc(loc_name, sev):
	r = requests.post("https://127.0.0.1:8000/api/locations", json = {"location_name": loc_name, "severity": sev}, verify="server.crt")
	if r.status_code == 200:
		st.success("Location has been saved successfully!")
	else:
		st.error("Cannot add location. Please check your location name and try again.")

st.title("Add locations")
st.html("<p>Organize and manage locations to group devices, simplify administration, and improve infrastructure monitoring.</p>")

st.text("Location name :")
loc_name = ui.input(type='text', placeholder="Location name", key="input1")
st.text("Severity :")
sev = ui.select(options=["Critical", "Medium", "Low"])

if st.button('Add location'):
	addLoc(loc_name, sev)
