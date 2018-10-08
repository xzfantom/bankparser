import bankparser
import bankparser.config

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route("/")
def main():
    banks = bankparser.config.bankconfig.get_list_banks()
    
    for bank in banks:
        print(bank)

    return render_template('index.html', banks=banks)

@bp.route("/parse", methods=['POST'])
def parse():
    if 'file' not in request.files:
        return json.dumps({'html':'<span>No file</span>'})
    
    return json.dumps({'html':'<span>All fields good !!</span>'})