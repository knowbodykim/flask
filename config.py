import os

BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

# MySQL 연결 URL : mysql+pymysql://<username>:<password>@<host>/<DBname>
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/pybo'
SQLALCHEMY_TRACK_MODIFICATIONS = False
