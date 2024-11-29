from typing import Dict, Optional

def safe_get_nested(data: Dict, *keys: str, default=None) -> Optional[Dict]:
    """Safely navigate nested dictionary structure."""
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
        if current is None:
            return default
    return current

def validate_response(data: Dict) -> bool:
    """Validate the API response structure."""
    if not data or not isinstance(data, dict):
        return False
    
    status = safe_get_nested(data, 'status', 'rCode')
    if status != 200:
        return False
    
    data_section = safe_get_nested(data, 'data')
    if not data_section:
        return False
    
    return True