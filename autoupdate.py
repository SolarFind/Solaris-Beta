from flask import *
from pprint import pprint
from os import environ
app = Flask(__name__)

@app.route("/gh", methods=["POST"])
def gh():
    pprint(request.data)
    return "OK"

if __name__ == "__main__":
    app.run("0.0.0.0", environ["AUP_PORT"])
