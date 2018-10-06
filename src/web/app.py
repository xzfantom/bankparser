from flask import Flask, render_template, request, json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/parse", methods=['POST'])
def parse():
    return json.dumps({'html':'<span>All fields good !!</span>'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)