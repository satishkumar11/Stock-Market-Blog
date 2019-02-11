from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment, PostLike
from flaskblog.posts.forms import PostForm, PostComment

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        print("Hello1")
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    childpost = Comment.query.filter_by(post_id = post.id).all()
    postcomment = PostComment()
    print("One1")
    if postcomment.validate_on_submit():
        print("One2 = ",postcomment.content.data, post.id,  current_user.id)
        data = Comment(content = postcomment.content.data, post_id = post.id, user_id = current_user.id)
        print("----------Data-----------")
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('posts.post', post_id = post.id))
    return render_template('post.html', title=post.title, post=post, postcomment=postcomment, childpost=childpost)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() # No need for db.session.add because they are already in the database
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Form')

@posts.route("/delete_post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    print("Post ========== ",post)
    if post.author != current_user:
        abort(403)

    likes = PostLike.query.filter_by(post_id = post.id).all()
    print("comment ================= ",likes)
    if(likes):
        PostLike.query.filter_by(post_id = post.id).delete()
        db.session.commit()

    comment = Comment.query.filter_by(post_id = post.id).all()
    print("comment ================= ",comment)
    if(comment):
        Comment.query.filter_by(post_id = post.id).delete()
        db.session.commit()

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)
