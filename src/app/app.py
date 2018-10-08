from flask import Flask, render_template, request, json
#from .. import bankparser
from .bankparser import config

app = Flask(__name__)

@app.route("/")
def main():
    banks = bankparser.config.bankconfig.get_list_banks()

    return render_template('index.html')

@app.route("/parse", methods=['POST'])
def parse():
    if 'file' not in request.files:
        return json.dumps({'html':'<span>No file</span>'})
    
    return json.dumps({'html':'<span>All fields good !!</span>'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)