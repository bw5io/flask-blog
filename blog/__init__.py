from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)   
app.config['SECRET_KEY']='2ea381c499e2df1774a2387309e4304579e3184bc143e629'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://c2108464:tuss1SAIN6boct_koh@csmysql.cs.cf.ac.uk:3306/c2108464_cmt120flask'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


from blog import routes
from blog.models import User, Post, Comment
from blog.views import AdminView

admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session)) 
admin.add_view(AdminView(Post, db.session)) 
admin.add_view(AdminView(Comment, db.session))