from flaskblog import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
from flask_login import UserMixin

# Extension Setup -> Extension requires User model to have certain attribues 1) is authenticated 2) is annonomous 3) is id so we use class
# UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# One to Many Relation
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Name Post beacuse this will look into the python code 
    # creates a virtual/fake column in the post table, that means Post table will have virtaul/sudo column
    # and refer back to the user
    # https://www.youtube.com/watch?v=juPQ04_twtA
    posts = db.relationship('Post', backref='author', lazy=True) 
    # Lazy means how the data for the relationship is loaded
    # lazy = dynamic -> we will  be albe to use filter(), all() types of method while quering
    # lazy = select -> this will make different query for different table
    # lazy = joined -> this will return the results from both the table at one sort
    # https://www.youtube.com/watch?v=g1oFlq7D_nQ


    comments = db.relationship('Comment', backref='childpostauthor', lazy=True)

    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
            if self.has_liked_post(post):
                PostLike.query.filter_by(
                    user_id=self.id,
                    post_id=post.id).delete()

    def has_liked_post(self, post):
            return PostLike.query.filter(
                PostLike.user_id == self.id,
                PostLike.post_id == post.id).count() > 0

    

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    
    # telling python not to expect self parameter as an argument insted it should expect token as an argument
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # The __repr__ method simply tells Python how to print objects of a class
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # user.id because this will actually look into the database thats why smaller case
     
    likes = db.relationship('PostLike', backref='post', lazy='dynamic') 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # user.id because this will actually look into the database thats why smaller case
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.date_posted}')"

class Expert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=True)
    state = db.Column(db.CHAR, nullable=True)

    def __repr__(self):
        return f"Expert('{self.username}', '{self.email}', '{self.image_file}')"