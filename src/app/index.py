import bankparser
import bankparser.config
import bankparser.qif
import os
import datetime

from flask import (
    Blueprint, render_template, request, json, url_for, send_file, redirect, jsonify
)

from flask import current_app as app

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route("/")
def main():
    banks = bankparser.config.bankconfig.get_list_banks()
    return render_template('index.html', banks=banks)

@bp.route("/parse/", methods=['POST'])
def parse():
    if 'inputFile' not in request.files:
        return redirect(url_for('/'))

    format = "%Y%m%dT%H%M%S"
    now = datetime.datetime.utcnow().strftime(format)

    file = request.files['inputFile']
    bankname = request.form['inputBank']
    prefix = bankname + now
    
    newname = os.path.join(app.config['UPLOAD_FOLDER'], prefix + ".qif")

    filename = os.path.join(app.config['UPLOAD_FOLDER'], prefix + ".in")

    file.save(filename)
    
    bank_parser = bankparser.config.bankconfig.get_parser(bankname)

    statement = bank_parser.parse(filename)
    qif = bankparser.qif.QIF(statement)
    qif.write(newname)

    return send_file(newname, as_attachment=True)

@bp.route("/oauth2", methods=['GET'])
def oauth():
    dict = {}
    for params in request.args:
        dict[params] = request.args.get(params)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], "data.json")

    with open(filepath, 'w') as outfile:
        json.dump(dict, outfile)

    return jsonify("result:ok")

@bp.route("/result", methods=['GET'])
def result():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], "data.json")
    with open(filepath, 'r') as infile:
        dict = json.load(infile)
    return jsonify(dict)
