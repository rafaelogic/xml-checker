from data.field_comparator import extract_all_fields, compare_fields, compare_field_structure, compare_field_structure_reverse
from data.value_comparator import compare_field_values

def process_xml_content(xml_content1, xml_content2, file1_name, file2_name, compare_values):
    fields1 = extract_all_fields(xml_content1)
    fields2 = extract_all_fields(xml_content2)
    
    if compare_values == "Missing Fields":
        # Use first XML as reference structure
        comparison_result = compare_field_structure(xml_content1, xml_content2)
        return {
            'reference_fields': comparison_result['reference_fields'],
            'missing_fields': comparison_result['missing_in_second_file'],
            'total_reference_fields': comparison_result['total_reference_fields'],
            'total_missing': comparison_result['total_missing']
        }
    
    elif compare_values == "Missing Fields (Reverse)":
        # Use second XML as reference structure (reverse check)
        comparison_result = compare_field_structure_reverse(xml_content1, xml_content2)
        return {
            'reference_fields': comparison_result['reference_fields'],
            'missing_fields': comparison_result['missing_in_first_file'],
            'total_reference_fields': comparison_result['total_reference_fields'],
            'total_missing': comparison_result['total_missing']
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