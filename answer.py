import pymysql
from flask import Flask, jsonify, request, session
from flask_restful import reqparse, abort, Api, Resource

from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
api = Api(app)

db = pymysql.connect(
        user = 'root',
        host = '127.0.0.1',
        port = 3306,
        db = 'week6_flask',
        charset = 'utf8',
    )

cursor = db.cursor()

parser = reqparse.RequestParser()
parser.add_argument("id")
parser.add_argument("name")

class Board(Resource):
    def get(self): ## Read
        sql = "SELECT id, name FROM `board`"
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(status = "success", result = result)
        
    
    def post(self):  ## Create 생성
        args = parser.parse_args()
        sql = "INSERT INTO `board` (`name`) VALUES (%s)"
        cursor.execute(sql, (args['name']))
        return jsonify(status = "success", result = {"name": args["name"]})
    
    
    def put(self):  ## Update 수정
        args = parser.parse_args()
        sql = "UPDATE `board` SET name = %s WHERE `id` = %s"
        return jsonify(status = "success", result = {"id": args["id"], "name": args["name"]})
    
    
    def delete(self):  ## Delete 
        args = parser.parse_args()
        sql = "DELETE FROM `board` WHERE `id` = %s"
        cursor.execute(sql, (args["id"]))
        return jsonify(status = "success", result = {"id": args["id"]})


api.add_resource(Board, '/board')


#---------------------------------------------------------------------

parser.add_argument("id")
parser.add_argument("title")
parser.add_argument("content")
parser.add_argument("board_id")

class BoardArticle(Resource):
    def get(self, board_id=None, board_article_id=None):
        if board_article_id:
            sql = "SELECT id, title, content FROM `boardArticle` WHERE `id`=%s"
            cursor.execute(sql, (board_article_id,))
            result = cursor.fetchone()
        else:
            sql = "SELECT id, title, content FROM `boardArticle` WHERE `board_id`=%s"
            cursor.execute(sql, (board_id,))
            result = cursor.fetchall()
            
        return jsonify(status = "success", result = result)

    def post(self, board_id):
        args = parser.parse_args()
        sql = "INSERT INTO `boardArticle` (`title`, `content`, `board_id`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (args['title'], args['content'], args['board_id']))
        db.commit()
        
        return jsonify(status = "success", result = {"title": args["title"]})
        
        
    def put(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        sql = "UPDATE `boardArticle` SET title = %s, content = %s WHERE `id` = %s"
        cursor.execute(sql, (args['title'], args["content"], args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"title": args["title"], "content": args["content"]})
        
        
    def delete(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        sql = "DELETE FROM `boardArticle` WHERE `id` = %s"
        cursor.execute(sql, (args["id"], ))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"]})

api.add_resource(BoardArticle, '/board/<board_id>', '/board/<board_id>/<board_article_id>')

#---------------------------------------------------------------------

"""
User APIs : 유저 SignUp / Login / Logout

SignUp API : *fullname*, *email*, *password* 을 입력받아 새로운 유저를 가입시킵니다.
Login API : *email*, *password* 를 입력받아 특정 유저로 로그인합니다.
Logout API : 현재 로그인 된 유저를 로그아웃합니다.
"""

# session을 위한 secret_key 설정
app.config.from_mapping(SECRET_KEY='dev')

@app.route('/auth/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email address already exists")
            return redirect(url_for('signup'))

        new_user = User(email=email, username=username,
                        password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    else:
        return render_template("signup.html") 


@app.route('/auth/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid user info")
            return redirect(url_for('login'))

        return redirect(url_for("profile"))
    else:
        return render_template('login.html')


@app.route('/auth/logout')
def logout():
    return "logout"



if __name__ == '__main__':
    app.run()