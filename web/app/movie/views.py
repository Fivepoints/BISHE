from . import movie
from flask import render_template, request
import requests, json

@movie.route('/tagList')
def tagList():
    with open('app/static/tags.dat') as f:
        taglt = eval(f.read())
        f.close()
    return render_template('movie/tag.html', taglt=taglt)

@movie.route('/search/<keyword>')
def search(keyword):
    start_url=r'https://api.douban.com/v2/movie/search?q='
    url=start_url+keyword
    r = requests.get(url=url)
    return render_template('movie/searchResult.html', movieInfo=r.json())