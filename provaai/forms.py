# -*- coding: utf-8 -*-
from wtforms import BooleanField, TextField, TextAreaField, PasswordField, validators, SelectField
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

from . import images_manager

class LoginForm(Form):
    email = TextField(u'email')
    password = PasswordField(u'senha')


from .models import Image
class ProfilePhotoField(FileField):
    def __init__(self,*args,**kwargs):
        super(ProfilePhotoField,self).__init__(*args,**kwargs)

    def populate_obj(self,obj,name):
        if self.has_file():
            filename = images_manager.save(self.data)
            img = Image.create(
                filename=filename,
                url=images_manager.url(filename)
            )
            setattr(obj, name, img)

class RegistrationForm(Form):
    name = TextField(u'Nome', [validators.Length(max=30),validators.Required()])
    last_name = TextField(u'Sobrenome', [validators.Required()])
    age = TextField(u'Idade', [validators.Required()])
    email = TextField(u'Email', [
        validators.Email(message='Invalid email address.'),
        validators.EqualTo(u'email_confirm', message='Emails must match')
    ])
    email_confirm = TextField(u'Repita o email')
    password = PasswordField(u'Senha', [
        validators.Required(),
        validators.EqualTo(u'confirm', message='Passwords must match')
    ])
    confirm = PasswordField(u'Repita a senha')
    address = TextField(u'Endereço')
    city = TextField(u'Cidade / Estado')
    zip_code = TextField(u'CEP')
    accept_news = BooleanField(u'Me manter informado sobre todas as informações e notícias do Prova Aí')
    accept_tos = BooleanField(u'Eu li e concordo com os termos de uso e a política de privacidade', [validators.Required()])

    profile_photo = ProfilePhotoField(u'Foto de perfil', validators=[
        FileAllowed(images_manager, u'Imagem Inválida')
    ])

class PhotoForm(Form):
    name = TextField(u'Nome', [validators.Required()])
    photo = FileField(u'Foto', validators=[
        FileRequired(),
        FileAllowed(images_manager, u'Imagem Inválida')
    ])
    description = TextField(u'Descrição')

from .models import Category
class AddClothForm(Form):
    #store = 
    name = TextField(u'Título curto da peça', [validators.Required()])
    color = TextField(u'Cor da peça')
    brand = TextField(u'Marca da peça')
    price = TextField(u'Preço')
    fullname = TextField(u'Título completo da peça')
    description = TextField(u'Descrição da peça')
    photo = FileField(u'Imagem da peça', validators=[
        FileRequired(),
        FileAllowed(images_manager, u'Imagem Inválida')
    ])
    category = SelectField(u'Categoria',coerce=int)
    subcategory = SelectField(u'SubCategoria',coerce=int)
    sex = SelectField(u'Sexo', choices=[('M','Masculino'),('F','Feminino')])
    
    def __init__(self, *args, **kwargs):
        super(AddClothForm, self).__init__(*args,**kwargs)

        parents = [ c for c in Category.select() if c.parent is None]
        self.category.choices = [ (c.id, c.name) for c in parents ] 
        if len(self.category.choices) > 0:
            self.set_subcategory(parents[0].id)
        else:
            self.subcategory.choices = []


    def set_subcategory(self, category_id):
        parent = Category.get(Category.id == category_id)
        self.subcategory.choices = [ (c.id, c.name) for c in Category.select().where(Category.parent == parent) ] 

class StoreRegistrationForm(Form):
    #Step 1
    category = TextField(u'Categoria')
    name = TextField(u'Nome da Loja')
    address = TextField(u'Endereço')
    number = TextField(u'Número')
    extra = TextField(u'Complemento')
    state = TextField(u'Estado')
    city = TextField(u'Cidade')
    zip_code = TextField(u'CEP')
    phone = TextField(u'Telefone')
    site = TextField(u'Site')
    logo_img = FileField(u'Logotipo', validators=[
        FileAllowed(images_manager, u'Imagem Inválida')
    ])
    description = TextAreaField(u'Descrição')
    perma_link = TextField(u'suamarca')
    #Step 3

# Loja de Shopping
# Categoria
# Nome da Loja
# Shopping
# Estado Cidade
# Andar da Loja Telefone
# Site
# Logotipo
# Descrição