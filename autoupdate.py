from flask import *
from os import environ
app = Flask(__name__)

@app.route("/gh", methods=["POST"])
def gh():
    print(request.data)

if __name__ == "__main__":
    app.run("0.0.0.0", environ["AUP_PORT"])
