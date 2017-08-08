from flask import Flask, render_template, url_for, request, flash, redirect, session
# from data import Articles
import pymysql
from wtforms import StringField, TextAreaField, PasswordField, validators, Form
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='myflaskapp',
                             cursorclass=pymysql.cursors.DictCursor)

# Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    cur = connection.cursor()
    result = cur.execute('select * from articles')
    articles = cur.fetchall()
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Article Found'
        return render_template('articles.html', msg=msg)
    cur.close()

@app.route('/article/<string:id>/')
def article(id):
    cur = connection.cursor()
    result = cur.execute('select * from articles where id=%s', [id])
    article = cur.fetchone()
    return render_template('article.html', article=article)

class RegisterForm(Form):
    name = StringField('Name', validators=[validators.length(min=1, max=50)])
    username = StringField('Username', validators=[validators.length(min=4, max=25)])
    email = StringField('Email', validators=[validators.length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.data_required(),
        validators.equal_to('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm password')

@app.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        # 密码加密
        password = sha256_crypt.encrypt(str(form.password.data))

        # create cursor
        cur = connection.cursor()

        cur.execute("insert into users (name, email, username, password) values(%s, %s, %s, %s)",
                    (name, email, username, password))
        # Commit to db
        connection.commit()
        # Close connection
        cur.close()

        flash('Yor are now registred and can log in', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

# User Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get Form field
        username = request.form['username']
        passworld_candidate = request.form['password']

        # Create database cursor

        cur = connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users where username= %s", [username])

        if result > 0:
            # Get started hash
            data = cur.fetchone()
            password = data['password']

            # Compare password
            if sha256_crypt.verify(passworld_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash("You are now logged in ", 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


# Check user if logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized,Please login', 'danger')
            return redirect(url_for('login'))
    return decorated_function


@app.route('/dashboard')
@login_required
# 装饰器要放在路由的下面
def dashboard():
    cur = connection.cursor()
    result = cur.execute('select * from articles')
    articles = cur.fetchall()
    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Article Found'
        return render_template('dashboard.html', msg=msg)
    cur.close()


@app.route('/logout')
def logout():
    session.clear()
    flash("You are now logged out", 'success')
    return redirect(url_for('login'))

class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

@app.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm(request.form)
    if request.method =='POST' and form.validate():
        title = form.title.data
        body = form.body.data
        cur = connection.cursor()
        cur.execute("Insert into articles (title,body,author) values(%s,%s,%s)",
                (title, body, session['username']))
        connection.commit()
        cur.close()
        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)

@app.route('/edit_article/<string:id>', methods=['POST', 'GET'])
@login_required
def edit_article(id):
    cur = connection.cursor()
    result = cur.execute("select * from  articles where id = %s", [id])
    article = cur.fetchone()
    form = ArticleForm(request.form)
    # populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        cur = connection.cursor()
        cur.execute('update articles set title=%s, body=%s where id = %s', [title, body, id])
        connection.commit()
        cur.close()
        flash('Article Updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)

@app.route('/delete_article/<string:id>', methods=['POST'])
@login_required
def delete_article(id):
    cur = connection.cursor()
    cur.execute('delete from articles where id =%s ', [id])
    connection.commit()
    cur.close()
    flash('Article Delete', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.secret_key = 'you can never guess'
    app.run(debug=True)