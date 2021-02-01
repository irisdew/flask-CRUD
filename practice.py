from flask import Flask, jsonify, redirect, url_for, render_template, request, session
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

import dbModule

app = Flask(__name__)

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        value = request.form['input']
        return f"{value}님 환영합니다."
    
    if request.method == 'GET':
        return render_template('welcome.html')

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %s' % post_id
    
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'Subpath %s' % subpath

@app.route('/people')
def json():
    people = [{'name':'Elice', 'birth-year':2015}, 
              {'name':'Dodo', 'birth-year':2016},
              {'name':'Queen', 'birth-year':2017}]
    return jsonify(people)

# 관리자 페이지로 이동
@app.route('/admin')
def admin():
    return "<h1>This is Admin Page</h1>"


# 학생 페이지로 이동
@app.route('/student')
def student():
    return "This is Student Page"


# redirect() 함수는 페이지에 다시 연결한다는 뜻으로 마치 페이지를 새로고침 한 것과 같은 동작합니다.
@app.route('/user/<name>')
def user(name):
    # 전달 받은 name이 'admin' 이라면?
    if name == 'admin':
        return redirect(url_for('admin'))

    # 전달 받은 name이 'student' 라면?
    elif name == 'student':
        return redirect(url_for('student'))

    else:        
        return 'User %s' % name


## <로그인>
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
userinfo = {'Elice': '1q2w3e4r!!'}


@app.route('/')
def home():
    if session.get('logged_in'):
        return render_template('loggedin.html')
    else:
        return render_template('index.html')


# login 주소에서 POST 방식의 요청을 받았을 때
@app.route('/login', methods = ['GET', 'POST'])  
def login():  
    if request.method == 'POST':
        id = request.form['id']  
        password = request.form['pwd'] 
        try:
            if (id in userinfo):
                if userinfo[id] == password:
                    session['logged_in'] = True
                    return render_template('loggedin.html')
                else:
                    return '비밀번호가 틀립니다.'
            return '아이디가 없습니다.'
        except:
            return "Don't login"
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        userinfo[request.form['username']] = request.form['password']
        print(userinfo)
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('index.html')

## <게시판>

board = []

@app.route('/board')
def boardhome():
    db_class = dbModule.Database()
    sql = "SELECT * FROM board"
    rows = db_class.executeAll(sql)
    return render_template('board.html', rows = rows)

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        db_class = dbModule.Database()
        sql = f"SELECT * FROM board WHERE name='{name}'"
        rows = db_class.executeAll(sql)
        print(rows)
        return render_template('search.html', rows = rows)
    else:
        return render_template('search.html')


@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            name = request.form['name']
            context = request.form['context']
            db_class = dbModule.Database()
            print(name, context)
            sql = f"INSERT INTO board (name, content) VALUES ('{name}', '{context}')"
            db_class.execute(sql)
            db_class.commit()
        except:
            db_class.rollback()
        finally:
            return redirect(url_for('boardhome'))
    else:
        return render_template('board.html', rows = board)


@app.route('/delete/<int:uid>')
def delete(uid):
    db_class = dbModule.Database()
    sql = f"DELETE FROM Board WHERE id='{uid}'"
    db_class.execute(sql)
    db_class.commit()
    return redirect(url_for('boardhome'))


@app.route('/update/<int:uid>', methods=['GET','POST'])
def update(uid):
    if request.method =='POST':
        name = request.form['name']
        context = request.form['context']
        db_class = dbModule.Database()
        sql = f"UPDATE board Set name='{name}', content='{context}' WHERE id='{uid}'"
        db_class.execute(sql)
        db_class.commit()
        return redirect(url_for('boardhome'))
    else:
        db_class = dbModule.Database()
        sql = f"SELECT * FROM board WHERE id ='{uid}'"
        rows = db_class.executeOne(sql)
        return render_template('update.html', index=uid, rows=rows)


@app.errorhandler(404)
#2번을 해보세요!
def page_not_found(error):
    #3번을 해보세요!
    app.logger.error(error)
    #4번을 해보세요!
    return render_template('page_not_found.html')


if __name__ == '__main__':
    app.run()