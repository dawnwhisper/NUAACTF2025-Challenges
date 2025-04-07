from flask import Flask, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'ctf.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flag (
                flag TEXT
            )
        ''')
        cursor.execute("INSERT OR IGNORE INTO flag (flag) VALUES ('FLAG{SQLi_Second_Order_123}')")
        cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'secure_pass')")
        db.commit()

init_db()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = user['username']
            return redirect(url_for('profile'))
        return "<script>alert('登录失败！');window.location.href='/login';</script>"
    return '''
    <html>
    <head>
        <title>登录</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
    </head>
    <body class="container mt-5">
        <div class="card p-4 shadow-lg">
            <h2 class="text-center">登录</h2>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">用户名</label>
                    <input type="text" name="username" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">密码</label>
                    <input type="password" name="password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">登录</button>
            </form>
            <div class="text-center mt-3">
                <a href="/register">没有账号？注册</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            return "<script>alert('注册成功！');window.location.href='/login';</script>"
        except sqlite3.IntegrityError:
            return "<script>alert('用户名已存在！');window.location.href='/register';</script>"
    return '''
    <html>
    <head>
        <title>注册</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
    </head>
    <body class="container mt-5">
        <div class="card p-4 shadow-lg">
            <h2 class="text-center">注册</h2>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">用户名</label>
                    <input type="text" name="username" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">密码</label>
                    <input type="password" name="password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-success w-100">注册</button>
            </form>
            <div class="text-center mt-3">
                <a href="/login">已有账号？登录</a>
            </div>
        </div>
    </body>
    </html>
    '''
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return f'''
    <html>
    <head>
        <title>个人资料</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
    </head>
    <body class="container mt-5">
        <div class="card p-4 shadow-lg">
            <h2 class="text-center">个人资料</h2>
            <p class="text-center">用户名: <strong>{session['username']}</strong></p>
            <div class="text-center mt-3">
                <a href="/change_password" class="btn btn-warning">修改密码</a>
                <a href="/logout" class="btn btn-danger">退出登录</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_password = request.form['new_password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, session['username']))
        cursor.execute("SELECT * FROM users WHERE username = '%s'" % session['username'])
        new_user = cursor.fetchone()
        new_username = new_user['username']
        db.commit()
        safe_username = new_username.replace("'", "\\'")
        return f"<script>alert(' {safe_username} 密码已修改！');window.location.href='/profile';</script>"
    return '''
    <html>
    <head>
        <title>修改密码</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
    </head>
    <body class="container mt-5">
        <div class="card p-4 shadow-lg">
            <h2 class="text-center">修改密码</h2>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">新密码</label>
                    <input type="password" name="new_password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-success w-100">提交</button>
            </form>
            <div class="text-center mt-3">
                <a href="/profile" class="btn btn-secondary">返回</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
