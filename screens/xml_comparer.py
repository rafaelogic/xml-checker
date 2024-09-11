import streamlit as st
import pandas as pd
from data.xml_processor import process_xml_content

def render_page():
    st.sidebar.header("Upload Files")

    xml_file1 = st.sidebar.file_uploader("Upload XML File 1", type=["xml"])
    xml_file2 = st.sidebar.file_uploader("Upload XML File 2", type=["xml"])

    if xml_file1 and xml_file2:
        xml_content1 = xml_file1.read().decode('utf-8')
        xml_content2 = xml_file2.read().decode('utf-8')

        file1_name = xml_file1.name
        file2_name = xml_file2.name

        compare_values = st.sidebar.radio(
            "Select Comparison Type", 
            options=["Missing Fields", "Field Values"]
        )

        if st.sidebar.button("Start Comparison"):
            results = process_xml_content(xml_content1, xml_content2, file1_name, file2_name, compare_values)
            
            if compare_values == "Missing Fields":
                st.subheader("Compare Missing Fields")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"Missing Fields in {file1_name}:")
                    st.write(", ".join(results['missing_in_file1']))
                
                with col2:
                    st.write(f"Missing Fields in {file2_name}")
                    st.write(", ".join(results['missing_in_file2']))
                
            elif compare_values == "Field Values":
                unique_titles = results['field_value_mismatches']['Title'].unique()
                
                st.subheader("Compare Field Values")

                if not results['field_value_mismatches'].empty:
                    # Highlight rows by title and display dataframe
                    styled_df = highlight_rows_by_title(results['field_value_mismatches'])
                    st.write(f"{len(unique_titles)} Properties having field value mismatches between {len(results['field_value_mismatches'])} rows:")
                    st.dataframe(styled_df)

                    # Option to render the table as HTML
                    if st.button("Display Results in HTML"):
                        html_table = generate_html_table(results['field_value_mismatches'], file1_name, file2_name)
                        # Print HTML to logs for debugging
                        print(html_table)  # To check in logs if HTML is being generated correctly
                        st.markdown(html_table, unsafe_allow_html=True)
                        st.write("You can print this page and save it as PDF in your browser.")
                else:
                    st.write("No mismatches found between the field values.")
    else:
        st.info("Please upload a pair of XML files in the sidebar to get started.")


def highlight_rows_by_title(df):
    def style_func(row):
        if row['Title'] in title_colors:
            return [f'background-color: {title_colors[row["Title"]]}'] * len(row)
        return [''] * len(row)
    
    title_colors = {}
    unique_titles = df['Title'].unique()
    colors = ['#f5f5f5', '#ffffff']
    
    for i, title in enumerate(unique_titles):
        title_colors[title] = colors[i % len(colors)]
    
    return df.style.apply(style_func, axis=1)

# New function to generate HTML table
def generate_html_table(df, file1_name, file2_name):
    # Initialize the HTML table with headers
    html = f"""
    <h2 style="text-align:center;">XML Comparison Report</h2>
    <p style="text-align:center;">Comparison between {file1_name} and {file2_name}</p>
    <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
        <tr>
            <th>Property Name</th>
            <th>{file1_name}</th>
            <th>{file2_name}</th>
        </tr>
    """

    # Populate the rows of the table
    for index, row in df.iterrows():
        html += f"""
        <tr>
            <td>{row['Title']}</td>
            <td>{row['Value1']}</td>
            <td>{row['Value2']}</td>
        </tr>
        """

    # Close the table
    html += "</table>"

    return html


if __name__ == "__main__":
    render_page()