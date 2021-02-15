from datetime import datetime
from blog import db
from blog import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes=db.Column(db.Integer, nullable=False, default=0)
    comment=db.relationship('Comment',backref='post',lazy=True)
    like=db.relationship('Like',backref='post',lazy=True)
    tag=db.relationship('Tag',backref='post',lazy=True)

    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='user', lazy=True)
    comment=db.relationship('Comment',backref='user',lazy=True)
    like=db.relationship('Like',backref='user',lazy=True)
    tag=db.relationship('Tag',backref='user',lazy=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    mobile_phone = db.Column(db.String(11))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    parent_id=db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    parent=db.relationship('Comment',backref='comment_parent',remote_side=id,lazy=True)

    def __repr__(self):
        return f"Post('{self.date}','{self.content}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    liker_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Like('{self.id}','{self.date}')"

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    tagger_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Like('{self.id}','{self.date}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

