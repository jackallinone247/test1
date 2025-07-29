import streamlit as st


#---Page Setup----

about_page = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True,
)

chatbot_page = st.Page(
    page="views/chatbot.py",
    title="ChatBot",
    icon=":material/smart_toy:",
)

dashboard_page = st.Page(
    page="views/sales_dashboard.py",
    title="Sales Dashboard",
    icon=":material/bar_chart:",
)

# --- Naviagation Setup (w/o section) ---

# pg = st.navigation(pages=[about_page,dashboard_page,chatbot_page])

# --- Naviagation Setup (w section) ---

pg = st.navigation(
    {   
        "Info": [about_page],
        "Projects": [dashboard_page,chatbot_page],
    }
)

# shared on all pages

st.logo("assets/logo.png")

#--- Run Navigation ---
pg.run()