from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/schedule')
def schedule():
    return render_template('schedule.html')