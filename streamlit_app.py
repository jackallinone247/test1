import streamlit as st


#---Page Setup----

about_page = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True,
)

CSVagent_page = st.Page(
    page="views/CSVagent.py",
    title="CSV-Agent",
    icon=":material/bar_chart:",
)

PDFagent_page = st.Page(
    page="views/PDFagent.py",
    title="PDF-Agent",
    icon=":material/document_search:",
)

# --- Naviagation Setup (w/o section) ---

# pg = st.navigation(pages=[about_page,dashboard_page,chatbot_page])

# --- Naviagation Setup (w section) ---

pg = st.navigation(
    {   
        "Info": [about_page],
        "Projects": [CSVagent_page,PDFagent_page],
    }
)

# shared on all pages

st.logo("assets/logo.png")

#--- Run Navigation ---
pg.run()