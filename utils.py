from itertools import product

def split_and_combine(input_dict):
    """Splits the values of the input_dict by commas and returns all possible combinations."""
    
    # If a value is None or not a string, it's returned as is, otherwise it's split by comma
    split_values = {
        key: [v.strip() for v in value.split(',')] if isinstance(value, str) else value 
        for key, value in input_dict.items() if value is not None
    }

    # Extract keys with None values
    none_keys = [key for key, value in input_dict.items() if value is None]

    # Compute the Cartesian product for the split values
    combined_dicts = []
    for combination in product(*split_values.values()):
        combined_dict = dict(zip(split_values.keys(), combination))
        
        # Add keys with None values to the combined dictionary
        for none_key in none_keys:
            combined_dict[none_key] = None

        combined_dicts.append(combined_dict)

    return combined_dicts

