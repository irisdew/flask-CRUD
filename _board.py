"""
Board APIs - 게시판 CRUD

Create API : name 을 입력받아 새로운 게시판을 만듭니다.
Read API : 현재 등록된 게시판 목록을 가져옵니다.
Update API : 기존 게시판의 name 을 변경합니다.
Delete API : 특정 게시판을 제거합니다.
"""

import dbModule
from flask import Flask, jsonify, redirect, url_for, render_template, request, session

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run()