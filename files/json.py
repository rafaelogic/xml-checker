import json
import streamlit as st

def load_required_fields(json_file):
    if json_file is None:
        return None
    
    try:
        data = json.load(json_file)
        # Convert the list to a dictionary
        required_fields = {field: None for field in data['required_fields']}
        return required_fields
    except Exception as e:
        st.error(f"Error loading JSON file: {e}")
        return None