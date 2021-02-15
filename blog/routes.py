from flask import render_template, url_for, flash, request, redirect
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc, or_
from is_safe_url import is_safe_url
from blog import app, db
from blog.models import User, Post, Comment, Like, Tag
from blog.forms import RegistrationForm, LoginForm, CommentForm, SearchForm
from blog.functions import flash_errors

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
    post=Post.query.get_or_404(post_id)
    comments = Comment.query.filter(Comment.post_id == post.id)
    if current_user.is_authenticated:
        like=Like.query.filter(Like.post_id==post.id, Like.liker_id==current_user.id).first()
        tag=Tag.query.filter(Tag.post_id==post.id, Tag.tagger_id==current_user.id).first()
    else:
        like=None
        tag=None
    form = CommentForm()
    return render_template('post.html',title=post.title, post=post, form=form, comments=comments, like=like, tag=tag)

@app.route('/post/<int:post_id>/comment', methods=['GET', 'POST']) 
@login_required
def post_comment(post_id):
    post = Post.query.get_or_404(post_id) 
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(content=form.comment.data, post_id=post.id, author_id=current_user.id))
        db.session.commit()
        flash("Your comment has been added to the post", "success")
        return redirect(f'/post/{post.id}')
    comments = Comment.query.filter(Comment.post_id == post.id)
    return render_template('post.html', post=post, comments=comments, form=form)

@app.route('/post/<int:post_id>/like')
@login_required
def post_like(post_id):
    post = Post.query.get_or_404(post_id)
    if not Like.query.filter_by(post_id=post.id, liker_id=current_user.id).all():
        db.session.add(Like(post_id=post.id, liker_id=current_user.id))
        post.likes+=1
        db.session.commit()
        flash("Liked!")
    else:
        flash("You already liked!")
    return redirect(f'/post/{post.id}')

@app.route('/post/<int:post_id>/tag')
@login_required
def post_tag(post_id):
    post = Post.query.get_or_404(post_id)
    current_tag=Tag.query.filter_by(post_id=post.id, tagger_id=current_user.id).first()
    if not current_tag:
        db.session.add(Tag(post_id=post.id, tagger_id=current_user.id))
        db.session.commit()
        flash("Tagged!")
    else:
        Tag.query.filter_by(post_id=post.id, tagger_id=current_user.id).delete(synchronize_session=False)
        db.session.commit()
        flash("Tag Removed!")
    next=request.args.get('next')
    if not is_safe_url(next, request.url_root):
        next=None
    return redirect(next or f'/post/{post.id}')

@app.route("/register", methods=['GET','POST'])
def register():
    next=request.args.get('next')
    if current_user.is_authenticated:
        flash("You've already logged in!")
        return redirect(next or url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,password=form.password.data,first_name=form.first_name.data,last_name=form.last_name.data,mobile_phone=form.mobile_phone.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Congratulations! Your registration has completed.")
        if not is_safe_url(next, request.url_root):
            return redirect(url_for('home'))
        return redirect(next or url_for('home'))
    else:
        flash_errors(form)
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data): 
            login_user(user)
            flash("Login Success!")
            next=request.args.get('next')
            if not is_safe_url(next, request.url_root):
                return redirect(url_for('home'))
            return redirect(next or url_for('home'))
        else:
            flash("Email or Password incorrect.")
    else:
        flash_errors(form)
    return render_template('login.html', title='Login', form=form)

@app.route("/search")
def search():
    if request.args.get('s'):
        search=request.args.get('s')
        post=Post.query.filter(or_(Post.content.like("%"+search+"%"),Post.title.like(search))).all()
        return render_template('search.html', title='Search', posts=post, search=search)
    else:
        return render_template('searchform.html', title='Search')

@app.route("/tagged")
@login_required
def tagged():
    post=Post.query.join(Tag, Post.id==Tag.post_id).filter_by(tagger_id=current_user.id).all()
    return render_template('tagged.html', title='Tagged Posts', posts=post)

@app.route("/allpost/<int:type>/<int:order>")
def allpost(type, order):
    if type==1:
        ty=Post.date
    elif type==0:
        ty=Post.likes
    else:
        return redirect(f"/allpost/0/0")
    if order==1:
        post=Post.query.order_by(ty).all()
    elif order==0:
        post=Post.query.order_by(desc(ty)).all()
    else:
        return redirect(f'/allpost/0/0')
    return render_template('allpost.html', title='All Posts', posts=post)
  
@app.route("/allpost")
def allpostroot():
    return redirect(f'/allpost/0/0')


@app.route("/logout")
def logout():
    logout_user()
    flash("You have successfully logged out!")
    next=request.args.get('next')
    if not is_safe_url(next, request.url_root):
        return redirect(url_for('home'))
    return redirect(next or url_for('home'))