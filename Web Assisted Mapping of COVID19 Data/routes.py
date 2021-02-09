from app import app 
from flask import render_template ,redirect, url_for, flash, get_flashed_messages, request,session
from functools import wraps
from app import login_required
from flask_wtf import FlaskForm



@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html',error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You have succesfully logged out')
    return redirect(url_for('login'))

@app.route('/default_map')
@login_required
def default_map():
    return render_template('default_map.html')

@app.route('/geodata_map')
@login_required
def geodata_map():
    return render_template('geodata_map.html')

@app.route('/marker_map')
@login_required
def marker_map():
    return render_template('marker_map.html')

@app.route('/heat_map')
@login_required
def heat_map():
    return render_template('heat_map.html')