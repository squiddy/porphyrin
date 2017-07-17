import os

import click
from flask import Flask

app = Flask(__name__)

from porphyrin.atc_catalog import convert_data, Catalog

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data/atc.json')

catalog = Catalog()
with open(DATA_FILE) as f:
    catalog.load(f)

import porphyrin.views

@app.cli.command()
@click.argument('filename')
def convert_atc_data(filename):
    with open(DATA_FILE, 'w') as target:
        with open(filename) as source:
            convert_data(source, target)

    click.echo('Converting ATC data to internal format done')