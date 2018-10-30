from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin.contrib import sqla
from flask_login import current_user
# User Class #

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    name = db.Column('name', db.String(50), unique=True, index=True)
    password = db.Column('password', db.String(256))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    seed = db.Column('seed', db.Integer)
    role = db.Column('role', db.String(15))
    addr1 = db.Column('addr1', db.String(30))
    addr = db.Column('addr', db.String(150))
    city = db.Column('city', db.String(30))

    def __init__(self, username, password, email, addr="", addr1="", city="", role="user", name="User", seed=0):
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
    time_reg = db.Column('registered_on', db.String(100), primary_key=True)
    loc = db.Column('location', db.String(80))
    req = db.Column('request', db.String(140))

    def __init__(self, uuid, ua, ip, loc, req):
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