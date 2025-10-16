import streamlit as st
from screens import xml_checker, xml_comparer, xml_field_explorer

def main():
    st.set_page_config(page_title='JSON-XML Comparer', layout="wide")

    col1, col2, col3 = st.columns(3)

    # Navbar for navigation
    with col1:
        page = st.selectbox("Navigation", ["JSON-XML Comparer", "Compare XML Files", "XML Field Explorer"])
    with col2:
        st.write("")
    with col3:
        st.write("")

    if page == "JSON-XML Comparer":
        xml_checker.render_page()

    elif page == "Compare XML Files":
        xml_comparer.render_page()
    
    elif page == "XML Field Explorer":
        xml_field_explorer.render_page()

if __name__ == "__main__":
    main()