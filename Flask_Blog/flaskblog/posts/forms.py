from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    content = TextAreaField('Content', validators = [DataRequired()])
    submit = SubmitField('Post')

class PostComment(FlaskForm):
    content = TextAreaField('Content', validators = [DataRequired()])
    submit = SubmitField('Post Comment')

class Market(FlaskForm):
    stockname = StringField('Get Stock Status', validators = [DataRequired()])
    submit = SubmitField('Check Stock Status')