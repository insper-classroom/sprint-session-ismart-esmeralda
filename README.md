<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->






<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="atendimento\static\atendimento\img\LOGO-ismart.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Plataforma de atendimento ao candidato ISMART</h3>

  <p align="center">
    Centralização do serviço de atendimento ao cliente em uma única plataforma.
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    
  </p>
</div>







<!-- ABOUT THE PROJECT -->
## Sobre a plataforma

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Nosso projeto é focado na otimização do atendimento aos candidatos do Ismart. Nosso objetivo é reduzir o tempo de atendimento individualizado, mantendo a personalização necessária para atender um público com variados níveis de conhecimento tecnológico. 

### Funcionalidades:
* **Interface Unificada**: Desenvolvemos uma plataforma em que um colaborador pode receber e responder dúvidas provenientes de email e WhatsApp em uma única interface.
  
* **Chatbot Personalizado**: Implementamos um chatbot com conhecimentos sobre o processo seletivo do Ismart, disponível no ambiente web do cliente e no WhatsApp da Ismart. O cliente pode optar falar com um atendente real se a sua dúvida não for resolvida.
* **Classificação Automática de Dúvidas**: Para evitar questionários sobre o assunto da dúvida para o cliente, desenvolvendo uma rede neural que classifica textos vetorizados para determinar o assunto da dúvida tratada pelo colaborador após o atendimento. Isso permite uma análise mais precisa sobre atendimentos passados.


<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>



### Construído com:



* [![Django][Django]][Django-url]
* [![Openai][Openai]][Openai-url]
* [![Tensorflow][Tensorflow]][Tensorflow-url]
* [![Keras][Keras]][Keras-url]
* [![Langchain][Langchain]][Langchain-url]
* [![Streamlit][Streamlit]][Streamlit-url]
* [![Twilio][Twilio]][Twilio-url]


<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Para rodar o projeto de forma local em seu computador, siga os seguintes passos

### Pré-requisitos

Para rodar o projeto, é necessário ter a versão mais recente do Python instalada em sua máquina, assim como os requerimentos do projeto. Para instalar os requerimentos:

Clone o repositório
   ```sh
   git clone https://github.com/insper-classroom/sprint-session-ismart-esmeralda
   ```

  Instale os requerimentos
```sh
    pip install -r requirements.txt
  ```

### Instalação 

1. Crie suas chaves secretas do Twilio e da OpenAI.

2. Crie uma pasta no diretório do projeto chamada ".env" 

3. Dentro da pasta `.env`, coloque as suas chaves secretas
```js
    OPENAI_API_KEY = <ENTER YOUR API KEY>
    TWILIO_SID = <ENTER YOUR TWILIO SID>
    TWILIO_AUTH = <ENTER YOUR TWILIO AUTH>
```
### Iniciando o chatbot

Para executar o chatbot, é necessário iniciar um servidor separado do servidor principal do site. Siga os passos abaixo:

1. Abra a pasta ``chatbot`` em uma nova janela do seu editor de código.
2. No terminal integrado do seu editor de código, execute o seguinte comando:
```sh
    streamlit run streamlit_app.py
```
### Iniciando o servidor

Para iniciar o servidor da aplicação, execute o seguinte comando no terminal integrado da aplicação principal:

```sh
    python manage.py runserver
```
### Utilizando a aplicação

Para criar um usuário com permissões de colaborador, execute no terminal o comando:

```sh
    python manage.py createsuperuser
```

E forneça as credenciais desejadas para esse usuário. Esse usuário criado terá todas as permissões de colaborador dentro do sistema.



<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>



<!-- USAGE EXAMPLES -->
## Inforamções Importantes

* Na versão Gratuita do Twillio é preciso que o usuário mande uma mensagem pré-definida para o número do colaborador antes de enviar qualquer dúvida. Essa mensagem é gerada aleatoriamente de conta para conta, e é uma limitação da versão gratuita do Twilio. No nosso caso, antes de mandar algo, o usuário deve mandar a seguinte mensagem para o número:
```bash
join century-anyway
```
* Nossa aplicação utiliza dois servidores. Para permitir que o Twilio envie requisições quando o número recebe uma mensagem, é necessário que os servidores estejam acessíveis externamente. Como servidores locais não podem receber requisições externas, utilizamos um sistema de encaminhamento de porta (port forwarding) para expor o servidor local e permitir que ele receba requisições do Twilio.



<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>



<!-- ROADMAP -->
## Próximos passos

- [ ] Adicionar funcionalidades ao chatbot
- [ ] Integrar outras plataformas, como Instagram à plataforma do colaborador
- [ ] Sugerir respostas rápidas para o colaborador, por meio de uma IA, que aprende por meio do estilo de escrita e resposta de cada colaborador.



<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>



<!-- CONTRIBUTING
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- LICENSE -->
<!-- ## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- CONTACT -->
## Contato

Gustavo Victor Valente Braga e Souza - [LinkedIn](https://www.linkedin.com/in/gustavo-valente-4b865824a/) - gustavovvbs@al.insper.edu.br

João Pedro Miguel - [LinkedIn](https://www.linkedin.com/in/jo%C3%A3o-pedro-a789b42b7/)

Bruno Oberhuber - [LinkedIn](https://www.linkedin.com/in/bruno-oberhuber/)

Raphael Lafer - [LinkedIn](https://www.linkedin.com/in/raphael-lafer-637b5b2bb/)

Matheus Vicco - [LinkedIn](https://www.linkedin.com/in/matheus-vicco-29bb24283/)


<p align="right">(<a href="#readme-top">Voltar para o topo</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: atendimento\static\atendimento\img\printplataforma.png
[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Openai]: https://img.shields.io/badge/openai-000000?style=for-the-badge&logo=openai&logoColor=white
[Openai-url]: https://openai.com/
[Tensorflow]: https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white
[Tensorflow-url]: https://www.tensorflow.org/?hl=pt-br
[Keras]: https://img.shields.io/badge/Keras%20-%23D00000.svg?&style=for-the-badge&logo=Keras&logoColor=white
[Keras-url]: https://keras.io/
[Langchain]: https://img.shields.io/badge/langchain-000000?style=for-the-badge&logo=langchain&logoColor=white
[Langchain-url]: https://www.langchain.com/
[Streamlit]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/
[Twilio]: https://img.shields.io/badge/Twilio-F22F46?style=for-the-badge&logo=Twilio&logoColor=white
[Twilio-url]: https://www.twilio.com/pt-br
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 