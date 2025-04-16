import re

# https://regex101.com/r/AneCvL/1
# Matches any number of headers, separated by commas
# Matches [Header], [Header, Header2], [Test_Section_1]
HEADER_REGEX_MATCH = re.compile(
    r"\[([a-zA-Z0-9_]+)](?:,*)?"
)

def pascal_case_to_snake_case(s: str) -> str:
    """
    Convert string from PascalCase to snake_case with special cases handling.
    
    Examples:
        TrimUMI -> trim_umi
        Sample_ID -> sample_id
        Cloud_Workflow -> cloud_workflow
        Index_ID -> index_id
        I7_Index_ID -> i7_index_id
        I5_Index_ID -> i5_index_id
        Sample_Type -> sample_type
        Sample_Description -> sample_description
        BCLConvert_Settings -> bclconvert_settings
        BCLConvert_Data -> bclconvert_data
        TSO500L_Settings -> tso500l_settings
        TSO500_Settings -> tso500_settings
        Read1Cycles -> read_1_cycles
    """
    # Special case replacements
    replacements = {
        'UMI': 'Umi',
        'ID': 'Id',
        'BCLConvert': 'Bclconvert',
        'TSO500L': 'Tso500l',
        'TSO500': 'Tso500'
    }
    
    # Apply initial replacements
    result = s
    for old, new in replacements.items():
        result = result.replace(old, new)
    
    # Remove underscores and convert to snake_case
    result = ''.join(result.split('_'))
    result = ''.join(['_' + c.lower() if c.isupper() else c.lower() for c in result]).lstrip('_')
    
    # Handle numeric cases (processed after converting to snake case)
    number_replacements = [
        ('read1_', 'read_1_'),
        ('read2_', 'read_2_'),
        ('index1_', 'index_1_'),
        ('index2_', 'index_2_'),
        ('_index1', '_index_1'),
        ('_index2', '_index_2'),
        ('_read1', '_read_1'),
        ('_read2', '_read_2')
    ]
    
    for old, new in number_replacements:
        result = result.replace(old, new)
        
    return result

def snake_case_to_pascal_case(s: str) -> str:
    """
    Convert string from snake_case to PascalCase with special cases handling.
    
    Examples:
        trim_umi -> TrimUMI
        sample_id -> Sample_ID
        cloud_workflow -> Cloud_Workflow
        index_id -> Index_ID
        i7_index_id -> I7_Index_ID
        i5_index_id -> I5_Index_ID
        sample_type -> Sample_Type
        sample_description -> Sample_Description
        bclconvert_settings -> BCLConvert_Settings
        bclconvert_data -> BCLConvert_Data
        tso500l_settings -> TSO500L_Settings
        tso500_settings -> TSO500_Settings
        read_1_cycles -> Read1Cycles
        cloud_settings -> Cloud_Settings
        cloud_data -> Cloud_Data
        cloud_ts500l_settings -> Cloud_TS500L_Settings
        cloud_ts500l_data -> Cloud_TS500L_Data
        cloud_ts500_settings -> Cloud_TS500_Settings
        cloud_tso500l_pipeline -> Cloud_TSO500L_Pipeline
    """
    # Special case replacements
    replacements = {
        'bclconvert': 'BCLConvert',
        'tso500l': 'TSO500L',
        'tso500': 'TSO500',
        'i7': 'I7',
        'i5': 'I5'
    }
    
    # Handle special cases with underscores
    underscore_cases = [
        'sample_id', 'cloud_workflow', 'index_id', 'i7_index_id', 
        'i5_index_id', 'sample_type', 'sample_description',
        'bclconvert_settings', 'bclconvert_data', 'tso500l_settings', 'tso500_settings',
        'cloud_settings', 'cloud_data', 'cloud_ts500l_settings', 'cloud_ts500l_data', 'cloud_ts500_settings',
        'cloud_tso500l_pipeline'
    ]
    
    if s in underscore_cases:
        parts = s.split('_')
        result = []
        for part in parts:
            if part in replacements:
                result.append(replacements[part])
            else:
                result.append(part.capitalize())
        return '_'.join(result)
    
    # Handle read cycles special case
    if s == 'read_1_cycles':
        return 'Read1Cycles'
    if s == 'read_2_cycles':
        return 'Read2Cycles'
    if s == 'index_1_cycles':
        return 'Index1Cycles'
    if s == 'index_2_cycles':
        return 'Index2Cycles'
    
    # Handle trim_umi special case
    if s == 'trim_umi':
        return 'TrimUMI'
    
    # Default conversion for other cases
    parts = s.split('_')
    result = []
    for part in parts:
        if part in replacements:
            result.append(replacements[part])
        else:
            result.append(part.capitalize())
    return ''.join(result)

