import streamlit as st
import xml.etree.ElementTree as ET
from collections import Counter
import pandas as pd

def render_page():
    st.title("XML Field Explorer")
    st.markdown("Upload an XML file to explore its fields and values")
    
    # Sidebar for file upload
    st.sidebar.header("Upload XML File")
    xml_file = st.sidebar.file_uploader("Upload XML file", type="xml")
    
    if xml_file is not None:
        # Read and parse XML content
        xml_content = xml_file.read().decode('utf-8')
        
        try:
            root = ET.fromstring(xml_content)
            
            # Show available operations
            st.sidebar.header("Operations")
            operation = st.sidebar.selectbox("Select Operation", ["Get Field Values"])
            
            if operation == "Get Field Values":
                # Extract all unique field names from the XML
                all_fields = extract_all_field_names(root)
                
                if all_fields:
                    st.sidebar.header("Select Field")
                    selected_field = st.sidebar.selectbox("Choose a field to analyze", sorted(all_fields))
                    
                    if st.sidebar.button("Analyze Field"):
                        analyze_field_values(root, selected_field)
                else:
                    st.error("No fields found in the XML file.")
                    
        except ET.ParseError as e:
            st.error(f"Error parsing XML file: {str(e)}")
    else:
        st.info("Please upload an XML file in the sidebar to get started.")

def extract_all_field_names(root):
    """Extract all unique field names from the XML structure"""
    field_names = set()
    
    def traverse_element(element):
        # Add current element tag
        field_names.add(element.tag)
        
        # Recursively traverse all children
        for child in element:
            traverse_element(child)
    
    traverse_element(root)
    return field_names

def analyze_field_values(root, field_name):
    """Analyze values for a specific field in the XML"""
    st.subheader(f"Analysis for field: '{field_name}'")
    
    # Find all elements with the specified field name
    elements = root.findall(f".//{field_name}")
    
    if not elements:
        st.warning(f"No elements found with field name '{field_name}'")
        return
    
    # Extract values
    values = []
    empty_count = 0
    
    for element in elements:
        if element.text is not None and element.text.strip():
            values.append(element.text.strip())
        else:
            empty_count += 1
    
    # Count occurrences of each value
    value_counts = Counter(values)
    total_elements = len(elements)
    
    # Display summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Occurrences", total_elements)
    
    with col2:
        st.metric("Unique Values", len(value_counts))
    
    with col3:
        st.metric("Empty/Null Values", empty_count)
    
    with col4:
        st.metric("Non-Empty Values", len(values))
    
    # Display value distribution
    if value_counts:
        st.subheader("Value Distribution")
        
        # Create DataFrame for better display
        df_data = []
        for value, count in value_counts.most_common():
            percentage = (count / total_elements) * 100
            df_data.append({
                "Value": value,
                "Count": count,
                "Percentage": f"{percentage:.2f}%"
            })
        
        df = pd.DataFrame(df_data)
        
        # Display as table
        st.dataframe(df, use_container_width=True)
        
        # Show top values if there are many
        if len(value_counts) > 10:
            st.subheader("Top 10 Most Common Values")
            top_values = dict(value_counts.most_common(10))
            st.bar_chart(top_values)
        else:
            st.subheader("Value Distribution Chart")
            chart_data = {value: count for value, count in value_counts.items()}
            st.bar_chart(chart_data)
        
        # Provide download option
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name=f"{field_name}_analysis.csv",
            mime="text/csv"
        )
    
    # Show sample values if available
    if values:
        st.subheader("Sample Values")
        sample_size = min(10, len(values))
        sample_values = values[:sample_size]
        
        for i, value in enumerate(sample_values, 1):
            st.text(f"{i}. {value}")
        
        if len(values) > sample_size:
            st.info(f"Showing {sample_size} of {len(values)} non-empty values")

if __name__ == "__main__":
    render_page()