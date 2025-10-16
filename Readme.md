# JSON-XML Comparer

A powerful tool for comparing JSON field requirements against XML files and comparing XML file structures. Features both a command-line interface and a modern web UI built with Streamlit.

## Features

### 🎯 Three Main Tools:

1. **JSON-XML Comparer** - Compare JSON field requirements against XML files
   - Upload JSON file with required fields
   - Upload multiple XML files to check
   - Visual table showing which fields are missing
   - Filter and select specific columns to display
   - Export results to CSV

2. **XML Field Structure Comparison** - Compare two XML files
   - **Normal Check**: Check what fields are missing in the second XML compared to the first (reference)
   - **Reverse Check**: Check what fields are missing in the first XML compared to the second
   - Visual status indicators (✓ for exists, ✗ for missing)
   - Match rate percentage
   - Export comparison table to CSV

3. **XML Field Value Comparison** - Compare field values between two XML files
   - Identify properties with value mismatches
   - Highlight differences
   - Export to CSV or PDF
   - HTML table view for browser printing

4. **XML Checker** - Explore XML field values
   - Upload XML file
   - Select any field from dropdown
   - View all unique values for that field
   - See value counts and statistics

## Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/rafaelogic/xml-checker.git
cd xml-checker
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create an `xmls` directory for your XML files:
```bash
mkdir xmls
```

4. (Optional) Create a `required_fields.json` file in the project root for command-line usage:
```json
{
    "required_fields": [
        "Title", 
        "Description", 
        "SKU", 
        "Storage"
    ]
}
```

## Usage

### Web UI (Recommended)

Run the Streamlit web application:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

#### Navigation:
- **JSON-XML Comparer** - Compare JSON requirements against XML files
- **Compare XML Files** - Compare two XML file structures or values
- **XML Checker** - Explore field values in XML files

### Command Line

For basic command-line usage:
```bash
python3 xml-checker.py
```

This will check all XML files in the `xmls` directory against the fields defined in `required_fields.json`.

**Example Output:**
```bash
File: properties.xml
Total number of properties: 4170
Number of properties missing each field:
  Title: 0 properties
  Unit_Number: 0 properties
  Type: 0 properties
  Status: 10 properties
  Location: 100 properties
  Latitude: 30 properties
  Yard: 120 properties
  gallery: 27 properties
```

## Features in Detail

### JSON-XML Comparer
- Upload JSON file with required field definitions
- Upload one or multiple XML files
- Interactive table with filtering options
- Show/hide fields with "Show All Fields" toggle
- Multi-select column display
- CSV export functionality

### Compare XML Files

#### Missing Fields Comparison
- **Normal Mode**: Use first XML as reference, check what's missing in second XML
- **Reverse Mode**: Use second XML as reference, check what's missing in first XML
- Visual table with ✓ (exists) and ✗ (missing) indicators
- Summary metrics: Total fields, Missing fields, Match rate percentage
- Clear reference file indicator
- CSV export with detailed comparison

#### Field Values Comparison
- Compare actual values of fields between two XML files
- Identify properties with mismatched values
- Alternating row colors for easy reading
- Export options: CSV, PDF, HTML
- Progress bar for PDF generation
- Browser-printable HTML view

### XML Checker
- Upload any XML file
- Dropdown showing all available field names
- Select "Get Field Value" option
- View all unique values for the selected field
- Display count of occurrences for each value
- Quick field exploration and validation

## Project Structure

```
xml-checker/
├── app.py                  # Main Streamlit application
├── xml-checker.py          # Command-line tool
├── required_fields.json    # JSON field requirements (optional)
├── requirements.txt        # Python dependencies
├── data/                   # Data processing modules
│   ├── field_comparator.py
│   ├── value_comparator.py
│   └── xml_processor.py
├── files/                  # File handling utilities
│   ├── json.py
│   └── xml.py
├── screens/                # UI screens
│   ├── xml_checker.py
│   └── xml_comparer.py
├── ui/                     # UI components
│   ├── display.py
│   └── style.css
└── xmls/                   # XML files directory
```

## Technologies Used

- **Python 3.x** - Core programming language
- **Streamlit** - Web UI framework
- **Pandas** - Data manipulation and analysis
- **ReportLab** - PDF generation
- **XML ElementTree** - XML parsing

## Tips

- 💡 To check for extra fields in XML comparison, use the **Reverse Check** mode
- 📊 Use the CSV export for further analysis in Excel or other tools
- 🔄 Use the "Clear Cache" button if you encounter any display issues
- 📸 The comparison tables are optimized for screenshots and reports

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.

## Future Enhancements

- Batch XML processing with progress tracking
- Custom field validation rules
- XML editing and auto-fill missing fields
- Advanced filtering and search capabilities
- API endpoint for programmatic access
- Support for additional file formats