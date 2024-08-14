import os
import json
import xml.etree.ElementTree as ET

def load_required_fields(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        return data.get("required_fields", [])

def check_missing_fields(file_path, required_fields):
    # Load the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Initialize variables to store counts and track missing fields
    total_properties = 0
    missing_fields_counts = {field: 0 for field in required_fields}

    # Loop through each property to check for missing fields
    for property in root.findall('.//property'):
        total_properties += 1
        for field in required_fields:
            # Use the find() method to look for direct children of the property element
            element = property.find(f'./{field}')
            # Check if the field is completely missing (not present)
            if element is None:
                missing_fields_counts[field] += 1

    # Print the results
    print('-----------------------------------------')
    print(f'File: {os.path.basename(file_path)}')
    print(f'Total number of properties: {total_properties}')
    print('Number of properties missing each field:')
    for field, count in missing_fields_counts.items():
        print(f'  {field}: {count} properties')
    print('-----------------------------------------')

def main():
    # Directory containing XML files
    xml_dir = 'xmls'
    json_file_path = 'required_fields.json'
    
    # Load required fields from JSON file
    required_fields = load_required_fields(json_file_path)
    
    # Iterate over each file in the xmls directory
    for file_name in os.listdir(xml_dir):
        if file_name.endswith('.xml'):
            file_path = os.path.join(xml_dir, file_name)
            check_missing_fields(file_path, required_fields)

if __name__ == "__main__":
    main()