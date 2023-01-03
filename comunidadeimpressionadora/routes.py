from flask import render_template, url_for, request, flash, redirect, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditar, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email = form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados)
            flash("Login feito com sucesso", "alert-success")
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:    
                return redirect(url_for('home'))
        else:
            flash("Falha no login. E-mail ou/e senha incorretos.", "alert-danger")

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crip = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crip)
        database.session.add(usuario)
        database.session.commit()
        flash("Conta criada com sucesso", "alert-success")
        return redirect(url_for('home'))    
            
    return render_template('login.html', form_login = form_login, form_criarconta = form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto=foto)

@app.route('/post/criar', methods=["GET", "POST"])
@login_required
def criar_post():
    form_post = FormCriarPost()
    if form_post.validate_on_submit():
        post = Post(titulo=form_post.titulo.data, corpo=form_post.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash("Post criado com sucesso.", "alert-success")
        return redirect(url_for('home'))
    return render_template('criarpost.html', form_post=form_post)

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    tamanho = (400,400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

    

@app.route('/perfil/editar', methods=["GET", "POST"])
@login_required
def editar():
    form_editar = FormEditar()
    if form_editar.validate_on_submit():
        current_user.username = form_editar.username.data
        current_user.email = form_editar.email.data
        if form_editar.foto_perfil.data:
            imagem = salvar_imagem(form_editar.foto_perfil.data)
            current_user.foto_perfil = imagem
        current_user.cursos = atualizar_cursos(form_editar)
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))

    foto = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto=foto, form_editar=form_editar)

@app.route('/post/<post_id>', methods=["GET", "POST"] )
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash("Post atualizado com sucesso", 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=["GET", "POST"])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash("Post excluido com sucesso", 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
