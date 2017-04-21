from . import movie
from flask import render_template, request
from flask_login import login_required,current_user
import requests, json
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
    movies = usercf.recommend(str(user_id))
    return render_template('movie/recommendResult.html',movieInfo=movies)

@movie.route('/loadRecSys')
def loadRecSys():

    usercf.generate_dataset()
    usercf.calc_user_sim()
    return render_template('movie/loadRecSys.html')