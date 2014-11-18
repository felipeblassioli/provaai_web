# -*- coding: utf-8 -*-
from werkzeug.utils import secure_filename

from flask import request, render_template, jsonify, redirect, url_for
from flask.ext.login import login_required, flash, login_user, logout_user, current_user,AnonymousUserMixin
from flask.ext.classy import FlaskView, route

from . import app, login_manager, images_manager, admin
from .models import *
from .forms import *

def _redirect(endpoint):
    return redirect(request.args.get("next") or url_for(endpoint))

def _render_template(*args, **kwargs):
    kwargs.update(dict(
        user = current_user,
        forms=dict(
            login=LoginForm()
        )
    ))
    return render_template(*args, **kwargs)

@login_manager.user_loader
def load_user(userid):
    user = None
    try:
        app.logger.debug("load_user id=[{}]".format(userid))
        user = User.get(User.id == userid)
    except User.DoesNotExist:
        app.logger.warning("User not found for id=[{}]".format(userid))
    return user

def authenticate(email,pwd):
    try:
        user = User.get(User.email == email)
        if user.password == pwd:
            return user
    except User.DoesNotExist:
        pass
    return None

@app.route('/', methods=['GET'], endpoint="index")
def index():
    showcase = Cloth.select()
    if current_user.is_anonymous():
        showcase=[]
        frozen=[]
        store={"logo":{"url":""}}
    else:
        store = current_user.store
        # Careful with this: (too ugly)
        action = request.args.get('action')
        if action == 'register_done':
            current_user.first_login = False
            current_user.save()
    return _render_template(
        'index.html', 
        store=store,
        showcase = showcase
    )

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        user = authenticate(form.email.data, form.password.data)
        if user == None:
            return "Login failed: User not found for email=[{}]".format(form.email.data)
        else:
            login_user(user)
            return _redirect("index")
        #return redirect(request.args.get("next") or url_for("index"))
    return _render_template("login.html", 
        form=form
    )

@app.route("/settings")
@login_required
def settings():
    return "Hello bro, "+current_user.name

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return _redirect("index")

@app.route('/register/', methods=['GET', 'POST'])
def register():
    print request.method, request.form
    form = RegistrationForm(request.form)
    print 'validate', form.validate_on_submit()
    if form.validate_on_submit():
        params = dict(
            name = form.name.data,
            last_name = form.last_name.data,
            age = form.age.data,
            email = form.email.data,
            password = form.password.data,
            address = form.address.data,
            accept_news = form.accept_news.data
        )
        usr = User.create(**params)
        Store.create(owner=usr,name="Loja Teste")
        login_user(usr)
        print jsonify(params)
        return _redirect("index")
    return _render_template('register.html', form=form)

@app.route('/setup/', methods=['GET'])
def setup():
    create_tables()
    Brand.create(name="Hollister")
    Brand.create(name="Nike")
    return "Ok"

@app.route('/upload/', methods=('GET', 'POST'))
def upload():
    form = PhotoForm()
    print "validate", form.validate_on_submit()
    if form.validate_on_submit():
        print "Success"
        print "photo", form.photo
        print form.photo.data
        print form.photo.data.filename
        filename = images_manager.save(form.photo.data)
        return filename
    else:
        print 'FAILEEEEEEEEEEEEEEEEEEEED'
        filename = None
    return _render_template('upload.html', form=form, filename=filename)

@app.route('/welcome/')
def welcome():
    return render_template('welcome.html')

class StoreView(FlaskView):
    def welcome(self):
        return render_template('store/welcome.html')
        
    @login_required
    def index(self):
        formAddCloth = AddClothForm()
        showcase = current_user.store.showcase
        return _render_template(
            'store/main.html',
            store=current_user.store,
            showcase=showcase,
            form=dict(
                add_cloth=formAddCloth
            )
        )

    @route('/register/', methods=['GET','POST'])
    def register_store(self):
        form = StoreRegistrationForm()
        if form.validate_on_submit():
            print "Success"
            return _redirect('StoreView:index')
        return _render_template(
            'store/register.html',
            form=form
        )
        
    @login_required
    @route('/add/', methods=['POST'])
    def add(self):
        form = AddClothForm()
        if form.validate_on_submit():
            print "Success"
            print "photo", form.photo
            print form.photo.data
            print form.photo.data.filename
            filename = images_manager.save(form.photo.data)
            img = Image.create(
                filename=filename,
                url=images_manager.url(filename)
            )
            cloth = Cloth.create(
                store = current_user.store,
                image = img,
                name = form.name.data,
                description = form.description.data,
                brand = Brand.select()[0],
                in_showcase=True
            )
            return _redirect('index')
        else:
            print 'FAILEEEEEEEEEEEEEEEEEEEED'
            return "OOOOOOOOK FAILED"

StoreView.register(app)

from flask.ext.admin.contrib.peewee import ModelView
for m in [User,Store,Cloth]:
    admin.add_view(ModelView(m))