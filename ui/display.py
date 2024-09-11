import streamlit as st
import pandas as pd

def display_results(results, show_all_fields, columns_to_show):
    for file_name, missing_in_file1, _, _ in results:  # We only care about `missing_in_file1`
        st.header(f"Results for {file_name}")

        # Convert the set of missing fields into a DataFrame for display
        df_missing_in_file1 = pd.DataFrame(missing_in_file1, columns=['Fields Missing in XML'])
        df_missing_in_file1_sorted = df_missing_in_file1.sort_values(by='Title')

        # Filter columns if necessary (though in this case, there is only one column)
        if columns_to_show:
            df_missing_in_file1 = df_missing_in_file1_sorted[df_missing_in_file1_sorted.columns.intersection(columns_to_show)]

        # Show all fields or only missing ones depending on the user's choice
        if show_all_fields:
            st.write("Fields Missing in XML:")
            st.write(df_missing_in_file1_sorted)
        else:
            if df_missing_in_file1_sorted.empty:
                st.write("No fields missing in this XML file.")
            else:
                st.write("Fields Missing in XML:")
                st.write(df_missing_in_file1_sorted)