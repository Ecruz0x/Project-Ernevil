import requests
import streamlit as st



cert = "server.crt"
st.html(
            "<h1>Locations</h1><p>Organize computers into logical groups for easier administration.</p>"
        )

try:
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }
    r = requests.get("https://127.0.0.1:8000/api/locations", verify=cert, headers=headers)
    rcmp = requests.get("https://127.0.0.1:8000/api/computers", verify=cert, headers=headers)

    if r.status_code != 200 or rcmp.status_code != 200:
        st.error("Failed to load data.")
        st.stop()

    locations = r.json()
    computers = rcmp.json()

    if "selected_location" in st.session_state:

        location = next(
            (
                loc
                for loc in locations
                if loc["id"] == st.session_state.selected_location
            ),
            None
        )

        if location is None:
            del st.session_state["selected_location"]
            st.rerun()

        @st.dialog("Add Computers")
        def add_computers_dialog():

            st.write(
                "Select one or more computers to add to this location."
            )

            available = [
                c for c in computers
                if c.get("location_id") != location["id"]
            ]

            selected = st.multiselect(
                "Available Computers",
                options=available,
                format_func=lambda c: c["computername"]
            )

            st.caption(
                "Only selected computers will be assigned to this location."
            )

            if st.button("Add"):

                requests.post(
                    "https://127.0.0.1:8000/api/locations/set", verify = cert, headers=headers,
                    json={
                        "location_id": location["id"],
                        "computer_id": [
                            c["computer_id"]
                            for c in selected
                        ]
                    }
                )

                st.rerun()

        st.button(
            "Back",
            on_click=lambda: st.session_state.pop(
                "selected_location", None
            )
        )

        st.html(f"<h2>{location['name']}</h2>")

        st.html(
            "<p>Browse, monitor, and manage all computers associated with this location.</p>"
        )

        st.divider()

        location_computers = requests.get(
            f"https://127.0.0.1:8000/api/computers/location?location_id={location['id']}", verify = cert, headers=headers
        ).json()

        st.html("<h2>Assigned Computers:</h2><p>Add existing computers to this location or remove them when no longer needed.</p>")

        for computer in location_computers:

            cols = st.columns([8, 1])

            with cols[0]:
                st.write(computer)

            with cols[1]:
                if st.button(
                    "...",
                    key=f"remove_{computer}",
                    help="Remove computer from this location"
                ):
                    requests.delete(
                        "https://127.0.0.1:8000/api/locations/delete", headers=headers,
                        verify=cert,
                        json={
                            "computer": computer
                        }
                    )
                    st.rerun()

        if not location_computers:
            st.info(
                "No computers are currently assigned to this location."
            )
        if st.button("Add Computer"):
            add_computers_dialog()

    else:
        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }
        st.html(
            "<h1>Locations</h1><p>Organize computers into logical groups for easier administration.</p>"
        )

        if not locations:
            st.info("No locations available.")
        else:
            st.caption(f"{len(locations)} location(s)")

        for location in locations:

            cols = st.columns([8, 1])

            with cols[0]:
                if st.button(
                    location["name"],
                    key=f"location_{location['id']}",
                    use_container_width=True
                ):
                    st.session_state.selected_location = location["id"]
                    st.rerun()

            with cols[1]:
                if st.button(
                    "...",
                    key=f"menu_{location['id']}",
                    help="Delete location"
                ):
                    requests.delete(
                         f"https://127.0.0.1:8000/api/locations/delete_loc", verify=cert, json={"location_id":location['id']}, headers=headers
                    )
                    st.rerun()

            st.caption(
                f"Severity: {location['severity']}"
            )

except Exception as e:
    st.error("An unknown error occurred, check your agents and try again")