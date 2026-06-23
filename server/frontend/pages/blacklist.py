import requests
import streamlit as st
import streamlit_shadcn_ui as ui


cert = "server.crt"


st.title("Blacklist Devices")

st.html(
    "<p>Devices that are blocked from registering or communicating with the platform.</p>"
)

def mapComputers(computers):
    computer_map = {}
    for computer in computers:
        computer_map[computer["computername"]] = computer["computer_id"]
    return computer_map

rcmp = requests.get("https://127.0.0.1:8000/api/computers/live", verify=cert)
if rcmp.status_code == 200:
    computers = rcmp.json()
else:
    computers = []

if computers:
    st.html("<h3>Select a device to Blacklist</h3>")
    computer_map = mapComputers(computers)
    
    choice = ui.select(options=computer_map.keys())
    reason = ui.input(type='text', placeholder="Reason", key="input1")
    if st.button("Blacklist", type="primary"):
        r = requests.patch("https://127.0.0.1:8000/api/computers/blacklist", json={"computer_id": computer_map[choice], "blacklist_state": True, "blacklist_reason": reason}, verify=cert)
        if r.status_code == 200:
            st.success(f"Device blacklisted successfully !")
            st.rerun()
        else:
            st.error("An unknown error occurred, check your agents and try again")
else:
    st.html("<h3>Select a device to Blacklist</h3>")
    computer_map = {"None": "None"}
    
    choice = ui.select(options=computer_map.keys())
    reason = ui.input(type='text', placeholder="Reason", key="input1")
    if st.button("Blacklist", type="primary"):
        st.error("Null device selected")


st.divider()



st.html("<h3>Blacklisted Devices</h3>")

rcmp = requests.get("https://127.0.0.1:8000/api/computers/blacklisted", verify=cert)
if rcmp.status_code == 200:
    computers = rcmp.json()

data = []

for computer in computers:
    if computer["location_id"]:
        r = requests.get(f"https://127.0.0.1:8000/api/locations/getlocbyid?location_id={computer['location_id']}", verify=cert)
        loc = r.json()
        data.append({"Computer ID": computer["computer_id"], "Computer Name": computer["computername"], "Location": loc, "OS": computer["os"], "Status": "Online" if computer["is_alive"] else "Offline"})
    else:
        data.append({"Computer ID": computer["computer_id"], "Computer Name": computer["computername"], "Location": "NULL", "OS": computer["os"], "Status": "Online" if computer["is_alive"] else "Offline"})

    col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
    col1.write("AgentID")
    col2.write("Agent")
    col3.write("Location")
    col4.write("Status")
    col5.write("Action")
    for device in data:
        col1.write(device["Computer ID"])
        col2.write(device["Computer Name"])
        col3.write(device["Location"])
        col4.write(device["Status"])

        if col5.button("Remove", key=f"connect_{device['Computer Name']}"):
            r = requests.patch("https://127.0.0.1:8000/api/computers/blacklist", json={"computer_id": device["Computer ID"], "blacklist_state": False}, verify=cert)
            print()
            if r.status_code == 200:
                st.success(f"Removed {device['Computer Name']} from blacklist")
            else:
                st.error("An unknown error occurred, check your agents and try again")
            st.rerun()