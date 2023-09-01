from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy, Pagination
import urllib.request, json

app = Flask(__name__)

# Defina a chave secreta aqui
app.secret_key = 'mysecretkey123'

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'
db = SQLAlchemy(app)

frutas = []
registros = []


class Cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(120))
    ch = db.Column(db.Integer)

    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch


@app.route('/', methods=['GET', 'POST'])
def principal():
    """
    frutas = ['Morango', 'Banana', 'Abacaxi',
              'Laranja', 'Manga', 'Maça', 'Melão',
              'Jambo', 'Tangerina']
    """

    if request.method == 'POST':
        if request.form.get('fruta'):
            frutas.append(request.form.get('fruta'))

    return render_template("index.html", frutas=frutas)


@app.route('/sobre', methods=['GET', 'POST'])
def sobre():
    """
    notas = {"Alan": 6.5, "Carlos": 5.5, "Marcos": 8.9,
             "Camila": 7.8, "Roberto": 4.9, "Alexia": 7.2}
    """

    if request.method == 'POST':
        if request.form.get('aluno') and request.form.get('nota'):
            registros.append({"aluno": request.form.get('aluno'),
                              "nota": request.form.get('nota')})

    return render_template("sobre.html", registros=registros)


@app.route('/filmes/<propriedade>')
def filmes(propriedade):

    if propriedade == 'populares':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=f99dbb8745b326c616475a6b60bad2a0"
    elif propriedade == 'kids':
        url = "https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=f99dbb8745b326c616475a6b60bad2a0"
    elif propriedade == '2010':
        url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=f99dbb8745b326c616475a6b60bad2a0"
    elif propriedade == 'drama':
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=f99dbb8745b326c616475a6b60bad2a0"
    elif propriedade == 'tom_cruise':
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=878&with_cast=500&sort_by=vote_average.desc&api_key=f99dbb8745b326c616475a6b60bad2a0"

    resposta = urllib.request.urlopen(url)

    dados = resposta.read()

    jsondata = json.loads(dados)

    return render_template("filmes.html", filmes=jsondata['results'])


@app.route('/cursos')
def lista_cursos():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    todos_cursos = Cursos.query.paginate(page=page, per_page=per_page)

    # return render_template('cursos.html', cursos=Cursos.query.all())
    return render_template('cursos.html', cursos=todos_cursos)


@app.route('/cria_curso', methods=['GET', 'POST'])
def cria_curso():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    ch = request.form.get('ch')

    if request.method == 'POST':
        if not nome or not descricao or not ch:
            flash("Preecha todos os campos do formulário", "error")
        else:
            curso = Cursos(nome, descricao, ch)

            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('lista_cursos'))

    return render_template('novo_curso.html')


@app.route('/<int:id>/atualiza_curso', methods=['GET', 'POST'])
def atualiza_curso(id):
    curso = Cursos.query.filter_by(id=id).first()

    if request.method == 'POST':
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        ch = request.form["ch"]

        Cursos.query.filter_by(id=id).update({
            "nome": nome,
            "descricao": descricao,
            "ch": ch
        })
        db.session.commit()

        return redirect(url_for('lista_cursos'))

    return render_template('atualiza_curso.html', curso=curso)


@app.route('/<int:id>/remove_curso')
def remove_curso(id):
    curso = Cursos.query.filter_by(id=id).first()

    db.session.delete(curso)
    db.session.commit()

    return redirect(url_for('lista_cursos'))


if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas do banco de dados
        db.create_all()

    # Executa a aplicação
    app.run(host='0.0.0.0', port=8000, debug=True)
