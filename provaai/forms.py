# -*- coding: utf-8 -*-
from wtforms import BooleanField, TextField, TextAreaField, PasswordField, validators
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

from . import images_manager

class LoginForm(Form):
    email = TextField(u'email')
    password = PasswordField(u'senha')

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

class PhotoForm(Form):
    name = TextField(u'Nome', [validators.Required()])
    photo = FileField(u'Foto', validators=[
        FileRequired(),
        FileAllowed(images_manager, u'Imagem Inválida')
    ])
    description = TextField(u'Descrição')

class AddClothForm(Form):
    #store = 
    name = TextField(u'Título curto da peça', [validators.Required()])
    color = TextField(u'Cor da peça')
    brand = TextField(u'Marca da peça')
    price = TextField(u'Preço')
    fullname = TextField(u'Descrição da peça')
    description = TextField(u'Descrição da peça')
    photo = FileField(u'Imagem da peça', validators=[
        FileRequired(),
        FileAllowed(images_manager, u'Imagem Inválida')
    ])
    category = TextField(u'Categoria')
    sex = TextField(u'Sexo')
    favorite = BooleanField(u'Peça favorita')
    

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