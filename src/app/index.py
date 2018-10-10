import bankparser
import bankparser.config
import bankparser.qif
import os
import datetime

from flask import (
    Blueprint, render_template, request, json, url_for, send_file
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
    
    newname = bankname + now + ".qif"
    newname = os.path.join(app.config['UPLOAD_FOLDER'], newname)

    filename = bankname + now + ".in"
    filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filename)
    
    bank_parser = bankparser.config.bankconfig.get_parser(bankname)

    statement = bank_parser.parse(filename)
    qif = bankparser.qif.QIF(statement)
    qif.write(newname)

    return send_file(newname, as_attachment=True)