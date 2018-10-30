from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "Secreto"

### BANCO  DE DADOS
def obter_conexao():
    conexao = sqlite3.connect('boletim')
    return conexao

### LISTAR VEICULOS ###
@app.route('/')
def index():
    conexao = obter_conexao()
    cursor = conexao.execute('SELECT * FROM Disciplina;')
    ##cursor2 = conexao.execute("insert into Veiculo ('ka', '2018', 'preto');")
    disciplina = cursor.fetchall()
    return render_template('index.html', disciplina=disciplina)

@app.route('/NovaDisciplina')
def nova_disciplina():
    return render_template('nova_disciplina.html', disc = [], editando = False, cod=0)


@app.route('/EditarDisciplina/<int:cod>')
def editar_disciplina(cod):
    conexao = obter_conexao()
    cursor = conexao.execute('SELECT * FROM disciplina where cod = ?;', [cod])
    disciplina = cursor.fetchone()

    return render_template('novo_veiculo.html', disc = disciplina ,editando = True)


@app.route('/SalvarDisciplina', methods=['POST'])
def salvar_disciplina():
    # obter dados do formulario

    editando = request.form['editando']
    cod = request.form['cod']
    nome = request.form['nome']
    nota1 = request.form['nota1']
    if nota1: nota1 = float(nota1)
    nota2 = float(request.form['nota2'])
    if nota2: nota2 = float(nota2)
    nota3 = float(request.form['nota3'])
    if nota3: nota3 = float(nota3)
    nota4 = float(request.form['nota4'])
    if nota4: nota4 = float(nota4)
    situacao = request.form['situacao']

    #conectar e enviar pro banco de dados
    conexao = obter_conexao()

    if editando == "True":
        conexao.execute('UPDATE Disciplina SET nome = ?, nota1 = ?, nota2 = ?, nota3 = ?, nota4 = ?, situacao = ? where cod = ?;', [nome, nota1, nota2, nota3, nota4, situacao, cod])
    else:
        conexao.execute('Insert INTO Disciplina (nome, nota1, nota2, nota3, nota4, situacao) values (?,?,?,?,?,?)', [nome, nota1, nota2, nota3, nota4, situacao])
    conexao.commit()

    return redirect('/')


# @app.route("/")
# def hello():
#     return "Hello World!"