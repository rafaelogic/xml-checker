import xml.etree.ElementTree as ET

def extract_all_fields(xml_content):
    root = ET.fromstring(xml_content)
    fields = {}
    for property in root.findall('.//property'):
        title = property.find('Title').text if property.find('Title') is not None else None
        if title:
            fields[title] = {child.tag: child.text for child in property}
    return fields

def extract_field_structure(xml_content):
    """Extract all unique field names (tags) from the XML structure"""
    root = ET.fromstring(xml_content)
    field_names = set()
    
    for property in root.findall('.//property'):
        for child in property:
            field_names.add(child.tag)
    
    return sorted(list(field_names))

def compare_field_structure(xml_content1, xml_content2):
    """Compare field structures between two XML files.
    Uses xml_content1 as the reference (correct structure)."""
    fields_reference = set(extract_field_structure(xml_content1))
    fields_to_check = set(extract_field_structure(xml_content2))
    
    # Find what's missing in the second file compared to the reference
    missing_fields = sorted(list(fields_reference - fields_to_check))
    
    return {
        'reference_fields': sorted(list(fields_reference)),
        'missing_in_second_file': missing_fields,
        'total_reference_fields': len(fields_reference),
        'total_missing': len(missing_fields)
    }

def compare_field_structure_reverse(xml_content1, xml_content2):
    """Reverse comparison - check what fields exist in xml_content2 but not in xml_content1.
    Uses xml_content2 as the reference and checks what's extra/missing in xml_content1."""
    fields_reference = set(extract_field_structure(xml_content2))
    fields_to_check = set(extract_field_structure(xml_content1))
    
    # Find what's missing in the first file compared to the second
    missing_fields = sorted(list(fields_reference - fields_to_check))
    
    return {
        'reference_fields': sorted(list(fields_reference)),
        'missing_in_first_file': missing_fields,
        'total_reference_fields': len(fields_reference),
        'total_missing': len(missing_fields)
    }

def compare_fields(fields1, fields2):
    titles1 = set(fields1.keys())
    titles2 = set(fields2.keys())
    
    missing_in_file2 = titles1 - titles2
    missing_in_file1 = titles2 - titles1
    
    common_titles = titles1 & titles2
    return missing_in_file1, missing_in_file2, common_titles