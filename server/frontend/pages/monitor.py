import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from code_editor import code_editor
import requests, time
from st_aggrid import AgGrid

cert = "server.crt"

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

st.header("Monitor your infrastructure")


if computers:
    st.html("<h2>Select a device (only online devices are displayed)</h2>")
    computer_map = mapComputers(computers)
    
    choice = ui.select(options=computer_map.keys())


    st.html(f"<h2>Current {choice} metrics </h2>")

    v = 5
    # Memory Usage
    rmem = requests.get(f"https://127.0.0.1:8000/api/computers/mem?computer_id={computer_map[choice]}", verify=cert)
    if rmem.status_code == 200:
        memdata = rmem.json()["usage"]
        memdata = str(memdata) + "%"
    else:
        memdata = "Unavailable"

    # Boottime
    rcmpb = requests.get(f"https://127.0.0.1:8000/api/computers/c?computer_id={computer_map[choice]}", verify=cert)
    if rcmpb.status_code == 200:
        boottime = rcmpb.json()["boottime"]
        os = rcmpb.json()["os"]
    else:
        boottime = "Unavailable"


    @st.fragment(run_every="5s")
    def live_metrics(choice):
        cols = st.columns(3)
        rmem = requests.get(f"https://127.0.0.1:8000/api/computers/mem?computer_id={computer_map[choice]}", verify=cert)
        if rmem.status_code == 200:
            memdata = rmem.json()["usage"]
            memdata = str(memdata) + "%"
        else:
            memdata = "Unavailable"

        rcpu = requests.get(f"https://127.0.0.1:8000/api/computers/cpu?computer_id={computer_map[choice]}", verify=cert)
        if rcpu.status_code == 200:
            cpu_usage = rcpu.json()["cpu_usage"]
        else:
            cpu_usage = "Unavailable"

        rcmpb = requests.get(f"https://127.0.0.1:8000/api/computers/c?computer_id={computer_map[choice]}", verify=cert)
        if rcmpb.status_code == 200:
            boottime = rcmpb.json()["boottime"]
            os = rcmpb.json()["os"]
        else:
            boottime = "Unavailable"
            os = "Unavailable"
        with cols[0]:
            ui.metric_card(title="CPU Usage", content=str(cpu_usage) + "%", description="Current CPU usage", key="cpu")
        with cols[1]:
            ui.metric_card(title="Memory Usage", content=memdata, description="Current memory usage", key="ram")
        with cols[2]:
            ui.metric_card(title="Boot time", content=boottime, description=f"When {choice} was last started", key="ladev")

    live_metrics(choice)


    ps_count = len(requests.get(f"https://127.0.0.1:8000/api/computers/ps?computer_id={computer_map[choice]}", verify=cert).json())
    @st.fragment(run_every="15s")
    def processes_scraper():
        # Processes scraper
        try:
            rps = requests.get(f"https://127.0.0.1:8000/api/computers/ps?computer_id={computer_map[choice]}", verify=cert)
            if rps.status_code == 200:
                ps_data = rps.json()
            data_ps = []
            for ps in ps_data:
                temp_d = {}
                temp_d["PID"] = str(ps["pid"])
                temp_d["Process"] = ps["name"]
                temp_d["User"] = ps["username"] if ps["username"] else "Null"
                data_ps.append(temp_d)

            ps_df = pd.DataFrame(data_ps)
            AgGrid(
                ps_df,
                fit_columns_on_grid_load=True,
                enable_enterprise_modules=True
            )
        except Exception as e:
            return st.write("Unknown Error, please refresh the page and try again.")
    # Users scraper
    try:
        rusers = requests.get(f"https://127.0.0.1:8000/api/computers/cusers?computer_id={computer_map[choice]}", verify=cert)
        if rusers.status_code == 200:
            users = rusers.json()
    except Exception as e:
        st.write("Unknown Error, please refresh the page and try again.")
        
    # Disks scraper
    try:
        rdsk = requests.get(f"https://127.0.0.1:8000/api/computers/hd?computer_id={computer_map[choice]}", verify=cert)
        if rdsk.status_code == 200:
            dsk_data = rdsk.json()
    except Exception as e:
        st.write("Unknown Error, please refresh the page and try again.")

    # NetIF scraper
    try:
        rnet = requests.get(f"https://127.0.0.1:8000/api/computers/net?computer_id={computer_map[choice]}", verify=cert)
        if rnet.status_code == 200:
            net_data = rnet.json()
    except Exception as e:
        st.write("Unknown Error, please refresh the page and try again.")

    data = [
        {"Users count": str(len(users)), "Partition count": str(len(dsk_data)), "Processes Count": str(ps_count), "OS": os},
    ]

    df_general = pd.DataFrame(data)

    st.table(df_general)

    st.html(f"<h3>Processes</h3><p style='font-size: 17px;'>Visualize and analyze processes on <strong>{choice}</strong></p>")
    processes_scraper()
    st.html(f"<h3>Partitions</h3>")
    disk_data = []

    for disk in dsk_data:
        d = {}
        d["Partition Name"] = disk["partitionname"]
        d["Mount Point"] = disk["mountpoint"]
        d["File System"] = disk["fstype"]
        disk_data.append(d)

    df_dsk = pd.DataFrame(disk_data)

    st.table(df_dsk)


    st.html(f"<h3>Networking</h3>")

    networking = []
    for interface in net_data:
        temp_d = {}
        temp_d["Network Interface"] = interface["ifname"]
        temp_d["IPv4 Address"] = interface["ipaddr"]
        networking.append(temp_d)


    df_net = pd.DataFrame(networking)

    st.table(df_net)

    # Commands execution
    st.html(f"<h2>Execute shell commands on {choice}</h2>")
    response = code_editor("# Write You commands here", response_mode="debounce")
    computers = requests.get("https://127.0.0.1:8000/api/computers/live", verify = cert).json()
    if st.button("Execute"):
        computer_map = mapComputers(computers)
        if choice in computer_map.keys():
            rcmds = requests.post("https://127.0.0.1:8000/api/commands", json = {"computer_id": computer_map[choice], "command": response['text']}, verify = cert)
            try:
                result = rcmds.json()["result"]
                output = str(result)
                st.code(output)
            except Exception as e:
                st.code("Execution error, please check your agents and try again.")
        else:
            st.code("Execution error, please check your agents and try again.")
            st.rerun()

    st.html(f"<h2>Open a remote session on {choice}</h2>")

    if st.button("Open a session"):
        st.write("Why hello there")

    st.html(f"<h2>Shutdown or restart {choice}</h2>")


    left, right = st.columns(2)

    if left.button(f"Shutdown", width="stretch", key="left_btn"):
        requests.post("https://127.0.0.1:8000/api/shutdown", json = {"computer_id": computer_map[choice]}, verify = cert)

    if right.button(f"Restart", width="stretch", key="right_btn"):
        requests.post("https://127.0.0.1:8000/api/restart", json = {"computer_id": computer_map[choice]}, verify = cert)

        



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
