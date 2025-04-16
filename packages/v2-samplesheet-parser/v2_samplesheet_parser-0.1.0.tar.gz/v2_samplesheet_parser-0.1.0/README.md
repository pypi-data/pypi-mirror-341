# v2-samplesheet-parser

A lightweight Python tool to parse and validate Illumina Sample Sheet v2 format. This tool supports multiple formats including BCLConvert, Cloud, TSO500L, and TSO500S sections.

## Features

- **Parse CSV to JSON**: Convert Illumina Sample Sheet v2 CSV format to structured JSON data
- **Validate Samplesheets**: Ensure samplesheets meet the required format and contain necessary sections
- **Retrieve Library Information**: Extract library information from samplesheets
- **Revert JSON to CSV**: Convert structured JSON data back to Illumina Sample Sheet v2 CSV format
- **Support for multiple section types**:
  - Run Info Sections (Header, Reads, Sequencing)
  - BCLConvert Sections
  - Cloud Sections
  - TSO500L Sections
  - TSO500S Sections
- **Data validation** using Pydantic models
- **Consistent naming conventions** with automatic conversion between PascalCase and snake_case
- **Comprehensive error handling** with detailed error messages

## Installation

```bash
pip install v2-samplesheet-parser
```

## Usage

### Basic Usage

```python
from v2_samplesheet_parser import parse_samplesheet

# Your samplesheet content as a string
samplesheet_content = """
[Header]
FileFormatVersion,2
RunName,my-illumina-sequencing-run
InstrumentPlatform,NovaSeq 6000

[Reads]
Read1Cycles,151
Read2Cycles,151
"""

# Parse the samplesheet
result = parse_samplesheet(samplesheet_content)
print(result)
```

### Supported Section Types

The parser supports various section types:

1. **Run Info Sections**

   - [Header]
   - [Reads]
   - [Sequencing]

2. **BCLConvert Sections**

   - [BCLConvert_Settings]
   - [BCLConvert_Data]

3. **Cloud Sections**

   - [Cloud_Settings]
   - [Cloud_Data]

4. **TSO500L Sections**

   - [TSO500L_Settings]
   - [TSO500L_Data]
   - [Cloud_TSO500L_settings]
   - [Cloud_TSO500L_Data]

5. **TSO500S Sections**
   - [TSO500S_Settings]
   - [TSO500S_Data]
   - [Cloud_TSO500S_Settings]
   - [Cloud_TSO500S_Data]

## Development

### Setup Development Environment

1. Clone the repository:

```bash
git clone https://github.com/umccr/v2-samplesheet-parser.git
cd v2-samplesheet-parser
```

2. Install development dependencies:

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

## Raising Issues

If you encounter any issues or have suggestions for improvements:

1. Check if the issue already exists in the [Issue Tracker](https://github.com/umccr/v2-samplesheet-parser/issues)
2. If not, create a new issue with:
   - A clear description of the problem
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Sample data (if applicable)
   - Python version and environment details

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Ray Liu (ray.liu@unimelb.edu.au)

## Acknowledgments

- Based on the Illumina Sample Sheet v2 format specification
- Built with Pydantic for robust data validation
