import streamlit as st
from forms.contact import contact_form



@st.dialog("Contact Me")
def show_contact_form():
    
    contact_form()

#--- Hero Section---

col1,col2 = st.columns(2, gap ="small", vertical_alignment='center')
with col1:
    st.image("./assets/logo.png",width=230)
with col2:
    st.title("AI Builds", anchor=False)
    st.write("AI Specialist, assisting enterprises by supporting AI-driven Insights")
    if st.button("✉ Contact Me"):
        show_contact_form()


# --- Experience & Qualifications ---
st.write("\n")
st.subheader("Experience & Qualifications", anchor=False)
st.write("""
            - 11 Years experince deriving Insights from Data
            - Stong hands-on experience and knowledg in Python,Excel,PowerBI and Streamlit)
            - Good Understanding of statistical principles and their respective applications
            - Excellent team-player and displaying a strong sense of initiative on tasks
            """)

# --- Skills ---
st.write("\n")
st.subheader("Skills", anchor=False)
st.write("""
            - Programming: Python, Pyspark, SQL, VBA
            - Data visualization: PowerBI, MS Excel, Plotly
            - Modeling: Logistic Regression, Linear regression, Decision trees
            """)            