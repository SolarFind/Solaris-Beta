
from flask import *

# from flask.ext.babel import Babel, gettext
import requests
from config import *

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

def write_data(pth, r):
    with open('click_stat.dat', 'a') as f:
        f.write("{0}\t{1}\n".format(r, pth))


page_rank = {}

#@main.route('/')
#def index():
#    print(request.headers)
#    return render_template('alpha_gate.html')

@main.route("/sw.js")
def sw():
    return redirect("/static/js/serviceworker.js")
@main.route('/')
def search_index():
    loc = str(request.accept_languages).split(",")[0]
    try:
        exmp = requests.get(BACK_URL + "/example").text
    except requests.exceptions.ConnectionError:
        exmp = "Backend server does not working"
    return render_template('index.html', loc=loc, exmp=exmp)

@main.route("/aucomp")
def auto_proxy():
    return jsonify(requests.get("http://solarfind.net:8121/aucomp").json())

@main.route('/redirect')
def redir():

    pth = request.args.get('url')
    r = request.args.get('r')
    write_data(pth, r)
    return redirect(pth)


@main.route('/search')
def get_search():
    try:
        sw = request.args.get('s')
        if sw[-1:]==" ":
            print("+")
            sw=sw[:-1]
        res = requests.get(BACK_URL + "/search?s={0}&p={1}".format(sw,
                                                                              request.args.get('p', default=1,
                                                                                               type=int)))
        res = res.json()
        #print(res)
        exmp = requests.get(BACK_URL + "/example").text
    except requests.exceptions.ConnectionError:
        res = {'time': 0.0, 'total': 0, 'data': [["Conn error", "", "Sorry! We have connection error!"]]}
        exmp = ''
    p = request.args.get('p', default=1, type=int)
    print("RAW", request.args.get('r', default=0, type=int))
    if int(request.args.get('raw', default=0, type=int)) == 0:
      return render_template(
        'search_jinja.html',
        exmp=exmp,
        active_page=p,
        results=res['data'],
        pages=int(res['total'] / 20) + 1 if res['total'] % 20 else res['total'] // 20,
        r_name=request.args.get('s'),
        total=res['total'],
        time=res['time']
       )
    else:
        return render_template(
            'raw_search.html',
            exmp=exmp,
            active_page=p,
            results=res['data'],
            pages=int(res['total'] / 20) + 1 if res['total'] % 20 else res['total'] // 20,
            r_name=request.args.get('s'),
            total=res['total'],
            time=res['time']
        )


@main.errorhandler(404)
def nfound_error(w):
    print(w)
    return render_template('404.html'), 404
