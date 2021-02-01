# week6 assignment

5~6주차 웹 백엔드 과제

### 실행 방법
1. schema.sql에 있는 sql문을 mysql db에 실행시켜 user, board, boardarticle 테이블을 생성합니다.
2. user, board, boardarticle 테이블에 적절히 기본 데이터를 추가합니다.
3. vscode에서 python-env 가상환경을 구축합니다.
4. requirements.txt에 기록된 프로그램을 버전에 맞게 가상환경에 설치합니다.
5. dbModule.py를 열어 알맞게 mysql db를 연결합니다.
7. templates 폴더에 있는 html파일을 다운받습니다.
8. app.py를 터미널에서 실행시킵니다.
9. http://127.0.0.1:5000/ 에 app.py로 만든 서버가 실행됩니다.
10. api를 테스트합니다.

### 메인DB: MySQL
mysql db connection은 dbModule.py로 모듈화하여 사용했습니다. <br>
`(reference) https://kkamikoon.tistory.com/162 ` 

dbModule.py

```
import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(
            user = 'root',
            host = '127.0.0.1',
            port = 3306,
            db = 'week6_flask',
            charset = 'utf8'
        )
        print("Opened database successfully")
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)
    
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
```

###  Prototype 웹 사이트 구현
flask_restful을 활용하여 api를 만들고 Postman으로 api를 테스트 하는 방법을 5주차 토요일 오후 수업 때 배웠지만, <br>
익숙하게 사용하기에는 어려움이 있을 것 같았습니다. <br>
그래서 flask_restful을 사용하지 않고 flask만을 사용해서 api를 만들었고, <br>
눈으로 직접 확인할 수 있게 html파일을 만들고 form태그로 입력을 받아 api를 테스트 하는 방법으로 과제를 했습니다. <br>
웹페이지간의 연결성이나 기능, 디자인은 미비하지만, <br>
flask로 api를 만들고 render_template으로 페이지를 출력하여 결과를 바로 눈으로 확인해 볼 수 있었습니다. <br>
`(reference) elice 5주차 실습 파일`

### app.py
모든 API가 모여 있는 최종 과제 제출 py파일입니다.

_user.py / _board.py / _boadarticle.py / _dashboard.py 를 합친 파일입니다.

<details>
<summary>app.py</summary>
<div markdown="1">       

```
import dbModule
from flask import Flask, jsonify, redirect, url_for, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config.from_mapping(SECRET_KEY='dev')

"""
1. User APIs 
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
2. Board APIs
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
3. BoardArticle APIs 
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
@app.route('/dashboard', methods=['GET'])
def dashboard():
    db_class = dbModule.Database()
    sql = "SELECT * FROM boardarticle GROUP BY board_id ORDER BY create_date DESC"
    rows = db_class.executeAll(sql)
    return render_template('dashboard.html', rows = rows)


if __name__ == '__main__':
    app.run()
```
</div>
</details>

##### 1. User APIs
```
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
```
- home : session으로 로그인 상태를 확인하여 로그인 된 사용자에게는 로그온 화면을 / 일반 사용자에게는 인덱스 화면을 보여줍니다.
- login : email과 password를 입력받아 로그인합니다. password는 hash로 확인합니다.
- register : fullname, email, password를 입력받아 회원가입합니다. 회원정보는 db의 user테이블에 저장됩니다. 비밀번호는 hash로 저장됩니다.
- logout: session값을 바꿔 로그아웃합니다. 인덱스 화면으로 되돌아갑니다.

#####2. Board APIs
```
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
```
- boardhome: 전체 게시판 목록을 보여줍니다.
- search: 게시판 이름으로 게시판을 검색할 수 있습니다. 
- add: 게시판 name(이름), content(게시판 정보)를 입력받아 게시판을 생성합니다. 게시판 정보는 db의 board 테이블에 저장됩니다.
- delete: 화면에 표시된 게시판 번호인 uid를 입력받아 게시판을 삭제합니다. uid 번호는 db에 저장된 게시판 정보의 id와 다르기 때문에 sql문으로 해당 게시판의 id를 찾아 게시판을 db에서 삭제합니다.  
- update: 화면에 표시된 게시판 번호인 uid를 입력받아 게시판을 수정합니다. uid 번호는 db에 저장된 게시판 정보의 id와 다르기 때문에 sql문으로 해당 게시판의 id를 찾아 게시판 정보를 db에서 수정합니다. 화면에서 수정할 name, content 정보를 받아 db에 업데이트합니다. 

#####3. Boardarticle APIs
```

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
```
- show_board: 주소로 입력받은 board_id에 해당하는 게시판의 글 목록을 보여줍니다.
- show_article: 주소로 입력받은 board_id, board_article_id에 해당하는 게시글을 보여줍니다.
- post_article: title, content, board_id(저장할 게시판 번호)를 입력받아 새 게시글을 작성합니다. 게시글 정보는 db의 boardarticle 테이블에 저장됩니다.
- update_article: 주소로 입력받은 board_id, board_article_id에 해당하는 게시글을 수정합니다. 수정할 title, content, new_board_id(위치를 변경할 게시판)을 입력받아 db의 boardarticle 테이블에서 해당 게시글 정보를 수정합니다. 수정이 완료되면 '수정이 완료되었습니다'를 출력합니다.
- delete_article: 주소로 입력받은 board_id, board_article_id에 해당하는 게시글을 삭제합니다. db의 boardarticle 테이블에서 해당 게시글 정보를 삭제합니다. 삭제가 완료되면 '삭제가 완료되었습니다'를 출력합니다.

#####4. Dashboard API
```
@app.route('/dashboard', methods=['GET'])
def dashboard():
    db_class = dbModule.Database()
    sql = "SELECT * FROM boardarticle GROUP BY board_id ORDER BY create_date DESC"
    rows = db_class.executeAll(sql)
    return render_template('dashboard.html', rows = rows)
```
- dashboard: 게시판별로 가장 최신에 작성된 글 1개씩만을 보여줍니다. 

- Dashboard API는 완벽하게 만들지 못했습니다. <br>
SQL문을 "SELECT * FROM boardarticle GROUP BY board_id ORDER BY create_date DESC"으로 하면 <br>
그룹별(board별)로 가장 최신의 글 1개씩 밖에 불러오지 못합니다. <br>
분명 다른 방법이 있겠지만... <br>
일단 각 게시판별로 최신의 글 1개씩만을 불러오는 형태로 만들었습니다. <br>

### 아쉬운 점 / 다음에 보완할 점
- flask_resful 등을 활용해서 restful하게 API를 설계해보고 싶습니다.
- 웹페이지간의 연결성이 있게 페이지를 설계해보고 싶습니다.
- css, bootstrap을 적용해보고 싶습니다.
- ORM(SQLAlchemy)을 이번에는 사용하지 않았는데 ORM으로 API를 만들어볼 것입니다.
- form대신 ajax나 다른 방법으로 데이터를 주고받도록 만들어보고 싶습니다. 
- 현재는 http://localhost:5000 에서만 실행됩니다. 다음에는 배포까지 해보고 싶습니다!