"""
User APIs : 유저 SignUp / Login / Logout

SignUp API : *fullname*, *email*, *password* 을 입력받아 새로운 유저를 가입시킵니다.
Login API : *email*, *password* 를 입력받아 특정 유저로 로그인합니다.
Logout API : 현재 로그인 된 유저를 로그아웃합니다.
"""

import dbModule
from flask import Flask, jsonify, redirect, url_for, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config.from_mapping(SECRET_KEY='dev')

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


if __name__ == '__main__':
    app.run()
