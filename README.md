# PROJETO ISMART

Este é um projeto desenvolvido por, Gustavo Valente, João Pedro Miguel, Matheus Vicco, Bruno Oberhuber e Raphael Lafer, estudantes de Ciências da Computação no Insper. O projeto foi desenvolvido em Python, utilizando um framework chamado Django, além de HTML e CSS para a interface visual.

## Objetivos

O objetivo principal do projeto é otimizar o processo de atendimento aos candidatos do Ismart, reduzindo o tempo dedicado pela equipe ao atendimento individualizado, sem perder a personalização necessária para atender um público de variados níveis de conhecimento tecnológico.

Além disso, buscamos aumentar a efetividade das respostas para as dúvidas dos usuários utilizando uma IA (Inteligência Artificial), no formato de um chat bot, que resolve rapidamente as dúvidas mais frequentes dos candidatos.

## Como executar o projeto

Para executar o projeto é necessário ter o Python mais recente instalado, e executar alguns comandos, sendo eles:

Comando para Instalar todas as bibliotecas utilizadas no projeto, listadas no arquivo requirements.txt

```bash
pip install -r requirements.txt
```

Comandos para fazer as migrações necessárias para rodar o projeto.

```bash
python manage.py makemigrations
python manage.py migrate
```

### Colaborador

Para cadastrar um novo colaborador no site será preciso criá-lo utilizando o próprio terminal com o comando:

```bash
python manage.py createsuperuser
```

Ele irá pedir um nome de usuário, email e senha, e após preencher esses quesitos, um usuário STAFF será criado, que poderá acessar as páginas dos colaboradores.

**IMPORTANTE**

É importante que os canditados não tenham acesso a esse comando, pois podem acessar páginas do site que são apenas para colaboradores, como a página para tirar dúvidas de usuários.

## Rodando o Chat Bot no site

Para executar o programa do chat bot, é preciso abrir outro servidor separado do servidor principal do site, para isso, abra a pasta chatbot em outra janela do seu editor de códigos e execute o seguinte comando:

```bash
streamlit run streamlit_app.py
```

## Conversas pelo Whatsapp (Twillio)

Para que as conversas do seu Whatsapp aparecam para você na plataforma de troca de mensagens, nós utilizamos um framework chamado Twillio, que permite essa função. Ao utilizar o Twillio é preciso [criar uma conta](https://login.twilio.com/u/signup?state=hKFo2SBieENlRUZEYmVKdEs4QzZDN09OOHR5clJidmdkMGV6T6Fur3VuaXZlcnNhbC1sb2dpbqN0aWTZIGJJVTFpbEtDYlE2c2NQZGJsUDlfVmh4V3FyM0o0UHZQo2NpZNkgTW05M1lTTDVSclpmNzdobUlKZFI3QktZYjZPOXV1cks) no site.

Já cadastrado, selecione a opção **Develop** no canto superior esquerdo da página, depois **Messaging**, **Try It Out**, e **Send a Whatsapp Message**. Na opção Sandbox, você poderá ver o número que será utilizado para os colaboradores mandarem mensagens pela plataforma. Já na opção sandbox settings, você deve colocar a url do servidor onde deseja receber as requisições. Ex: https://sua_url/receberzap/

**IMPORTANTE**

Na versão Gratuita do Twillio é preciso que o usuário mande a seguinte mensagem para o número dos colaboradores, antes de mandar sua dúvida, para que o programa funcione devidamente:

```bash
join century-anyway
```

Agora o programa deve estar devidamente configurado e pronto para uso.