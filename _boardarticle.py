"""
BoardArticle APIs - 게시판 글 CRUD

Create API : title, content 를 입력받아 특정 게시판(board)에 새로운 글을 작성합니다.
Read API : 게시판의 글 목록을 가져오거나, 특정 게시판(board)에 글의 내용을 가져옵니다.
Update API : 게시판 글의 title, content를 변경합니다.
Delete API : 특정 게시판 글을 제거합니다.
"""

import dbModule
from flask import Flask, jsonify, redirect, url_for, render_template, request, session

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()