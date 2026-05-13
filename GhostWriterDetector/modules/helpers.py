def safe_get(data, *keys, default=None):
    """Safely access nested dictionary"""
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
            if current is None:
                return default
        else:
            return default
    return current


def dict_merge(dict1, dict2):
    """Merge two dictionaries"""
    result = dict1.copy()
    result.update(dict2)
    return result


def error_response(message, code=400):
    """Create error response"""
    return {'error': message, 'status': code}


def success_response(data, message='Success', code=200):
    """Create success response"""
    return {'data': data, 'message': message, 'status': code}
