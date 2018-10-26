from flask import *
from . import utils

weather = Blueprint('weather', __name__, template_folder='templates', static_folder='static')



def capitalize(string, lower_rest=False):
    return string[:1].upper() + (string[1:].lower() if lower_rest else string[1:])


@weather.route('/')
def get_weather():
    lat = request.cookies.get('lat', default=None)
    longi = request.cookies.get('long', default=None)
    m_data = utils.get_all([lat, longi])
    temp = m_data['temp'][0]
    status = m_data['w_dscr']
    status_img = status.replace(' ', '_') + '.jpg'
    return render_template('weather.html', temp=temp, status=capitalize(status), status_img=status_img,
                           ndata=utils.get_forecast([lat, longi]))
