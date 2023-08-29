from flask import Flask, render_template, request
import urllib.request, json

app = Flask(__name__)

frutas = []
registros = []


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
