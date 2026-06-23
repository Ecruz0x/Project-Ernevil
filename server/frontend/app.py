import streamlit as st

st.set_page_config(
    page_title="Ernevil",
    page_icon=":material/info:",
    layout="wide",
)

# Login page
login_page = st.Page(
    "pages/login.py",
    title="Login",
    icon=":material/login:",
    default=("token" not in st.session_state),
)

# Protected pages
overviewPage = st.Page(
    "pages/overviewpage.py",
    title="Overview",
    icon=":material/dashboard:",
    default=("token" in st.session_state),
)

KeyComputersPage = st.Page(
    "pages/keygen.py",
    title="Generate a secret key",
    icon=":material/lock:",
)

AvComputersPage = st.Page(
    "pages/listdev.py",
    title="Available Devices",
    icon=":material/devices:",
)

monitorComputersPage = st.Page(
    "pages/monitor.py",
    title="Monitor Devices",
    icon=":material/check_circle:",
)

blacklistComputersPage = st.Page(
    "pages/blacklist.py",
    title="Blacklist Devices",
    icon=":material/dangerous:",
)

locations = st.Page(
    "pages/listlocations.py",
    title="Locations",
    icon=":material/home_pin:",
)

addLocations = st.Page(
    "pages/addlocations.py",
    title="Add Locations",
    icon=":material/add_location:",
)

generateComputerReports = st.Page(
    "pages/reports.py",
    title="Computer Report",
    icon=":material/description:",
)

networkAlerts = st.Page(
    "pages/netalerts.py",
    title="Alerts and Notifications",
    icon=":material/notification_important:",
)

if "token" not in st.session_state:
    pg = st.navigation([login_page])
else:
    pg = st.navigation(
        {
            "": [overviewPage],
            "IAM": [KeyComputersPage],
            "Computers & Reports": [
                AvComputersPage,
                monitorComputersPage,
                blacklistComputersPage,
                generateComputerReports,
            ],
            "Locations": [locations, addLocations],
            "Alerts": [networkAlerts],
        }
    )

pg.run()