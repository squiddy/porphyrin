"""
See https://en.wikipedia.org/wiki/Anatomical_Therapeutic_Chemical_Classification_System
"""

import csv
import json
from typing import Union, TextIO


class AtcGroup:
    """
    Represents part of an ATC code.
    """
    def __init__(self, code, name, catalog):
        self.catalog = catalog
        self.code = code
        self.name = name


class AtcCode:
    """
    Represents ATC code and allows access to all groups/levels by properties.
    """
    def __init__(self, code, name, catalog):
        if len(code) != 7:
            raise Exception('Invalid code, expected 6 characters')

        self.code = code
        self.name = name
        self.catalog = catalog
    
    @property
    def first_level(self):
        return self.code[0]

    @property
    def first_group(self):
        return self.catalog.lookup(self.code[0])

    @property
    def second_level(self):
        return self.code[1:3]

    @property
    def second_group(self):
        return self.catalog.lookup(self.code[:3])

    @property
    def third_level(self):
        return self.code[3]

    @property
    def third_group(self):
        return self.catalog.lookup(self.code[:4])

    @property
    def fourth_level(self):
        return self.code[4]

    @property
    def fourth_group(self):
        return self.catalog.lookup(self.code[:5])

    @property
    def fifth_level(self):
        return self.code[5:]


class Catalog:
    def __init__(self):
        self.entries = {}

    def load(self, file: TextIO):
        self.entries = json.load(file)

    def lookup(self, code: str) -> Union[None, AtcCode, AtcGroup]:
        match = self.entries.get(code)
        if not match:
            return None

        if len(code) != 7:
            return AtcGroup(code, match, self)
        else:
            return AtcCode(code, match, self)


def convert_data(source_file: TextIO, target_file: TextIO):
    """
    Expects a CSV file in `source_file` and writes the atc codes as JSON into
    `target_file`.
    """
    entries = {}

    reader = csv.reader(source_file)
    for row in reader:
        if all(not col for col in row):
            # skip empty lines
            continue

        if len(row) != 5:
            raise Exception('Failed to convert ATC data')

        atc_code = row[0].strip()
        name = row[2].strip().replace('\n', '')
        entries[atc_code] = name

    json.dump(entries, target_file)
