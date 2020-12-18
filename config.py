import os



basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True #this is used to prevent Cross-Site Request Forgery, increasing the security of our form input
SECRET_KEY = '7ashf37haiiofja09d8'
