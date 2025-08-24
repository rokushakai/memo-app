import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, Blueprint, Response
import csv
from io import StringIO

memo_bp = Blueprint('memo', __name__, url_prefix='/memo')
DATABASE = 'posts.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@memo_bp.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id, title FROM posts ORDER BY id DESC')
    posts = cur.fetchall()
    return render_template('index.html', posts=posts)

@memo_bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            return 'タイトルは必須です。', 400
        db = get_db()
        cur = db.cursor()
        cur.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        db.commit()
        return redirect(url_for('memo.index'))
    return render_template('create.html')

@memo_bp.route('/<int:post_id>')
def post(post_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id, title, content FROM posts WHERE id = ?', (post_id,))
    post = cur.fetchone()
    if post is None:
        return 'メモが見つかりません。', 404
    return render_template('post.html', post=post)

@memo_bp.route('/export_csv')
def export_csv():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id, title, content FROM posts ORDER BY id DESC')
    posts = cur.fetchall()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'タイトル', '内容'])
    for post in posts:
        cw.writerow(post)
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=memos.csv"})

def create_app():
    app = Flask(__name__)
    app.teardown_appcontext(close_connection)
    app.register_blueprint(memo_bp)
    return app

app = create_app()