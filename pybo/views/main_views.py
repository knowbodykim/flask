from flask import Blueprint, url_for, render_template, jsonify, request
from werkzeug.utils import redirect
from pybo.models import Question
from pybo import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')
# 밑에 접속하는 주소의 기본값
# 예) url_prefix = '/main'
# localhost:5000/

@bp.route('/')
def index():
    return redirect(url_for('question._list'))

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/test')
def test():
    # 관련 웹페이지 주소
    # redirect("페이지url")
    # render_template() 페이지를 template 사용하는 경우 사용
    # redirect(url_for('다른 라우트에 있는 page'))
    
    return render_template("test.html")

@bp.route('/test2')
def test2():
    return render_template("./test/test2.html")


@bp.route('/load_question')
def load_question():
    # 1. DB에서 값을 읽어오기
    # Question.query.all() 모든 레코드 조회
    # Question.query.first() 첫번째 레코드 조회
    # Question.query.get(id) 특정 ID로 조회
    # Question.query.filter_by(field=value) 단순 조건 필터링
    # Question.query.filter(Question.field == value) 보다 복잡한 조건 필터링
    # Question.query.order_by(Question.create_date.desc()) 생성날짜 역순 정렬

    question_list = Question.query.order_by(Question.create_date.desc())
    # 확인을 위해서 question_list를 출력
    print("question 리스트 :", question_list)
    # 2. JSON 변환
    question_list_dict = [question.to_dict() for question in question_list]
    # 3. 변환 결과를 return
    return jsonify(question_list_dict)

# 생략이 되어 있지만 GET방식, query 가져올 수 있음
# http://<주소>/load_question_id?id=<번호>

@bp.route('/load_question_id', methods=['GET'])
def load_question_id():
    # 1. 쿼리 파라미터 가져오기
    # request는 맨 위에 from flask import request 추가
    # 클라이언트에서
    # http://<ip주소>/load_question_id?id=3
    # 위 주소에서 id 값을 추출해서 가져옴
    id = request.args.get('id')

    # 2. 기본 조회 : 모든 데이터
    if not id:
        return "id값이 없습니다."
    else:
        # id 값을 기준으로 필터링
        question = Question.query.get(id)

        return jsonify(question.to_dict())

# GET이 아닌 POST 방식으로 값을 가져옴
# 엔드포인트(주소) 는 같아도 상관이 없음
@bp.route('/load_question_id', methods=['POST'])
# POST 방식은 JSON으로 데이터 가져옴
# GET 방식과는 다르게 id값을 가져와야 함.
def load_question_id_post():
    # 1. 요청 데이터 가져오기
    # JSON 요청에서 "ID" 필드를 가져옴
    data = request.get_json()
    print("data : ", data)
    id =  data.get('id') if data else None

    # 2. 기본 조회 : 모든 데이터
    if not id:
        return jsonify({"errer":"id 값이 없습니다."}), 400
    
    # 3. 데이터 조회
    question = Question.query.get(id)
    if not question:
        return jsonify({"error":f"id {id}에 해당하는 데이터가 없습니다."}), 400
    
    # 4. 결과 반환

    return jsonify(question.to_dict())


@bp.route('/add_question', methods=['POST'])

def add_question_post():
    data = request.get_json()
    print("data : ", data)
    subject = data.get('subject') if data else None
    content = data.get('content') if data else None

    print(f"subject {subject}, content {content}")
    # 3. 새로운 Question 객체 생성
    new_question = Question(
        subject = subject,
        content = content,
        create_date = datetime.now()
    )
    
    # 데이터베이스 세션에 추가
    # DB라는 것을 사용하기 위해서는 아래 코드를 파일 윗부분에 추가
    # from pybo import db
    db.session.add(new_question)

    # 변경사항 커밋
    db.session.commit()
    
    # db.session.commit() 데이터 추가 커밋
    # 제대로 실행안되고 문제가 발생하면?
    # 문제가 발생하면 서버 프로그램이 중단
    # try, except 구문을 사용하면 문제발생시
    # 적절한 코드가 실행되어 종료 방지
    # try, except 구문을 사용하여 처리하여야 함.

    try:
        db.session.commit()
        print("Commit successfull")
        
    except SQLAlchemyError as e:
        # SQLAlchemyError를 사용하기 위해서
        # 상단에 from sqlalchemy.exc import SQLAlchemyError
        db.session.rollback()
        print(f"Commit failed : {str(e)}")
        return jsonify({"error" : "데이터 추가실패"+str(e)}), 500

    # 4. 결과 반환
    return jsonify({"message" : "추가가 완료되었습니다."}), 200


# @bp.route('/')
# def index():
#    question_list = Question.query.order_by(Question.create_date.desc())
#    return render_template('question/question_list.html', question_list=question_list)
    # render_template("html 파일경로", html 변수 = python 변수)
    # DB에서 query해온 question_list를 question_list.html 안에 대입


# @bp.route('/detail/<int:question_id>/')
# def detail(question_id):
#     question = Question.query.get_or_404(question_id)
#     return render_template('question/question_detail.html', question=question)


