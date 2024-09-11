import streamlit as st

def read_xml_content(xml_file):
    try:
        return xml_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading XML file {xml_file.name}: {e}")
        return None