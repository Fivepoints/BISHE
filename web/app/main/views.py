from flask import render_template
from flask_login import current_user
from . import main
from ..models import Movie, Rating, User

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/schedule')
def schedule():
    return render_template('schedule.html')

@main.route('/setting')
def setting():
    user_id = current_user.user_id
    sendEmailbol=User.query.filter_by(user_id=user_id).first().sendEmail
    print(sendEmailbol)
    settingilt = {}
    settingilt['sendEmailbol'] = sendEmailbol
    settingilt['subjects'] = []
    ratings = Rating.query.filter_by(user_id=user_id).all()
    for rating in ratings:
        movie_name=Movie.query.filter_by(movie_id=rating.movie_id).first().movie_name
        subject= {'movie_id':rating.movie_id, 'movie_name': movie_name, 'rating_score': rating.rating}
        settingilt['subjects'].append(subject)
    return render_template('setting.html',settingilt=settingilt)