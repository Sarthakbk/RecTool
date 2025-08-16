from typing import Dict, List, Any, Tuple

def validate_jd_data(data: Dict[str, Any], is_update: bool = False) -> Dict[str, Any]:
    """
    Validate job description data
    
    Args:
        data: Dictionary containing job description data
        is_update: Boolean indicating if this is an update operation
    
    Returns:
        Dictionary with validation result
    """
    errors = []
    
    # Required fields for creation
    required_fields = ['jd_title', 'primary_skill', 'mode', 'tenure_months', 'open_positions']
    
    if not is_update:
        for field in required_fields:
            if not data.get(field):
                errors.append(f'{field} is required')
    
    # Validate field types and values
    validation_results = [
        _validate_string_field(data, 'jd_title', 150, required=not is_update),
        _validate_string_field(data, 'primary_skill', 100, required=not is_update),
        _validate_string_field(data, 'secondary_skills', max_length=None),
        _validate_enum_field(data, 'mode', ['Onsite', 'Remote', 'Hybrid'], required=not is_update),
        _validate_integer_field(data, 'tenure_months', min_value=1, required=not is_update),
        _validate_integer_field(data, 'open_positions', min_value=1, required=not is_update),
        _validate_integer_field(data, 'available_positions', min_value=0),
        _validate_decimal_field(data, 'experience_min', 4, 1, min_value=0),
        _validate_decimal_field(data, 'experience_max', 4, 1, min_value=0),
        _validate_decimal_field(data, 'budget_min', 10, 2, min_value=0),
        _validate_decimal_field(data, 'budget_max', 10, 2, min_value=0),
        _validate_text_field(data, 'jd_keywords'),
        _validate_text_field(data, 'original_jd'),
        _validate_text_field(data, 'special_instruction')
    ]
    
    # Collect all validation errors
    for result in validation_results:
        if result and not result['valid']:
            errors.extend(result['errors'])
    
    # Validate logical relationships
    logical_errors = _validate_logical_relationships(data)
    errors.extend(logical_errors)
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def _validate_string_field(data: Dict[str, Any], field_name: str, max_length: int, required: bool = False) -> Dict[str, Any]:
    """Validate string field"""
    if field_name not in data:
        if required:
            return {'valid': False, 'errors': [f'{field_name} is required']}
        return {'valid': True, 'errors': []}
    
    value = data[field_name]
    if value is None:
        if required:
            return {'valid': False, 'errors': [f'{field_name} cannot be null']}
        return {'valid': True, 'errors': []}
    
    if not isinstance(value, str):
        return {'valid': False, 'errors': [f'{field_name} must be a string']}
    
    if max_length and len(value) > max_length:
        return {'valid': False, 'errors': [f'{field_name} must be {max_length} characters or less']}
    
    return {'valid': True, 'errors': []}

def _validate_enum_field(data: Dict[str, Any], field_name: str, valid_values: List[str], required: bool = False) -> Dict[str, Any]:
    """Validate enum field"""
    if field_name not in data:
        if required:
            return {'valid': False, 'errors': [f'{field_name} is required']}
        return {'valid': True, 'errors': []}
    
    value = data[field_name]
    if value is None:
        if required:
            return {'valid': False, 'errors': [f'{field_name} cannot be null']}
        return {'valid': True, 'errors': []}
    
    if value not in valid_values:
        return {'valid': False, 'errors': [f'{field_name} must be one of: {", ".join(valid_values)}']}
    
    return {'valid': True, 'errors': []}

def _validate_integer_field(data: Dict[str, Any], field_name: str, min_value: int = None, required: bool = False) -> Dict[str, Any]:
    """Validate integer field"""
    if field_name not in data:
        if required:
            return {'valid': False, 'errors': [f'{field_name} is required']}
        return {'valid': True, 'errors': []}
    
    value = data[field_name]
    if value is None:
        if required:
            return {'valid': False, 'errors': [f'{field_name} cannot be null']}
        return {'valid': True, 'errors': []}
    
    try:
        int_value = int(value)
        if min_value is not None and int_value < min_value:
            return {'valid': False, 'errors': [f'{field_name} must be {min_value} or greater']}
        return {'valid': True, 'errors': []}
    except (ValueError, TypeError):
        return {'valid': False, 'errors': [f'{field_name} must be a valid integer']}

def _validate_decimal_field(data: Dict[str, Any], field_name: str, precision: int, scale: int, min_value: float = None) -> Dict[str, Any]:
    """Validate decimal field"""
    if field_name not in data:
        return {'valid': True, 'errors': []}
    
    value = data[field_name]
    if value is None:
        return {'valid': True, 'errors': []}
    
    try:
        float_value = float(value)
        if min_value is not None and float_value < min_value:
            return {'valid': False, 'errors': [f'{field_name} must be {min_value} or greater']}
        
        # Check precision and scale
        str_value = str(float_value)
        if '.' in str_value:
            integer_part, decimal_part = str_value.split('.')
            if len(integer_part) > (precision - scale):
                return {'valid': False, 'errors': [f'{field_name} integer part exceeds maximum length']}
            if len(decimal_part) > scale:
                return {'valid': False, 'errors': [f'{field_name} decimal part exceeds maximum precision']}
        
        return {'valid': True, 'errors': []}
    except (ValueError, TypeError):
        return {'valid': False, 'errors': [f'{field_name} must be a valid number']}

def _validate_text_field(data: Dict[str, Any], field_name: str) -> Dict[str, Any]:
    """Validate text field"""
    if field_name not in data:
        return {'valid': True, 'errors': []}
    
    value = data[field_name]
    if value is None:
        return {'valid': True, 'errors': []}
    
    if not isinstance(value, str):
        return {'valid': False, 'errors': [f'{field_name} must be a string']}
    
    return {'valid': True, 'errors': []}

def _validate_logical_relationships(data: Dict[str, Any]) -> List[str]:
    """Validate logical relationships between fields"""
    errors = []
    
    # Validate experience range
    exp_min = data.get('experience_min')
    exp_max = data.get('experience_max')
    if exp_min is not None and exp_max is not None:
        try:
            if float(exp_min) > float(exp_max):
                errors.append('experience_min cannot be greater than experience_max')
        except (ValueError, TypeError):
            pass
    
    # Validate budget range
    budget_min = data.get('budget_min')
    budget_max = data.get('budget_max')
    if budget_min is not None and budget_max is not None:
        try:
            if float(budget_min) > float(budget_max):
                errors.append('budget_min cannot be greater than budget_max')
        except (ValueError, TypeError):
            pass
    
    # Validate available positions vs open positions
    open_pos = data.get('open_positions')
    available_pos = data.get('available_positions')
    if open_pos is not None and available_pos is not None:
        try:
            if int(available_pos) > int(open_pos):
                errors.append('available_positions cannot exceed open_positions')
        except (ValueError, TypeError):
            pass
    
    return errors

def sanitize_jd_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize job description data by removing extra whitespace and normalizing values
    
    Args:
        data: Raw job description data
    
    Returns:
        Sanitized data dictionary
    """
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Remove leading/trailing whitespace
            sanitized[key] = value.strip()
        elif isinstance(value, (int, float)):
            # Ensure numeric values are properly typed
            sanitized[key] = value
        else:
            # Keep other types as-is
            sanitized[key] = value
    
    return sanitized 