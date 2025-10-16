import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from data.xml_processor import process_xml_content

# Cache the expensive processing function
@st.cache_data(show_spinner=False)
def process_xml_content_cached(xml_content1, xml_content2, file1_name, file2_name, compare_values):
    return process_xml_content(xml_content1, xml_content2, file1_name, file2_name, compare_values)

def render_page():
    st.sidebar.header("Upload Files")

    xml_file1 = st.sidebar.file_uploader("Upload Reference XML (correct structure)", type=["xml"], help="This will be used as the reference structure")
    xml_file2 = st.sidebar.file_uploader("Upload XML to Compare", type=["xml"], help="This will be compared against the reference")
    
    # Add cache clear button
    if st.sidebar.button("🔄 Clear Cache", help="Clear cached results if you're experiencing issues"):
        st.cache_data.clear()
        st.sidebar.success("Cache cleared!")

    if xml_file1 and xml_file2:
        xml_content1 = xml_file1.read().decode('utf-8')
        xml_content2 = xml_file2.read().decode('utf-8')

        file1_name = xml_file1.name
        file2_name = xml_file2.name

        compare_values = st.sidebar.radio(
            "Select Comparison Type", 
            options=["Missing Fields", "Missing Fields (Reverse)", "Field Values"]
        )

        if st.sidebar.button("Start Comparison"):
            # Use cached function for performance
            results = process_xml_content_cached(xml_content1, xml_content2, file1_name, file2_name, compare_values)
            
            if compare_values == "Missing Fields":
                st.subheader("Field Structure Comparison")
                st.info(f"Using **{file1_name}** as the **Reference XML**")
                
                # Display summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Fields in Reference", results['total_reference_fields'])
                with col2:
                    st.metric("Missing Fields", results['total_missing'])
                with col3:
                    completion_rate = ((results['total_reference_fields'] - results['total_missing']) / results['total_reference_fields'] * 100) if results['total_reference_fields'] > 0 else 0
                    st.metric("Match Rate", f"{completion_rate:.1f}%")
                
                st.divider()
                
                # Create a comprehensive table for all fields
                missing_fields_set = set(results['missing_fields'])
                
                # Create table data with status indicators
                table_data = []
                for field in results['reference_fields']:
                    if field in missing_fields_set:
                        status = '✗'
                    else:
                        status = '✓'
                    table_data.append({
                        'Field Name': field,
                        f'Status in {file2_name}': status
                    })
                
                # Create comparison dataframe
                comparison_df = pd.DataFrame(table_data)
                
                # Display the table
                st.subheader("Field Comparison Table")
                st.dataframe(
                    comparison_df,
                    use_container_width=True,
                    hide_index=True,
                    height=min(600, (len(results['reference_fields']) + 1) * 35)
                )
                
                # Summary messages
                if not results['missing_fields']:
                    st.success(f"✅ Perfect match! All {results['total_reference_fields']} reference fields are present in {file2_name}.")
                else:
                    st.error(f"❌ {file2_name} is missing {results['total_missing']} out of {results['total_reference_fields']} fields from the reference.")
                    st.info("💡 Tip: To check for extra fields, reverse the file order (upload the current second file as the reference).")

                # Offer CSV export
                csv = comparison_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Comparison Table (CSV)", 
                    csv, 
                    file_name=f"field_comparison_{file1_name}_vs_{file2_name}.csv", 
                    mime="text/csv"
                )
            
            elif compare_values == "Missing Fields (Reverse)":
                st.subheader("Field Structure Comparison (Reverse)")
                st.info(f"Using **{file2_name}** as the **Reference XML**")
                
                # Display summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Fields in Reference", results['total_reference_fields'])
                with col2:
                    st.metric("Missing Fields", results['total_missing'])
                with col3:
                    completion_rate = ((results['total_reference_fields'] - results['total_missing']) / results['total_reference_fields'] * 100) if results['total_reference_fields'] > 0 else 0
                    st.metric("Match Rate", f"{completion_rate:.1f}%")
                
                st.divider()
                
                # Create a comprehensive table for all fields
                missing_fields_set = set(results['missing_fields'])
                
                # Create table data with status indicators
                table_data = []
                for field in results['reference_fields']:
                    if field in missing_fields_set:
                        status = '✗'
                    else:
                        status = '✓'
                    table_data.append({
                        'Field Name': field,
                        f'Status in {file1_name}': status
                    })
                
                # Create comparison dataframe
                comparison_df = pd.DataFrame(table_data)
                
                # Display the table
                st.subheader("Field Comparison Table")
                st.dataframe(
                    comparison_df,
                    use_container_width=True,
                    hide_index=True,
                    height=min(600, (len(results['reference_fields']) + 1) * 35)
                )
                
                # Summary messages
                if not results['missing_fields']:
                    st.success(f"✅ Perfect match! All {results['total_reference_fields']} reference fields are present in {file1_name}.")
                else:
                    st.error(f"❌ {file1_name} is missing {results['total_missing']} out of {results['total_reference_fields']} fields from the reference.")

                # Offer CSV export
                csv = comparison_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Comparison Table (CSV)", 
                    csv, 
                    file_name=f"field_comparison_reverse_{file2_name}_vs_{file1_name}.csv", 
                    mime="text/csv"
                )
            
            elif compare_values == "Field Values":
                unique_titles = results['field_value_mismatches']['Title'].unique()
                
                st.subheader("Compare Field Values")

                if not results['field_value_mismatches'].empty:
                    # Highlight rows by title and display dataframe
                    styled_df = highlight_rows_by_title(results['field_value_mismatches'])
                    st.write(f"{len(unique_titles)} Properties having field value mismatches between {len(results['field_value_mismatches'])} rows:")
                    st.dataframe(styled_df)

                    # Offer CSV export for field value mismatches
                    csv_mismatches = results['field_value_mismatches'].to_csv(index=False)
                    st.download_button("Download CSV", csv_mismatches, file_name="field_value_mismatches.csv", mime="text/csv")

                    # PDF generation with progress bar
                    if st.button("Generate PDF Report"):
                        progress = st.progress(0)  # Initialize the progress bar
                        pdf_data = generate_pdf_report_with_progress(results['field_value_mismatches'], file1_name, file2_name, progress)
                        st.download_button("Download PDF", data=pdf_data, file_name="field_value_mismatches.pdf", mime="application/pdf")
                        
                    # Option to render the table as HTML
                    if st.button("Display Results in HTML"):
                        html_table = generate_html_table(results['field_value_mismatches'], file1_name, file2_name)
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

# Function to generate HTML table
def generate_html_table(df, file1_name, file2_name):
    html = [f"""
    <h2 style="text-align:center;">XML Comparison Report</h2>
    <p style="text-align:center;">Comparison between {file1_name} and {file2_name}</p>
    <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
        <tr>
            <th>Property Name</th>
            <th>{file1_name}</th>
            <th>{file2_name}</th>
        </tr>
    """]
    
    for _, row in df.iterrows():
        html.append(f"""
        <tr>
            <td>{row['Title']}</td>
            <td>{row['Value1']}</td>
            <td>{row['Value2']}</td>
        </tr>
        """)

    html.append("</table>")
    return "".join(html)

# Function to generate PDF report with progress bar
def generate_pdf_report_with_progress(df, file1_name, file2_name, progress):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title and headers
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 50, f"XML Comparison Report: {file1_name} vs {file2_name}")
    
    # Column headers
    p.setFont("Helvetica-Bold", 10)
    y = height - 100
    p.drawString(100, y, "Title")
    p.drawString(300, y, file1_name)
    p.drawString(500, y, file2_name)
    y -= 20

    # Paginate rows with progress update
    total_rows = len(df)
    p.setFont("Helvetica", 10)
    for index, row in df.iterrows():
        if y < 100:  # Start new page if space runs out
            p.showPage()
            p.setFont("Helvetica", 10)
            y = height - 50

        # Write row data
        p.drawString(100, y, str(row['Title']))
        p.drawString(300, y, str(row['Value1']))
        p.drawString(500, y, str(row['Value2']))
        y -= 20

        # Update progress bar
        progress.progress((index + 1) / total_rows)

    p.save()

    buffer.seek(0)
    return buffer.getvalue()

if __name__ == "__main__":
    render_page()