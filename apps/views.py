from flask import render_template, flash, redirect, url_for , g, session
from .forms import LoginForm, SignupForm, EditProfileForm,PostForm
from models import User, Post
from flask_login import LoginManager, UserMixin, login_user, logout_user,current_user, login_required
from apps import lm
from apps import db
from apps import app
from apps import oauth, models
from oauth import app_oauth
from datetime import datetime
import sys
from config import POSTS_PER_PAGE


app.register_blueprint(app_oauth)


@app.route('/', methods=['GET', 'POST'])
def root():
    method = oauth.get_method()
    if (not method):
        form = LoginForm()
        if form.validate_on_submit():
            oauth.set_method('local')
            user = models.load_user_by_email_method(form.email.data, 'local')
            if user and user.password == form.password.data:
                login_user(user, True)
                return redirect(url_for('index'))
        return render_template('login.html',
                           title='Sign In',
                           providers=app.config['OAUTH_PROVIDERS'],
                           form=form)
    else:
        user = oauth.get_user_info(method)
        if user['id'] is not None:
            us = models.load_user_by_email_method(user['email'], method)
            if (us is None):
                user2 = User(nickname=user['name'], email=user['email'], method=method)
                db.session.add(user2)
                db.session.commit()
            else:
                user2 = us
            login_user(user2, True)


    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    #news = models.News.query.paginate(page, POSTS_PER_PAGE, False).items
    #news = db.session.query(models.News.title, models.News.desc, models.News.image, models.News.url, db.func.sum(models.News.rank).label("rank")).group_by(models.News.id, models.News.title, models.News.desc, models.News.image, models.News.url).all()
    news = db.session.query(models.News.title, models.News.desc,models.News.image, models.News.url,models.News.tags, db.func.sum(models.News.rank).label("rank")).filter(
        models.News.title!=None).group_by(models.News.title, models.News.desc, models.News.image
, models.News.url,models.News.tags).order_by(db.func.sum(models.News.rank).desc()).yield_per(POSTS_PER_PAGE).all()
    #ln = len(models.News.query.all())
    ln = len(news)
    has_more = (page * POSTS_PER_PAGE) < ln
    has_less = page >1
    prev_num = page -1
    next_num = page +1
    end = (page * POSTS_PER_PAGE)
    init = end - POSTS_PER_PAGE
    return render_template('index.html',
                           title='Home',
                           form=form,
                           news=news[init:end],
                           has_more=has_more,
                           has_less = has_less,
                           next_num = next_num,
                           prev_num = prev_num)
@app.route('/logout')
@app.route('/logout/')
def logout():
    if current_user:
        logout_user()
    oauth.set_method(None)
    return redirect(url_for('root'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        oauth.set_method('local')
        user = User(nickname=form.name.data, email=form.email.data, method='local', password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, True)
        return redirect(url_for('index'))
    return render_template('signup.html',
                           title='Sign Up',
                           form=form)





@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)


@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('editProfile.html', form=form)


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

