def to_dict(output, error):
    """
    Returns output and error of command as a dictionary. The values are lists of strings
    :param output:
    :param error:
    :return:
    """
    result = {}

    if error:
        result['error'] = clean(error)
    else:
        result['output'] = clean(output)

    return result


def clean(byte_string):
    """
    Decodes byte_string, converts it into a list of rows and filters out empty rows
    Return filtered list of strings
    :param byte_string:
    :return:
    """
    output = byte_string.decode('utf-8').split('\n')
    return list(filter(None, output))
