from flask import *
#from raven.contrib.flask  import Sentry
from config import Configuration
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from random import randint
#from apps.akadoton.views import akadoton

import sys
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import flask_admin as fadmin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
import flask_monitoringdashboard as dashboard
from password_hashing import create_hash, validate_password
sys.path.append('/Alpha_1/UI_Flask/pycharm-debug-py3k.egg')

app = Flask(__name__, static_folder=None, template_folder="templates")
app.config.from_object(Configuration)
db = SQLAlchemy(app)

# User Class #


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    name = db.Column('name', db.String(50), unique=True , index=True)
    password = db.Column('password' , db.String(256))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
    seed = db.Column('seed', db.Integer)
    role = db.Column('role' , db.String(15))
    addr1 = db.Column('addr1' , db.String(30))
    addr = db.Column('addr' , db.String(150))
    city = db.Column('city' , db.String(30))
 
    def __init__(self , username, password, email, addr="", addr1="", city="", role = "user", name = "User", seed=0):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.registered_on = datetime.utcnow()
        self.name = name
        self.addr = addr
        self.seed = seed
        self.addr1 = addr1
        self.city = city
        db.create_all()
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.id
 
    def __repr__(self):
        return '<User %r>' % (self.username)

# ---------- #

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))

    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    user = db.relationship(User, backref='info')

    def __str__(self):
        return '%s - %s' % (self.key, self.value)

class UserAdmin(sqla.ModelView):
    inline_models = (UserInfo,)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

class LoggedUser(db.Model):
    __tablename__ = "logs"
    uuid = db.Column('uuid', db.BigInteger)
    useragent = db.Column('ua', db.String(140))
    ip = db.Column('ip', db.String(32))
    time_reg = db.Column('registered_on' , db.String(100), primary_key=True)
    loc = db.Column('location', db.String(80))
    req = db.Column('request' , db.String(140))

    def __init__(self , uuid, ua, ip, loc, req):
        print(uuid, ua, ip, loc, req)
        self.uuid = uuid
        self.useragent = ua
        self.ip = ip
        self.loc = loc
        self.req = req
        self.time_reg = datetime.utcnow()
        db.create_all()
    def __repr__(self):
        return '<Request {}:{}>'.format(self.ip, self.req)





login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#sentry = Sentry(app, dsn='https://082b8cf14f494e2f9ea84e2b7614347f:89d3be577d8c416b9324294869126180@sentry.io/1188746')
app.config['TEMPLATES_AUTO_RELOAD'] = True


from apps.main.views import main
from apps.weather.views import weather
from apps.news.views import news
from apps.admin.views import myadmin



app.register_blueprint(main)
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



@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    seed=0
    user = User(request.form['username'],
     create_hash(request.form['password']),
     request.form['email'],
     name=request.form['name']+" "+request.form['surname'], 
     addr=request.form['addr'], 
     addr1 = request.form['addr1'], 
     city=request.form['city'], seed=0)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))
 
@app.route('/login',methods=['GET','POST'])
def login():
    print(request.method)
    if request.method == 'GET':
        if request.args.get("nsi") == '1':
           return render_template('login.html', nsi=True)
        else:
           return render_template('login.html', nsi=False)
    print(request.form)
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username).first()
    try:
      pvl = validate_password(request.form['password'], registered_user.password)
    except AttributeError:
      pvl = False
    if registered_user is None or not pvl:
        print('Username or Password is invalid' , 'error')
        return redirect(url_for('login')+"?nsi=1")
    print(registered_user.role)
    login_user(registered_user)
    print('Logged in successfully')
    if registered_user.role == "admin":
       resp = make_response(redirect(url_for('myadmin.get_adminpanel')))
    else:
       resp = make_response(redirect(url_for('main.search_index')))
    return resp

@app.route('/logout')
def logout():
    logout_user()
    resp = make_response(redirect(url_for('main.search_index')))
    return resp

if __name__ == "__main__":
    #reload-test
    app.run(host="0.0.0.0")
