import dbModule
from flask import Flask, jsonify, redirect, url_for, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config.from_mapping(SECRET_KEY='dev')

"""
1. User APIs : 유저 SignUp / Login / Logout
"""

@app.route('/')
def home():
    if session.get('logged_in'):
        return render_template('loggedin.html')
    else:
        return render_template('index.html')


@app.route('/login', methods = ['GET', 'POST'])  
def login():  
    if request.method == 'POST':
        email = request.form['email']  
        password = request.form['password']
        db_class = dbModule.Database()
        sql = f"SELECT * FROM user WHERE email='{email}'"
        row = db_class.executeOne(sql)
        print(row)
        if row is not None:
            if check_password_hash(row['password'], password):
                session['logged_in'] = True
                return render_template('loggedin.html')
            else:
                return '비밀번호가 틀립니다.'
        else: 
            return '아이디가 없습니다'       
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        hashed_password = generate_password_hash(request.form['password'])
        db_class = dbModule.Database()
        sql = f"INSERT INTO user (fullname, email,  password) VALUES ('{fullname}', '{email}', '{hashed_password}')"
        db_class.execute(sql)
        db_class.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('index.html')

"""
2. Board APIs - 게시판 CRUD
"""

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
            content = request.form['content']
            db_class = dbModule.Database()
            print(name, content)
            sql = f"INSERT INTO board (name, content) VALUES ('{name}', '{content}')"
            db_class.execute(sql)
            db_class.commit()
        except:
            db_class.rollback()
        finally:
            return redirect(url_for('boardhome'))
    else:
        db_class = dbModule.Database()
        sql = "SELECT * FROM board"
        rows = db_class.executeAll(sql)
        return render_template('add.html', rows = rows)


@app.route('/delete/<int:uid>')
def delete(uid):
    db_class = dbModule.Database()
    rows = db_class.executeAll("SELECT * FROM board")
    row_id = rows[uid-1]['id']
    sql = f"DELETE FROM Board WHERE id='{row_id}'"
    db_class.execute(sql)
    db_class.commit()
    return redirect(url_for('boardhome'))


@app.route('/update/<int:uid>', methods=['GET','POST'])
def update(uid):
    if request.method =='POST':
        name = request.form['name']
        content = request.form['content']
        db_class = dbModule.Database()
        rows = db_class.executeAll("SELECT * FROM board")
        row_id = rows[uid-1]['id']
        sql = f"UPDATE board Set name='{name}', content='{content}' WHERE id='{row_id}'"
        db_class.execute(sql)
        db_class.commit()
        return redirect(url_for('boardhome'))
    else:
        db_class = dbModule.Database()
        sql = "SELECT * FROM board"
        rows = db_class.executeAll(sql)
        row = rows[uid-1]
        return render_template('update.html', index=uid, row=row)

"""
3. BoardArticle APIs - 게시판 글 CRUD
"""

@app.route('/board/<int:board_id>')
def show_board(board_id):
    db_class = dbModule.Database()
    sql = "SELECT id, title, content FROM `boardarticle` WHERE `board_id`=%s"
    result = db_class.executeAll(sql, (board_id,))
    board_name = db_class.executeOne(f"SELECT name FROM board WHERE id={board_id}")['name']
    return render_template('boardarticle.html', board_name=board_name, result=result)

@app.route('/board/<int:board_id>/<int:board_article_id>')
def show_article(board_id, board_article_id):
        db_class = dbModule.Database()
        sql = f"SELECT * FROM `boardarticle` WHERE (`board_id`={board_id}) && (`id`={board_article_id})"
        result = db_class.executeOne(sql)
        return render_template('article.html', result=result)

@app.route('/post', methods = ['GET', 'POST'])
def post_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        board_id = request.form['board_id']
        print(title, content, board_id)
        db_class = dbModule.Database()
        sql = f"INSERT INTO boardarticle (`title`, `content`, `board_id`) VALUES ('{title}', '{content}', '{board_id}')"
        db_class.execute(sql)
        db_class.commit()
        return "게시글 추가가 완료되었습니다"
    else:
        return render_template('post.html')

@app.route('/board/<int:board_id>/<int:board_article_id>/update', methods = ['GET', 'POST'])        
def update_article(board_id, board_article_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_board_id = request.form['board_id']
        print(title, content, new_board_id)
        db_class = dbModule.Database()
        sql = "UPDATE `boardArticle` SET title = %s, content = %s, board_id = %s WHERE `id` = %s"
        db_class.execute(sql, (title, content, new_board_id, board_article_id))
        db_class.commit()
        return '수정이 완료되었습니다'
    else:
        return render_template('update_article.html', board_id = board_id, board_article_id = board_article_id)
        
@app.route('/board/<int:board_id>/<int:board_article_id>/delete')        
def delete_article(board_id, board_article_id):
    db_class = dbModule.Database()
    sql = "DELETE FROM `boardArticle` WHERE `id` = %s"
    db_class.execute(sql, (board_article_id))
    db_class.commit()
    return '삭제가 완료되었습니다'

"""
4. Dashboard APIs
"""

import dbModule
from flask import Flask, jsonify, redirect, url_for, render_template, request, session

app = Flask(__name__)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    db_class = dbModule.Database()
    sql = "SELECT * FROM boardarticle GROUP BY board_id ORDER BY create_date DESC"
    rows = db_class.executeAll(sql)
    return render_template('dashboard.html', rows = rows)


if __name__ == '__main__':
    app.run()