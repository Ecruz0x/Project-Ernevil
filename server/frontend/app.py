import streamlit as st




overviewPage = st.Page(
	"pages/overview_page.py", title="Overview", default=True, icon=":material/dashboard:"
)


AvComputersPage = st.Page(
    "pages/monitor_computers.py", title="Monitor Computers", icon=":material/devices:"
)

blacklistComputersPage = st.Page(
    "pages/blacklist_computers.py", title="Blacklist Computers", icon=":material/dangerous:"
)


locations = st.Page(
    "pages/list_locations.py", title="Locations", icon=":material/home_pin:"
)


addLocations = st.Page(
    "pages/add_locations.py", title="Add Locations", icon=":material/add_location:"
)

generateComputerReports = st.Page(
    "pages/c_reports.py", title="Computer Report", icon=":material/description:"
)

networkAlerts = st.Page(
	"pages/netalerts.py", title="Network Alerts", icon=":material/notification_important:"
)



pg = st.navigation(

    {
    	"": [overviewPage],
        "Computers & Reports": [AvComputersPage, blacklistComputersPage, generateComputerReports],
        "Locations": [locations, addLocations],
        "Alerts": [networkAlerts]
    }
    
)


pg.run()