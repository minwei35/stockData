
def is_not_blank(value):
    try:
        if value is None:
            return False
        if value.strip() == '':
            return False
        else:
            return True
    except ValueError or TypeError:
        return False


def is_blank(value):
    try:
        if value is None:
            return True
        if value.strip() == '':
            return True
        else:
            return False
    except ValueError or TypeError:
        return True
