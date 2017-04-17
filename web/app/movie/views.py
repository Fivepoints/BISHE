from . import movie
from flask import render_template, request

@movie.route('/tagList')
def tagList():
    with open('app/static/tags.dat') as f:
        taglt = eval(f.read())
        f.close()
    return render_template('movie/tag.html', taglt=taglt)