from flask import Flask, render_template, request, session, flash
from werkzeug.utils import redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "Victory"


### BANCO  DE DADOS
def obter_conexao():
    conexao = sqlite3.connect('escola.banco')
    return conexao


### LISTAR VEICULOS ###
@app.route('/veiculo')
def veiculos():
    conexao = obter_conexao()
    cursor = conexao.execute('SELECT * FROM Veiculo;')
    ##cursor2 = conexao.execute("insert into Veiculo ('ka', '2018', 'preto');")
    carros = cursor.fetchall()
    return render_template('veiculos.html', carros=carros)


### INSERIR VEICULOS ###
@app.route('/NovoVeiculo')
def novo_veiculo():
    return render_template('novo_veiculo.html', carro = [], editando= False)


## REMOVER VEICULOS
@app.route('/RemoverVeiculo/<string:nome>')
def remover_veiculo(nome):
    conexao = obter_conexao()
    conexao.execute('DELETE From veiculo where nome = ? ', [nome])
    conexao.commit()
    return redirect('/veiculo')


## EDITAR VEICULOS
@app.route('/EditarVeiculo/<string:nome>')
def editar_veiculo(nome):
    conexao = obter_conexao()
    cursor = conexao.execute('SELECT * FROM Veiculo where nome = ?;', [nome])
    carros = cursor.fetchone()

    return render_template('novo_veiculo.html', carro = carros, editando = True)


@app.route('/SalvarVeiculo', methods=['POST'])
def salvar_veiculo():
    # obter dados do formulario

    editando = request.form['editando']
    nome = request.form['nome_veiculo']
    ano = request.form['ano_veiculo']
    cor = request.form['cor_veiculo']

    #conectar e enviar pro banco de dados
    conexao = obter_conexao()

    if editando == "True":
        conexao.execute('UPDATE Veiculo SET nome = ?, ano = ?, cor = ?;', [nome, ano, cor])
    else:
        conexao.execute('Insert INTO Veiculo values (?,?,?)', [nome, ano, cor])
    conexao.commit()

    return redirect('/veiculo')


@app.route('/')
def pagina_inicial():
    return 'Pagina Inicial'


@app.route('/home/<int:numero>')
def index(numero):
    dobro = numero * 2
    return render_template('index.html', valor=dobro)


@app.route('/informacao/<string:autor>')
def informacao(autor):
    return render_template('informacao.html', autor=autor)


@app.route('/profissionais')
def profissionais():
    return render_template('profissionais.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('form_login.html')
    elif request.method == 'POST':
        usuario = request.form['user']
        senha = request.form['pass']

        if usuario == 'Philipe' and senha == '123':
            session['username'] = usuario
            flash('Login realizado com sucesso!')
            return redirect('/home/10')
        else:
            flash('Usuario e/ou Senha incorretos.!')
            return redirect('/login')


@app.route('/logout')
def logout():
    # remove the username form te session
    session.pop('username', None)
    return redirect('/home/1')


@app.route('/nos')
def quem_somos():
    return render_template('quem_somos.html')


if __name__ == '__main__':
    app.run()
