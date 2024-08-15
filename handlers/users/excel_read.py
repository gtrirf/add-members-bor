import pandas as pd
import re

def process_file(file_path):
    df = pd.read_excel(file_path)
    phone_number_regex = r'\+?[0-9 ]{10,20}'
    phone_numbers = []

    for column in df.columns:
        for value in df[column].dropna():
            if isinstance(value, str):
                matches = re.findall(phone_number_regex, value)
                cleaned_numbers = [re.sub(r'\s+', '', match) for match in matches]
                phone_numbers.extend(cleaned_numbers)

    return phone_numbers
