import xml.etree.ElementTree as ET

def extract_all_fields(xml_content):
    root = ET.fromstring(xml_content)
    fields = {}
    for property in root.findall('.//property'):
        title = property.find('Title').text if property.find('Title') is not None else None
        if title:
            fields[title] = {child.tag: child.text for child in property}
    return fields

def compare_fields(fields1, fields2):
    titles1 = set(fields1.keys())
    titles2 = set(fields2.keys())
    
    missing_in_file2 = titles1 - titles2
    missing_in_file1 = titles2 - titles1
    
    common_titles = titles1 & titles2
    return missing_in_file1, missing_in_file2, common_titles