from typing import Dict, List, Any, Union
from .util import snake_case_to_pascal_case

def revert_samplesheet_to_csv(samplesheet: Dict[str, Any]) -> str:
    """
    Convert a samplesheet dictionary (JSON format) back to CSV string format.
    
    This function takes a dictionary representation of a samplesheet and converts it
    back to the original CSV format with section headers.
    
    Args:
        samplesheet (Dict[str, Any]): The samplesheet data as a dictionary
        
    Returns:
        str: The samplesheet in CSV format with section headers
        
    Example:
        >>> samplesheet = {
        ...     "header": {
        ...         "file_format_version": "2",
        ...         "run_name": "my-run",
        ...         "instrument_platform": "NovaSeq 6000"
        ...     },
        ...     "reads": {
        ...         "read_1_cycles": "151",
        ...         "read_2_cycles": "151"
        ...     }
        ... }
        >>> csv = revert_samplesheet_to_csv(samplesheet)
        >>> print(csv)
        [Header]
        FileFormatVersion,2
        RunName,my-run
        InstrumentPlatform,NovaSeq 6000
        
        [Reads]
        Read1Cycles,151
        Read2Cycles,151
    """
    sections = []
    
    # Define the expected order of sections
    section_order = [
        'header',
        'reads',
        'sequencing',
        'bclconvert_settings',
        'bclconvert_data',
        'cloud_settings',
        'cloud_data',
        'cloud_ts500l_settings',
        'cloud_ts500l_data'
    ]
    
    # Special case mappings for section names
    section_name_mappings = {
        'clouddata': 'Cloud_Data',
        'cloudts500ldata': 'Cloud_TSO500L_Data',
        'cloudts500lsettings': 'Cloud_TSO500L_Settings',
        'cloudsettings': 'Cloud_Settings'
    }
    
    # Special case mappings for field names
    field_name_mappings = {
        'sample_id': 'Sample_ID',
        'index': 'index',
        'index2': 'index2',
        'sample_project': 'Sample_Project',
        'index_id': 'Index_ID',
        'sample_type': 'Sample_Type',
        'library_name': 'LibraryName',
        'library_prep_kit_name': 'LibraryPrepKitName',
        'index_adapter_kit_name': 'IndexAdapterKitName',
        'cloud_workflow': 'Cloud_Workflow',
        'cloud_ts500l_pipeline': 'Cloud_TSO500L_Pipeline',
        'generated_version': 'GeneratedVersion'
    }
    
    # Define field order for specific sections
    field_order = {
        'header': [
            'file_format_version',
            'run_name',
            'run_description',
            'instrument_platform',
            'instrument_type',
            'index_orientation'
        ],
        'reads': [
            'read_1_cycles',
            'read_2_cycles',
            'index_1_cycles',
            'index_2_cycles'
        ],
        'bclconvert_settings': [
            'barcode_mismatches_index1',
            'barcode_mismatches_index2',
            'override_cycles',
            'create_fastq_for_index_reads',
            'no_lane_splitting',
            'fastq_compression_format',
            'adapter_behavior',
            'adapter_read1',
            'adapter_read2',
            'minimum_trimmed_read_length',
            'mask_short_reads',
            'software_version'
        ],
        'cloud_settings': [
            'generated_version',
            'cloud_workflow',
            'cloud_ts500l_pipeline'
        ]
    }
    
    # Process sections in the defined order
    for section_key in section_order:
        # Find the matching key in the samplesheet
        matching_key = None
        for key in samplesheet.keys():
            if key.lower() == section_key:
                matching_key = key
                break
        
        if not matching_key:
            continue
            
        value = samplesheet[matching_key]
        
        # Handle non-array sections (header, reads, settings)
        if not matching_key.endswith('_data') and value and isinstance(value, dict):
            # Get section name with special case handling
            section_name = None
            for key, mapped_name in section_name_mappings.items():
                if section_key == key:
                    section_name = mapped_name
                    break
            
            if section_name is None:
                section_name = snake_case_to_pascal_case(matching_key)
            
            rows = []
            
            # Use predefined field order if available, otherwise sort alphabetically
            if section_key in field_order:
                # Get all fields in the predefined order
                ordered_fields = []
                for field in field_order[section_key]:
                    if field in value:
                        ordered_fields.append(field)
                
                # Add any remaining fields that weren't in the predefined order
                for field in sorted(value.keys()):
                    if field not in ordered_fields:
                        ordered_fields.append(field)
                
                # Process fields in the defined order
                for k in ordered_fields:
                    v = value[k]
                    # Convert snake_case to PascalCase for the key with special case handling
                    field_key = k.lower()
                    if field_key in field_name_mappings:
                        pascal_key = field_name_mappings[field_key]
                    else:
                        pascal_key = snake_case_to_pascal_case(k)
                    
                    if 'Sequencing' in section_name and isinstance(v, list):
                        joint_value = ';'.join(v)
                        rows.append(f"{pascal_key},{joint_value}")
                    else:
                        rows.append(f"{pascal_key},{v}")
            else:
                # Sort keys to ensure consistent order
                sorted_keys = sorted(value.keys())
                
                for k in sorted_keys:
                    v = value[k]
                    # Convert snake_case to PascalCase for the key with special case handling
                    field_key = k.lower()
                    if field_key in field_name_mappings:
                        pascal_key = field_name_mappings[field_key]
                    else:
                        pascal_key = snake_case_to_pascal_case(k)
                    
                    if 'Sequencing' in section_name and isinstance(v, list):
                        joint_value = ';'.join(v)
                        rows.append(f"{pascal_key},{joint_value}")
                    else:
                        rows.append(f"{pascal_key},{v}")
            
            sections.append(f"[{section_name}]\n{chr(10).join(rows)}\n")
        
        # Handle data sections (arrays)
        elif matching_key.endswith('_data') and isinstance(value, list) and value:
            # Get section name with special case handling
            section_name = None
            for key, mapped_name in section_name_mappings.items():
                if section_key == key:
                    section_name = mapped_name
                    break
            
            if section_name is None:
                section_name = snake_case_to_pascal_case(matching_key)
            
            columns = list(value[0].keys())
            
            # Convert column names to PascalCase with special case handling
            header_parts = []
            for col in columns:
                field_key = col.lower()
                if field_key in field_name_mappings:
                    header_parts.append(field_name_mappings[field_key])
                else:
                    header_parts.append(snake_case_to_pascal_case(col))
            
            header = ','.join(header_parts)
            
            # Create rows
            rows = []
            for row in value:
                row_values = [str(row.get(col, '')) for col in columns]
                rows.append(','.join(row_values))
            
            sections.append(f"[{section_name}]\n{header}\n{chr(10).join(rows)}\n")
    
    return '\n'.join(sections)

