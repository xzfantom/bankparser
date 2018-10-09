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
    print (request.get_json())
    return json.dumps(request.json)
    #if 'inputFile' not in request.files:
    #    return json.dumps({'html':'<span>No file</span>'})
    
    #return json.dumps({'html':'<span>All fields good !!</span>'})