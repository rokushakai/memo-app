import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
DATABASE = 'posts.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# メモの一覧表示
@app.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id, title FROM posts ORDER BY id DESC')
    posts = cur.fetchall()
    return render_template('index.html', posts=posts)

# 新しいメモの作成
@app.route('/create', methods=('GET', 'POST'))
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
        return redirect(url_for('index'))

    return render_template('create.html')

# メモの詳細表示
@app.route('/<int:post_id>')
def post(post_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id, title, content FROM posts WHERE id = ?', (post_id,))
    post = cur.fetchone()
    if post is None:
        return 'メモが見つかりません。', 404
    return render_template('post.html', post=post)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)