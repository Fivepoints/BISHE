from ..models import Movie
from flask import flash, redirect, url_for
from . import movie
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
    user_id = current_user.id
    movies_id = usercf.recommend(str(user_id))
    if movies_id is None:
        flash('before recommend you shoud start the recommend algorithm!')
        return redirect(url_for('main.index'))
    start_url = r'https://api.douban.com/v2/movie/search?q='
    movies=[]
    for movie_id in movies_id:
        movie = Movie.query.filter_by(id=movie_id[0]).first()
        url = start_url + movie.moviename + '&count=1'
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
    return render_template('movie/loadRecSys.html')