import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from code_editor import code_editor
import requests, time

rcmp = requests.get("http://127.0.0.1:8000/api/computers/live")
if rcmp.status_code == 200:
    computers = rcmp.json()
else:
    computers = []

st.header("Monitor your infrastructure")




if computers:
    st.html("<h2>Choose a device (Only online devices will appear) </h2>")
    computer_map = {}
    for computer in computers:
        computer_map[computer["computername"]] = computer["computer_id"]

    choice = ui.select(options=computer_map.keys())


    st.html(f"<h2>Current {choice} metrics </h2>")

    v = 5
    # Memory Usage
    rmem = requests.get(f"http://127.0.0.1:8000/api/computers/mem?computer_id={computer_map[choice]}")
    if rmem.status_code == 200:
        memdata = rmem.json()["usage"]
        memdata = str(memdata) + "%"
    else:
        memdata = "Unavailable"

    # Boottime
    rcmpb = requests.get(f"http://127.0.0.1:8000/api/computers/c?computer_id={computer_map[choice]}")
    if rcmpb.status_code == 200:
        boottime = rcmpb.json()["boottime"]
    else:
        boottime = "Unavailable"

    cols = st.columns(3)
    with cols[0]:
        ui.metric_card(title="CPU Usage", content=v, description="Current CPU usage", key="cpu")
    with cols[1]:
        ui.metric_card(title="Memory Usage", content=memdata, description="Current memory usage", key="ram")
    with cols[2]:
        ui.metric_card(title="Boot time", content=boottime, description=f"When {choice} was last started", key="ladev")


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


else:
    st.html("<h2>No devices are currently detected. Please verify that your agents are running and that the credentials are configured correctly.</h2>")
    cols = st.columns(3)
    with cols[0]:
        ui.metric_card(title="CPU Usage", content="0.0%", description="Current CPU usage", key="cpu")
    with cols[1]:
        ui.metric_card(title="Memory Usage", content="0.0%", description="Current memory usage", key="ram")
    with cols[2]:
        ui.metric_card(title="Boot time", content="None", description=f"When computer was last started", key="ladev")
    data = [
        {"Users": "None", "Disks": "None", "Processes Count": "None", "OS": "None"},
    ]
    df = pd.DataFrame(data)
    st.table(df)

    st.html(f"<h3>Networking</h3>")

    networking = [
        {"Network Interfaces": "None", "IP Addresses": "None"},
    ]

    df2 = pd.DataFrame(networking)
    st.table(df2)