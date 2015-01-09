# -*- coding: utf-8 -*-
from werkzeug.utils import secure_filename

from flask import request, render_template, jsonify, redirect, url_for
from flask.ext.login import login_required, flash, login_user, logout_user, current_user,AnonymousUserMixin
from flask.ext.classy import FlaskView, route

from . import app, login_manager, images_manager, admin
from .models import *
from .forms import *

def _redirect(endpoint, *args, **kwargs):
    url_params = kwargs.pop('url_params', '')
    return redirect(request.args.get("next") or url_for(endpoint, *args, **kwargs)+url_params)

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

from flask import abort
@app.route('/<path:path>')
def catch_all(path):
    try:
        store = Store.get(Store.perma_link == path.lower())
        # Flask-classy`s make_proxy method uses request.view_args and accepts no params
        request.view_args.pop('path')
        request.view_args['id'] = store.id
        return app.view_functions['StoreView:index']()
    except Store.DoesNotExist:
        pass
    return abort(404)

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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return _redirect("index")

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.profile_photo.has_file():
            filename = images_manager.save(form.profile_photo.data)
            img = Image.create(
                filename=filename,
                url=images_manager.url(filename)
            )
        else:
            img = current_user.profile_photo
        params = dict(
            name = form.name.data,
            last_name = form.last_name.data,
            age = form.age.data,
            email = form.email.data,
            password = form.password.data,
            address = form.address.data,
            accept_news = form.accept_news.data,
            profile_photo = img
        )
        usr = User.create(**params)
        #Store.create(owner=usr,name="Loja Teste")
        login_user(usr)
        return _redirect("index")
    return _render_template('user/register.html', form=form)

@login_required
@app.route('/store/register/', methods=['GET','POST'], endpoint='register_store')
def register_store():
    form = StoreRegistrationForm()
    if form.validate_on_submit():
        print "Success", current_user, type(current_user)
        addr = form.address.data +', '+form.number.data+', '+form.state.data+', '+form.city.data
        #print form.logo_img.data
        #print form.logo_img.data.filename
        print 'files', request.files
        if form.logo_img.has_file:
            print form.logo_img
            print form.logo_img.data, type(form.logo_img.data)
            filename = images_manager.save(form.logo_img.data)
            img = Image.create(
                filename=filename,
                url=images_manager.url(filename)
            )
        else:
            img = None
        params = dict(
            owner = User.get(User.id == current_user.id),
            name = form.name.data,
            perma_link = form.perma_link.data,
            address = addr,
            zip_code = form.zip_code.data,
            site = form.site.data,
            logo = img
        )
        print params
        s = Store.create(**params)
        return _redirect('StoreView:index', id=s.id)
    return _render_template(
        'store/register.html',
        form=form
    )


@app.route('/setup/', methods=['GET'])
def setup():
    create_tables()
    Brand.create(name="Hollister")
    Brand.create(name="Nike")

    category_data = {
        u'Calçado': [u'Botas',u'Chinelos',u'Rasteiras',u'Sandalias',u'Sapatenis',u'Sapatilhas','Sapato Casual','Sapato Social',u'Sapatos',u'Tenis'],
        u'Esporte': [u'Acessorios','Calçados',u'Equipamentos',u'Shorts',u'Camisetas'],
        u'Bolsas e Acessorios': [u'Acessorios para cabelo',u'Bijuterias',u'Bolsas',u'Bones e chapeus',u'Carteiras',u'Cintos',u'Mochilas e malas',u'Necessaires',u'Oculos',u'Relogios'],
        u'Casual': [u'Shorts',u'Camisetas',u'Calças Jeans',u'Camisetas',u'Jaquetas',u'Minissaia',u'Moletons',u'Polos',u'Saias',u'Vestidos']
    }
    for category, subcategories in category_data.items():
        c = Category.create(name=category)
        for s in subcategories:
            Category.create(name=s,parent=c.id)
    return "Ok"

class UserView(FlaskView):

    @login_required
    @route('/settings/', methods=['GET','POST'])
    def settings(self):
        form = RegistrationForm(obj=current_user)
        form.accept_tos.validators = []
        form.password.validators = []
        if form.validate_on_submit():
            form.populate_obj(current_user)
            current_user.save()
        return _render_template('user/settings.html',form=form)

    @login_required
    def add(self):
        pass

    @login_required
    def closet(self):
        pass

    @login_required
    def change_password(self):
        pass

class StoreView(FlaskView):
    route_base = '/store/<int:id>/'

    def welcome(self):
        return render_template('store/welcome.html')
    
    def index(self,id):
        formAddCloth = AddClothForm()
        current_store = Store.get(Store.id == id)

        return _render_template(
            'store/index.html',
            store=current_store,
            showcase=current_store.showcase,
            form=dict(
                add_cloth=formAddCloth
            )
        )

    @login_required
    def edit(self, id):
        current_store = Store.get(Store.id == id)
        return _render_template(
            'store/edit.html',
            store=current_store,
            form=dict(
                add_cloth=AddClothForm()
            )
        )

    @login_required
    @route('/settings/', methods=['GET','POST'])
    def settings(self, id):
        store = current_user.store
        form = StoreRegistrationForm(obj=store)
        if form.validate_on_submit():
            form.populate_obj(store)
            store.save()
            #_redirect('StoreView:settings', id=id)
            #render_response('store/settings.html', form=form)
        return _render_template('store/settings.html', store=store, form=form)
        
    @login_required
    @route('/add/', methods=['POST'])
    def add(self,id):
        store = Store.get(Store.id == id)
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
                store = store,
                image = img,
                name = form.name.data,
                fullname = form.fullname.data,
                description = form.description.data,
                color = form.color.data,
                price = form.price.data,
                sex = form.sex.data,
                brand = Brand.select()[0],
                in_showcase=True
            )
            return _redirect('StoreView:edit',id=id)
        else:
            print 'FAILEEEEEEEEEEEEEEEEEEEED'
            current_store = current_store = Store.get(Store.id == id)
            return _render_template(
                'store/edit.html',
                store=current_store,
                form=dict(
                    add_cloth=form
                ),
                auto_show_dialog=True
            )

StoreView.register(app)
UserView.register(app)

from flask.ext.admin.contrib.peewee import ModelView
for m in [User,Store,Cloth,Category]:
    admin.add_view(ModelView(m))

print app.url_map