import streamlit as st
from screens import xml_checker, xml_comparer

def main():
    st.set_page_config(page_title='XML Field Checker', layout="wide")

    col1, col2, col3 = st.columns(3)

    # Navbar for navigation
    with col1:
        page = st.selectbox("Navigation", ["XML Field Checker", "Compare XML Files"])
    with col2:
        st.write("")
    with col3:
        st.write("")

    if page == "XML Field Checker":
        xml_checker.render_page()

    elif page == "Compare XML Files":
        xml_comparer.render_page()

if __name__ == "__main__":
    main()