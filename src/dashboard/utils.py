import json
from collections import defaultdict
import os
cwd = os.getcwd()

def get_code_from_country(value):
    with open(cwd+"/currencies.json", encoding='utf-8') as currencies:
        countries_data = json.load(currencies)
        for country_data in countries_data:
            while country_data['countryName'] == value:
                code = country_data['currencyCode']
                break
        return code
