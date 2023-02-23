# Criar Repositório Web-SVN

Este projeto consiste em uma página web que permite criar repositórios no servidor SVN, verificando se a pasta já existe e adicionando as permissões de acesso corretas.

## Funcionamento

Ao acessar a página inicial, o usuário preenche o formulário com o nome da pasta e escolhe o produto ao qual o repositório está relacionado. Em seguida, o aplicativo verifica se a pasta já existe no servidor. Se a pasta não existe, o aplicativo cria a pasta e adiciona as permissões de acesso corretas no arquivo de configuração `dav_svn.authz`. 

Caso a pasta já exista, o aplicativo exibe uma mensagem informando que a pasta já existe e não faz nenhuma alteração.

## Pré-requisitos

Para executar o aplicativo, é necessário ter as seguintes bibliotecas instaladas:

- Flask

Para instalar as bibliotecas necessárias, execute o seguinte comando:

`pip install -r requirements.txt`


## Como executar

Para executar o aplicativo, basta rodar o arquivo `app.py` com o comando `sudo python app.py` e acessar a URL `http://localhost/criarepositorio` no navegador:


## Autor

Arthur Nunes Catarina - Analista de Infraestrutura

