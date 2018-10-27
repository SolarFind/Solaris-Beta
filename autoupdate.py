from flask import *
import json

from os import environ
app = Flask(__name__)

@app.route("/gh", methods=["POST"])
def gh():
    mydata = json.loads(request.data.decode())
    print(json.dumps(mydata, indent=4))
    return "OK"

if __name__ == "__main__":
    app.run("0.0.0.0", environ["AUP_PORT"])