from flask import Flask, render_template, request

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
