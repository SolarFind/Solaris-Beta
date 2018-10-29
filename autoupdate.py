from flask import *
import json

from os import environ, system, execv
import sys

app = Flask(__name__)

@app.route("/gh", methods=["POST"])
def gh():
    mydata = json.loads(request.data.decode())
    print(json.dumps(mydata, indent=4))
    if mydata["ref"] == "refs/heads/master":
        system("git pull origin master")
        system("uwsgi --reload /SolarFind/PUI.pid")
    return "OK"

@app.route("/aup_restart")
def aup(): execv(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    app.run("0.0.0.0", environ["AUP_PORT"])
