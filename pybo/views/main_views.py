from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')
# 밑에 접속하는 주소의 기본값
# 예) url_prefix = '/main'
# localhost:5000/


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return 'Pybo index'