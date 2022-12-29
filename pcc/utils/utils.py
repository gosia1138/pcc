import re

def get_valid_filename(raw_user_input_str):
    processed_str = str(raw_user_input_str).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', processed_str)
