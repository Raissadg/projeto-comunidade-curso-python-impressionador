from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirmacao = PasswordField("Confirmação de senha", validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario =  Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.")


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    lembrar_dados = BooleanField("Lembrar dados")
    botao_submit_login = SubmitField("Fazer Login")

class FormEditar(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    foto_perfil = FileField("Atualizar foto de perfil", validators=[FileAllowed(['png','jpg'])])
    curso_vba = BooleanField("VBA Impressionador")
    curso_excel = BooleanField("Excel Impressionador")
    curso_powerbi = BooleanField("Power BI Impressionador")
    curso_python = BooleanField("Python Impressionador")
    curso_ppt = BooleanField("Apresentações Impressionadoras")
    curso_sql = BooleanField("SQL Impressionador")
    botao_submit_confirmar = SubmitField("Confirmar Edição")

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario =  Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("Usuário já existente com esse e-mail. Cadastre outro e-mail.")

class FormCriarPost(FlaskForm):
    titulo = StringField("Título do Post", validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField("Escreva seu Post Aqui", validators=[DataRequired()])
    botao_submit_post = SubmitField("Criar Post")