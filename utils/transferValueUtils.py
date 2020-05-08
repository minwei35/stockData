
def get_string(value):
    try:
        if value is None:
            return None
        result = str(value)
        if result == 'nan':
            return None
        else:
            return result
    except ValueError or TypeError:
        return None


def get_float(value):
    try:
        result = get_string(value)
        if result is not None:
            result = float(result)
        return result
    except ValueError or TypeError:
        return None


def get_attr_string(class_name, class_attr):
    try:
        value = getattr(class_name, class_attr)
        return get_string(value)
    except AttributeError:
        return None


def get_attr_float(class_name, class_attr):
    try:
        value = getattr(class_name, class_attr)
        return get_float(value)
    except AttributeError:
        return None
