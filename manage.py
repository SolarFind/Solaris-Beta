from flask import *
#from raven.contrib.flask  import Sentry
from config import Configuration
from database import *
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from random import randint

import sys
import flask_admin as fadmin
sys.path.append('/Alpha_1/UI_Flask/pycharm-debug-py3k.egg')

app = Flask(__name__, static_folder=None, template_folder="templates")
app.config.from_object(Configuration)
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#sentry = Sentry(app, dsn='https://082b8cf14f494e2f9ea84e2b7614347f:89d3be577d8c416b9324294869126180@sentry.io/1188746')
app.config['TEMPLATES_AUTO_RELOAD'] = True


from apps.main.views import main
from apps.weather.views import weather
from apps.news.views import news
from apps.admin.views import myadmin
from apps.userman.views import um


app.register_blueprint(main)
app.register_blueprint(um)
app.register_blueprint(weather, url_prefix='/weather')
app.register_blueprint(news, url_prefix='/news')
app.register_blueprint(myadmin, url_prefix='/admin')
#app.register_blueprint(akadoton, url_prefix='/akadoton')
db.create_all()
# Create admin
adminf = fadmin.Admin(app, url="/admin/crud", name='Solarium CRUD', template_mode='bootstrap3')

# Add views
adminf.add_view(UserAdmin(User, db.session))

#dashboard.config.init_from(file='/Alpha_1/UI_Flask/config.cfg')
#dashboard.bind(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def db_logger():
    try:
       print("\n!REQUEST URL: {}\n".format(request.url))
    except Exception as e:
        print("[BUG] ",e)
    #print("CUSER: ", current_user.get_id())
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    req=request.url.split("/", maxsplit=3)[3]
    print(req)
    loc=(request.cookies.get("lat", default=""),  request.cookies.get("long", default=""))
    try:
      uuid=current_user.get_id()
    except Exception as e:
      print(e)  
      uuid=0
    print(uuid)
    if uuid is None:
        uuid=0
    #print("USER ",uuid, ip, loc, browser, "with request", req)
    loog = LoggedUser(int(uuid), ua=ua, ip=ip, loc=str(loc), req=str(req))
    db.session.add(loog)
    db.create_all()
    db.session.commit()



if __name__ == "__main__":
    #reload-test
    app.run(host="0.0.0.0")
