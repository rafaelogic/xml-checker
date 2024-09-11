import streamlit as st
from files.json import load_required_fields
from files.xml import read_xml_content
from data.field_comparator import compare_fields, extract_all_fields
from ui.display import display_results

def render_page():
    # Sidebar for file upload
    st.sidebar.header("Upload Files")

    json_file = st.sidebar.file_uploader("Upload JSON file", type="json")
    xml_files = st.sidebar.file_uploader("Upload XML files", type="xml", accept_multiple_files=True)

    # Initialize session state for filter option if it doesn't exist
    if 'show_all_fields' not in st.session_state:
        st.session_state.show_all_fields = "Show All"

    # Initialize session state for results if it doesn't exist
    if 'results' not in st.session_state:
        st.session_state.results = []

    if 'columns_to_show' not in st.session_state:
        st.session_state.columns_to_show = []

    # Button to start check
    if st.sidebar.button('Start Check'):
        if not xml_files:
            st.error("Please upload at least one XML file.")
        else:
            required_fields = load_required_fields(json_file)
            if required_fields is None:
                st.error("Failed to load required fields from JSON.")
            else:
                results = []
                for xml_file in xml_files:
                    xml_content = read_xml_content(xml_file)
                    if xml_content:
                        fields = extract_all_fields(xml_content)
                        file_results = compare_fields(fields, required_fields)
                        results.append((xml_file.name, *file_results))
                
                st.session_state.results = results
                st.session_state.show_all_fields = "Show All"

                # Get all column names for the dropdown
                if results:
                    all_columns = list(required_fields.keys())
                    st.session_state.all_columns = all_columns

    # Display results and filter option only if results exist
    if st.session_state.results:
        st.session_state.show_all_fields = st.checkbox('Show All Fields', value=True)

        # Multi-select for choosing columns to show
        if 'all_columns' in st.session_state:
            st.session_state.columns_to_show = st.multiselect(
                'Select Columns to Display',
                st.session_state.all_columns,
                default=st.session_state.all_columns
            )

        display_results(st.session_state.results, st.session_state.show_all_fields, st.session_state.columns_to_show)
    else:
        st.info("Please upload a JSON file and XML files in the sidebar to get started.")