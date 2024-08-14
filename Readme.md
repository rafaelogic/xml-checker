# XML Field Checker

A simple script that checks if certain fields are missing in a list of XML files. To use it, follow these steps:

## Setup
1. Install Python3 if you don't have it already.

2. Clone this repository.

3. Create an `xmls` directory and Put your XML files inside.

4. Create a new file called `required_fields.json` in the project root if not present. This file should contain a list of the fields that you want to check if they are missing in each XML file. For example:
```json
{
    "required_fields": [
        'Title', 
        'Description', 
        'SKU', 'Storage'
    ]
}
```

## Usage
1. cd to the project's root directory

2. Run `python3 xml-checker.py`
**Example Output** 
```bash
File: properties.xml
Total number of properties: 4170
Number of properties missing each field:
  Title: 0 properties
  Unit_Number: 0 properties
  Type: 0 properties
  Bedrooms: 0 properties
  Bathrooms: 0 properties
  Project: 0 properties
  Price: 0 properties
  VAT: 0 properties
  Status: 10 properties
  Area: 0 properties
  Location: 100 properties
  Latitude: 30 properties
  Longitude: 0 properties
  Apartment_Floor: 0 properties
  Block: 0 properties
  Phase: 0 properties
  Construction_Stage: 0 properties
  Plot_Size: 0 properties
  Yard: 120 properties
  Description: 0 properties
  gallery: 27 properties
  ```

## Roadmap
- Develop a UI that will highlight the items where the fields are missing.
- Automatically fill the item with the missing field.