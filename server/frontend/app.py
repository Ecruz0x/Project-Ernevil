import streamlit as st
import streamlit_shadcn_ui as ui


welcome = st.Page(
    "pages/welcome.py",
    title = "Welcome to Ernevil",
    )

locations = st.Page(
    "pages/locations.py",
    title = "Locations"
    )

computers = st.Page(
    "pages/computers.py",
    title = "Computers"
    )


my_pages = [welcome, locations, computers]
st.title("Request manager")
st.logo("src/logo.png")

pg = st.navigation(my_pages)

pg.run()