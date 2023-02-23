# This Python file uses the following encoding: utf-8
import subprocess
import os
from flask import Flask, render_template, request, redirect
from werkzeug.middleware.dispatcher import DispatcherMiddleware


#Configurando flag para rodar local/production
local = True

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/execute', methods=['POST'])
def execute():
    team = request.form['team']
    tipo = request.form['tipo']
    cod_produto = request.form['cod_produto']
    nome_produto = request.form['nome_produto']
    
    #Define as variáveis Release e Source
    Release = "Release"
    Source = "Source"
    # Concatena os valores do campo para formar o nome do repositório
    nome_pasta = cod_produto + '_' + nome_produto
    
    #Verifica se o diretório já existe
    if os.path.isdir(nome_pasta):
        mensagem =f"Repositório {nome_pasta} já existe"
        return render_template('resultado.html', mensagem=mensagem)
    else:
        #Executa os comandos para criação do repositorio
        os.chdir('/mnt/svn-ng')
        os.makedirs(nome_pasta)
        result_svncreate = subprocess.run(["svnadmin create /mnt/svn-ng/" + nome_pasta], stderr=subprocess.PIPE, shell=True, stdout=subprocess.PIPE)
        stdout = result_svncreate.stdout.decode('utf-8')
        stderr = result_svncreate.stderr.decode('utf-8')
        if result_svncreate.returncode != 0:
            mensagem = f"Erro ao executar svnadmin create: {result_svncreate.stderr.decode()}"
            return render_template('resultado.html', mensagem=mensagem)
        #Cria o repositório se for release
        if (tipo == 'Release'):
            result_release = subprocess.run(["svn mkdir file:///mnt/svn-ng/" + nome_pasta + "/" + Release + " -m 'Criado pasta Release'"], stderr=subprocess.PIPE, shell=True, stdout=subprocess.PIPE)
            stdout = result_release.stdout.decode('utf-8')
            stderr = result_release.stderr.decode('utf-8')
            if result_release.returncode != 0:
                mensagem = f"Erro ao executar svn mkdir: {result_release.stderr.decode()}"
                return render_template('resultado.html', mensagem=mensagem)
        #Cria o repositório se for source
        else:
            result_source = subprocess.run(["svn mkdir file:///mnt/svn-ng/" + nome_pasta + "/" + Source + " -m 'Criado pasta Source'"], stderr=subprocess.PIPE, shell=True, stdout=subprocess.PIPE)
            stdout = result_source.stdout.decode('utf-8')
            stderr = result_source.stderr.decode('utf-8')
            if result_source.returncode != 0:
                mensagem = f"Erro ao executar svn mkdir: {result_source.stderr.decode()}"
                return render_template('resultado.html', mensagem=mensagem)
        #Altera as permissões    
        result_chgrp = subprocess.run(["chgrp -R svnusers /mnt/svn-ng"], stderr=subprocess.PIPE, shell=True, stdout=subprocess.PIPE)
        stdout = result_chgrp.stdout.decode('utf-8')
        stderr = result_chgrp.stdout.decode('utf-8')
        if result_chgrp.returncode != 0:
            mensagem = f"Erro ao executar chgrp: {result_chgrp.stderr.decode()}"
            return render_template('resultado.html', mensagem=mensagem)

        result_chmod = subprocess.run(["chmod -R g+w /mnt/svn-ng"], stderr=subprocess.PIPE, shell=True, stdout=subprocess.PIPE)
        stdout = result_chmod.stdout.decode('utf-8')
        stderr = result_chmod.stdout.decode('utf-8')
        if result_chmod.returncode != 0:
            mensagem = f"Erro ao executar chmod: {result_chmod.stderr.decode()}"
            return render_template('resultado.html', mensagem=mensagem)
        #Adiciona o acesso das equipes no dav_svn.authz
        if (team == "cabinet"):
            with open("/etc/apache2/dav_svn.authz", 'a') as file:
                file.write('\n\n########' + nome_pasta + '#########\n')
                file.write('[' + nome_pasta + ':/]\n')
                file.write('@ti = rw\n')
                file.write('@art-cabinet = rw\n')
                file.write('@dev-cabinet = rw\n')
        #Reinicia o apache
            subprocess.run(["systemctl", "restart", "apache2"])
        
        if (team == 'tablet'):
            with open("/etc/apache2/dav_svn.authz", 'a') as file:
                file.write('\n\n########' + nome_pasta + '#########\n')
                file.write('[' + nome_pasta + ':/]\n')
                file.write('@ti = rw\n')
                file.write('@art-tablet = rw\n')
                file.write('@dev-tablet = rw\n')
        #Reinicia o apache
            subprocess.run(["systemctl", "restart", "apache2"])
        mensagem =f"Repositório {nome_pasta}/{tipo} criado com sucesso"
    return render_template('resultado.html', mensagem=mensagem)

if __name__ == "__main__":
    if local == False:
        app = DispatcherMiddleware(app, {'/criarepositorio': app})
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 8080, app)
    else:
        app.run(debug=True, host='0.0.0.0', port=8080, threaded=True, use_reloader=True)
