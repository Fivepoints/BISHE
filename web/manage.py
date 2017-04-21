import os

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
    # path='../ml-1m/users.dat'
    # count=0
    # fp = open(path,'r')
    # for line in fp.readlines():
    #     ilt = line.split('::')
    #     user = User(gender=ilt[1],age=ilt[2],occupation=ilt[3])
    #     db.session.add(user)
    #     count+=1
    #     print("\r当前进度: {:.2f}%".format(count/6040), end="")
    # print('begin writing to batabase')
    # db.session.commit()
    path = '../ml-1m/ratings.dat'
    count = 0
    fp = open(path, 'r')
    for line in fp.readlines():
        ilt = line.split('::')
        rating = Rating(user_id=ilt[0], movie_id=ilt[1], rating=ilt[2])
        count += 1
        if count == 10000:
            db.session.commit()
        db.session.add(rating)
        print("\r当前进度: {:.2f}%".format(count/1000209), end="")
    db.session.commit()

if __name__ == '__main__':

    manager.run()
  