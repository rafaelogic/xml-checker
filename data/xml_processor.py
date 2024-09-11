from data.field_comparator import extract_all_fields, compare_fields
from data.value_comparator import compare_field_values

def process_xml_content(xml_content1, xml_content2, file1_name, file2_name, compare_values):
    fields1 = extract_all_fields(xml_content1)
    fields2 = extract_all_fields(xml_content2)
    
    if compare_values == "Missing Fields":
        missing_fields_in_file1, missing_fields_in_file2, _ = compare_fields(fields1, fields2)
        return {
            'missing_in_file1': missing_fields_in_file1,
            'missing_in_file2': missing_fields_in_file2
        }
    
    elif compare_values == "Field Values":
        _, _, common_titles = compare_fields(fields1, fields2)
        field_value_mismatches_df = compare_field_values(fields1, fields2, common_titles, file1_name, file2_name)
        return {
            'field_value_mismatches': field_value_mismatches_df,
            'common_titles': compare_fields(fields1, fields2)
        }
    
    else:
        raise ValueError(f"Unknown comparison type: {compare_values}")