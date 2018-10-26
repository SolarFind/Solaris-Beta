from flask import *
from flask_login import login_user , logout_user , current_user , login_required


myadmin = Blueprint('myadmin', __name__, template_folder='templates', static_folder='static')

def capitalize(string, lower_rest=False):
    return string[:1].upper() + (string[1:].lower() if lower_rest else string[1:])


@myadmin.route('/logout')
def _adminlogout():
    return redirect("/logout")

@myadmin.route('/')
@login_required
def get_adminpanel():
    return render_template('admin.html')
