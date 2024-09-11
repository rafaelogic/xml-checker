import pandas as pd

def normalize_value(value):
    """
    Return an empty string if the value is None
    """
    if value is None:
        return ""

    """
    Normalize values by removing extra whitespace, special characters, and converting HTML entities.
    """
    # Remove leading and trailing whitespace
    value = value.strip()

    # Handle HTML entities and special characters if necessary
    # For example, replace HTML entities with their corresponding characters
    # This can be expanded as needed
    value = value.replace('&#x20AC;', '€').replace('&#xA0;', ' ').replace('&lt;', '<').replace('&gt;', '>')

    return value

def convert_to_numeric(value):
    """
    Convert a string value to a float if possible, otherwise return None.
    """
    try:
        # Attempt to convert to a float
        return float(value)
    except ValueError:
        # Return None if conversion fails
        return None

def compare_field_values(fields1, fields2, common_titles, file1_name, file2_name):
    mismatches = []
    
    for title in common_titles:
        property1 = fields1.get(title, {})
        property2 = fields2.get(title, {})
        
        # Get all unique fields across both properties
        all_fields = set(property1.keys()) | set(property2.keys())
        
        for field in all_fields:
            # Normalize values
            value1 = normalize_value(property1.get(field, 'Not Present'))
            value2 = normalize_value(property2.get(field, 'Not Present'))
            
            ref1 = property1.get('Property_Reference', 'Not Present')
            ref2 = property2.get('Property_Reference', 'Not Present')
            
            # Convert to numeric values for comparison if possible
            numeric_value1 = convert_to_numeric(value1)
            numeric_value2 = convert_to_numeric(value2)
            
            seen_titles = set()
            
            if numeric_value1 is not None and numeric_value2 is not None:
                # Compare numeric values
                if numeric_value1 != numeric_value2:
                    mismatches.append({
                        'Reference #': ref1,
                        'Title': title,
                        'Field': field,
                        f'{file1_name}': value1,
                        f'{file2_name}': value2
                    })
            else:
                # Compare as strings if not numeric
                if value1 != value2:
                    mismatches.append({
                        'Reference #': ref2,
                        'Title': title,
                        'Field': field,
                        f'{file1_name}': value1,
                        f'{file2_name}': value2
                    })
                
    return pd.DataFrame(mismatches)