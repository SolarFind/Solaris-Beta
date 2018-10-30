from flask import *
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from password_hashing import create_hash, validate_password
from database import *

um = Blueprint('userman', __name__, template_folder='templates', static_folder='static')

def capitalize(string, lower_rest=False):
    return string[:1].upper() + (string[1:].lower() if lower_rest else string[1:])


@um.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    seed = 0
    user = User(request.form['username'],
                create_hash(request.form['password']),
                request.form['email'],
                name=request.form['name'] + " " + request.form['surname'],
                addr=request.form['addr'],
                addr1=request.form['addr1'],
                city=request.form['city'], seed=0)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@um.route('/login', methods=['GET', 'POST'])
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
        print('Username or Password is invalid', 'error')
        return redirect(url_for('login') + "?nsi=1")
    print(registered_user.role)
    login_user(registered_user)
    print('Logged in successfully')
    if registered_user.role == "admin":
        resp = make_response(redirect(url_for('myadmin.get_adminpanel')))
    else:
        resp = make_response(redirect(url_for('main.search_index')))
    return resp


@um.route('/logout')
def logout():
    logout_user()
    resp = make_response(redirect(url_for('main.search_index')))
    return resp