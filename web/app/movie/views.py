import sqlalchemy
from ..models import Movie, Rating
from flask import flash, redirect, url_for
from . import movie
from .. import db
from flask import render_template
from flask_login import login_required, current_user
import requests
from .usercf import usercf

@movie.route('/tagList')
def tagList():
    with open('app/static/tags.dat') as f:
        taglt = eval(f.read())
        f.close()
    return render_template('movie/tag.html', taglt=taglt)

@movie.route('/topN/<start>')
def topN(start):
    start_url=r'https://api.douban.com/v2/movie/top250?count=10'
    url=start_url+'&start='+start
    r = requests.get(url)
    return render_template('movie/topN.html', movieInfo=r.json(), current_page=(int(start)//10+1))

@movie.route('/search/<keyword>')
@login_required
def search(keyword):
    start_url=r'https://api.douban.com/v2/movie/search?q='
    url=start_url+keyword+'&count=5'
    # print(url)
    r = requests.get(url=url)
    return render_template('movie/searchResult.html', movieInfo=r.json())

@movie.route('/recommed')
@login_required
def recommend():
    user_id = current_user.user_id
    movies_id = usercf.recommend(str(user_id))
    if movies_id is None:
        flash('before recommend you shoud start the recommend algorithm!')
        return redirect(url_for('main.index'))
    start_url = r'https://api.douban.com/v2/movie/search?q='
    movies=[]
    for movie_id in movies_id:
        movie = Movie.query.filter_by(movie_id=movie_id[0]).first()
        print(movie.movie_name)
        url = start_url + movie.movie_name + '&count=1'
        r = requests.get(url=url)
        j = r.json()
        if len(j["subjects"]) == 0:
            continue
            # j["subjects"].append({"title":movie.moviename})
            # j["subjects"].append({"images": {"small":"unknow"}})
            # j["subjects"].append({"year": 0})
            # j["subjects"].append({"genres": movie.movie_genres.split('|')})
            # j["subjects"].append({"directors": [{"name":"unknow"}]})
            # j["subjects"].append({"casts": ['unknow','unknow','unknow']})
            # j["subjects"].append({"reatings": {"average":0}})
        movies.append(j)
    return render_template('movie/recommendResult.html',moviesInfo=movies)

@movie.route('/loadRecSys')
def loadRecSys():
    usercf.generate_dataset()
    usercf.calc_user_sim()
    flash('the algorithm is staring')
    return redirect(url_for('main.index'))
    # return render_template('movie/loadRecSys.html')

@movie.route('/addRatingRecord/<original_name>/<rating>')
def addRatingRecord(original_name,rating):
    user_id = current_user.user_id
    like_str = '%'+original_name+'%'
    movie = Movie.query.filter(Movie.movie_name.ilike(like_str)).first()
    # print(movie.movie_id)
    # return redirect(url_for('main.index'))
    if movie is None:
        flash('add ratingRecord failure!')
        return redirect(url_for('main.index'))
    else:
        rating = Rating(user_id=user_id, movie_id=movie.movie_id, rating=rating)
        try:
            db.session.add(rating)
            db.session.commit()
            flash('add ratingRecord suc!')
            return redirect(url_for('main.index'))
        except sqlalchemy.exc.InvalidRequestError or sqlalchemy.exc.IntegrityError:
            flash('add ratingRecord failure because of the same ratingRecord already in database')
            return redirect(url_for('main.index'))

@movie.route('/delRatingRecord/<movie_id>')
def delRatingRecord(movie_id):
    user_id = current_user.user_id
    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    # rating = Rating(user_id=user_id, movie_id=movie_id)
    db.session.delete(rating)
    db.session.commit()
    flash('delete ratingRecord suc!')
    return redirect(url_for('main.index'))