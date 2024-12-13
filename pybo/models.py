from pybo import db

# Question 클래스가 db.Model을 상속받음
# 클래스는 빵틀 = 속성 (변수, 데이터) + 메서드 (함수)
# 클래스 -> 틀, 틀로 만든 것이 객체

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)


# db.Model이라는 클래스를 Question 받아서 새로운 클래스 생성
class Question(db.Model):
    # Column, primary key, nullable, Datetime -> DB에 관한 설정
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    def to_dict(self):
        """
        Question 객체를 딕셔너리 객체로 변환
        """
        return {
            "id": self.id,
            "subject": self.subject,
            "content": self.content,
            "create_date": self.create_date.isoformat() if self.create_date else None
        }

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)