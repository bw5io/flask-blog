from flask import render_template, url_for
from blog import app, db
from blog.models import User, Post
from flask import request, redirect
from blog.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title, post=post)

@app.route("/register", methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if request.method=='POST':
        user=User(username=form.username.data,email=form.email.data,password=form.password.data,first_name=form.first_name.data,last_name=form.last_name.data,mobile_phone=form.mobile_phone.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('register_complete'))
    return render_template('register.html', title='Register', form=form)

@app.route("/register_complete")
def register_complete():
    return render_template('register_complete.html', title='Congratulations!')

@app.route("/login", methods=['GET','POST'])
def login():
    form=LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data): 
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))