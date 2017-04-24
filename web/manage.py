import os, re

from app import create_app, db
from app.models import User, Movie, Rating

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)



def make_shell_context():
    return dict(app=app, db=db, User=User, Movie=Movie, Rating=Rating)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

def dat2base():

    '''transefer dat to database'''
    path='../ml-latest-small/movies.csv'
    count=0
    fp = open(path,'r')
    fp.readline()
    regex = re.compile("(\d+),\"?(.+)\"?,(.+)")
    for line in fp.readlines():
        ilt = regex.search(line)
        if ilt.group(2).endswith("\""):
            movie = Movie(movie_id=ilt.group(1), movie_name=ilt.group(2)[:-2], movie_genres=ilt.group(3))
        else:
            movie = Movie(movie_id=ilt.group(1),movie_name=ilt.group(2),movie_genres=ilt.group(3))
        db.session.add(movie)
        count+=1
        if count % 1000 == 0:
            db.session.commit()
        print("\r当前进度: {:.2f}%".format(count / 9126 * 100), end="")
    db.session.commit()

    path = '../ml-latest-small/ratings.csv'
    count = 0
    fp = open(path, 'r')
    fp.readline()
    for line in fp.readlines():
        ilt = line.split(',')
        rating = Rating(user_id=ilt[0], movie_id=ilt[1], rating=ilt[2])
        count += 1
        if count == 1000:
            db.session.commit()
        db.session.add(rating)
        print("\r当前进度: {:.2f}%".format(count/100005*100), end="")
    db.session.commit()

    path = '../ml-latest-small/ratings.csv'
    count = 0
    fp = open(path, 'r')
    fp.readline()
    for line in fp.readlines():
        ilt = line.split(',')
        if User.query.filter_by(user_id=ilt[0]).first() is not None:
            continue
        user = User(user_id=ilt[0],username='unKnow Man'+str(ilt[0]))
        count += 1
        if count == 1000:
            db.session.commit()
        db.session.add(user)
        print("\r当前进度: {:.2f}%".format(count / 100005 * 100), end="")
    db.session.commit()

if __name__ == '__main__':
    manager.run()
    dat2base()

  