import bankparser
import bankparser.config

from flask import (
    Blueprint, render_template, request, json
)

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route("/")
def main():
    banks = bankparser.config.bankconfig.get_list_banks()
    return render_template('index.html', banks=banks)

@bp.route("/parse", methods=['POST'])
def parse():
    if 'inputFile' not in request.files:
        return json.dumps({'html':'<span>No file</span>'})
    
    return json.dumps({'html':'<span>All fields good !!</span>'})