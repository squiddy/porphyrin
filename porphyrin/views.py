import naposapi
from flask import render_template, request

from porphyrin import app


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/classification/lookup/')
def classification_lookup():
    atc_code = request.args.get('atc_code')
    result = naposapi.lookup_classification(atc_code)
    return render_template('classification.html', atc_code=atc_code, result=result)