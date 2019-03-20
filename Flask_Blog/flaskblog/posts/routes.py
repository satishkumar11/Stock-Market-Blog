from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, Markup)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment, PostLike
from flaskblog.posts.forms import PostForm, PostComment, Payment
import stripe

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # print("Hello1")
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
    # print("One1 = ", current_user)
    if postcomment.validate_on_submit():
        if(current_user.is_authenticated):
            # print("One2 = ",postcomment.content.data, post.id,  current_user.id)
            data = Comment(content = postcomment.content.data, post_id = post.id, user_id = current_user.id)
            # print("----------Data-----------")
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('posts.post', post_id = post.id))
        else:
            flash('You dont have permission to do that. Please check your account !', 'danger')
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
    # print("Post ========== ",post)
    if post.author != current_user:
        abort(403)

    likes = PostLike.query.filter_by(post_id = post.id).all()
    # print("comment ================= ",likes)
    if(likes):
        PostLike.query.filter_by(post_id = post.id).delete()
        db.session.commit()

    comment = Comment.query.filter_by(post_id = post.id).all()
    # print("comment ================= ",comment)
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

pub_key = 'pk_test_b4cwVvHM6XiU7YYRGGx60lq8'
secret_key = 'sk_test_qJpB5juHtLFeTpoZQY1yjqJ1'
stripe.api_key = secret_key

@posts.route("/payment/<int:expert_id>", methods=['GET', 'POST'])
@login_required
def payment(expert_id):
    # print("expert_id = ",expert_id)
    form = Payment()
    if form.validate_on_submit():
        flash('Your payment has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('payment.html', title='Payment', form=form, legend='Payment', pub_key=pub_key)

@posts.route('/pay', methods=['POST'])
def pay():
    
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=19900,
        currency='usd',
        description='The Product'
    )

    return redirect(url_for('posts.thanks'))

@posts.route('/thanks')
def thanks():
    return render_template('thanks.html')


@posts.route("/chart", methods=['GET', 'POST'])
def chart():
    bar_labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
    ]   

    bar_values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
    ]

    colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

    return render_template('chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values)
