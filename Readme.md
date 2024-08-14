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

## Roadmap
- Develop a UI that will highlight the items where the fields are missing.
- Automatically fill the item with the missing field.