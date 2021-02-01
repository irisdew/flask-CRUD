"""
4. Dashboard APIs

RecentBoardArticle API : 모든 게시판에 대해 각각의 게시판의 가장 최근 *3* 개의 게시판 글의 *title* 을 가져옵니다.
                         (*k* 개의 게시판이 있다면 최대 *k * 3* 개의 게시판 글의 *title* 을 반환합니다.)
"""

import dbModule
from flask import Flask, jsonify, redirect, url_for, render_template, request, session

app = Flask(__name__)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    db_class = dbModule.Database()
    sql = "SELECT * FROM boardarticle GROUP BY board_id ORDER BY create_date DESC"
    # "SELECT title FROM boardarticle GROUP BY board_id ORDER BY create_date DESC LIMIT 3"
    rows = db_class.executeAll(sql)
    return render_template('dashboard.html', rows = rows)


if __name__ == '__main__':
    app.run()