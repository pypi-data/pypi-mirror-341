
from v2_samplesheet_parser.functions.parser import parse_samplesheet

def retrieve_library_from_csv_samplesheet(samplesheet: str) -> list:
    """
    Retrieve the library information from a CSV samplesheet
    """
    bclconvert_data = parse_samplesheet(samplesheet).get("bclconvert_data", [])
    # remove repeated value
    return list(dict.fromkeys(entry["sample_id"] for entry in bclconvert_data))

