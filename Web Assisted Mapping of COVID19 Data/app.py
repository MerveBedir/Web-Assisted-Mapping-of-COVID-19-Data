from flask import Flask,render_template ,redirect, url_for, flash, get_flashed_messages, request,session
from functools import wraps
import covid

app = Flask(__name__)
app.config['SECRET_KEY'] = "totallysecretkey"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
    


