'''
Parse stdout from attrib cmd
'''

def parse_attributes(attributes_string):
    ''' Parse the attributes from a string and returns a list '''
    clean_string = attributes_string.strip()
    attributes = [attr.upper() for attr in clean_string if attr != ' ']
    return attributes


def attrib_parser(stdout):
    ''' Parse the attrib stdout and returns a dict [path, attributes] '''
    lines = [line for line in stdout.split('\n') if line != '']
    ATTRIBUTES_FIELD = 13
    parsed_attributes = {}
    for line in lines:
        attributes, path = line[:ATTRIBUTES_FIELD], line[ATTRIBUTES_FIELD:]
        parsed_attributes[path] = parse_attributes(attributes)
    return parsed_attributes
