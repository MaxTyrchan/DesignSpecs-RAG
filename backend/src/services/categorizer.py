def categorize(elements):
    """
    Categorizes the elements into unique types and counts the number of each type
    :param elements: list of elements
    :return: unique_types: set of unique types
    """
    if isinstance(elements, list):
        element_dict = [el.to_dict() for el in elements]
            
        unique_types = set()
            
        for item in element_dict:
            unique_types.add(item['type'])
            
        return unique_types
    else:
        raise ValueError("elements must be a dictionary")
    