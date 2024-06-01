from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Conversa, Mensagem, Stats, EmailForm, Mail
from django.contrib.contenttypes.models import ContentType
from chatbot.classificador import classifier
from django.utils import timezone
from users.models import CustomUser
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
import json
from chatbot.classificador import classifier
from .raglogic import get_prompt
from twilio.rest import Client
import smtplib
import imaplib 
import os
from email.message import EmailMessage
from django.core.mail import send_mail
import mailparser
import email
from email.header import decode_header
from ismart import settings
import re
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = os.getenv('OPENAI_API_KEY')


def index(request):
    """
    Essa função renderiza a primeira página de index do site.
    
    Parâmetros:
        request (HttpRequest): O objeto da requisição HTTP.
        
    Retorno:
        HttpResponse: O template renderizado.
    """
    return render(request, 'atendimento/index.html')


@login_required
def duvidas(request):
    """
    Essa função renderiza a página de login.
    
    Parâmetros:
        request (HttpRequest): O objeto da requisição HTTP.
        
    Retorno:
        HttpResponse: O template renderizado.
    """
    return render(request, 'atendimento/sobre_duvida.html')


@login_required
def aluno(request):
    """
    Essa função renderiza a página principal do aluno.
    
    Parâmetros:
        request (HttpRequest): O objeto da requisição HTTP.
        
    Retorno:
        HttpResponse: O template renderizado.
    """
    return render(request, 'atendimento/aluno.html')


@login_required
@staff_member_required
def side_nao_atribuido(request):
    """
    View para renderizar o template 'side_nao_atribuido.html' com uma lista de conversas sem colaboradores atribuídos

    Parâmetros:
    - request: O objeto da requisição HTTP.

    Retorna:
    - O template renderizado com a lista de conversas sem atribuídos.

    """

    colab = request.user.id
    conversas = Conversa.objects.all()
    notassigned = conversas.filter(assigned_to=None, resolved=False, is_gpt=False)

    return render(request, 'atendimento/side_nao_atribuido.html', {'notassigned': notassigned})


@login_required
@staff_member_required
def side_minhas_conversas(request):
    """
    View para renderizar o template 'minhas_conversas.html' com uma lista de conversas que o colaborador autenticado está atribuído.

    Parâmetros:
    - request: O objeto da requisição HTTP.

    Retorna:
    - O template renderizado com a lista de conversas atribuídas ao colaborador.

    """

    colab = request.user.id 
    conversas = Conversa.objects.filter(assigned_to=colab, resolved=False, is_gpt= False)
    tudo = Conversa.objects.all()
    notassigned = tudo.filter(assigned_to=None, resolved=False, is_gpt= False)

    return render(request, 'atendimento/side_minhas_conversas.html', {'yours': conversas, 'notassigned': notassigned})


@csrf_exempt
@staff_member_required
@login_required
def assign_conversa(request, conversa_id):
    """
    View para atribuir uma conversa de id 'conversa_id' ao colaborador autenticado.

    Parâmetros:
    - request: O objeto da requisição HTTP.
    - conversa_id: o ID da conversa a ser atribuída ao colaborador.

    Returna:
    - Uma resposta redirecionando o colaborador para a url 'side_nao_atribuido'.
    """

    conversa = Conversa.objects.get(id=conversa_id)
    conversa.assigned_to = request.user
    conversa.save()
    return redirect('side_nao_atribuido')


@csrf_exempt
@staff_member_required
@login_required
def send_msg(request, telefone, conversa_id):
    """
    View para enviar uma mensagem via WhatsApp.

    Parâmetros:
    - request: O objeto da requisição HTTP.
    - telefone: O número de telefone para enviar a mensagem.
    - conversa_id: O ID da conversa relacionada à mensagem.

    Retorna:
    - Uma resposta redirecionando para a página de chat da conversa.
    """
    account_sid = 'AC4001f4f9199704babdc1297dfffeabda'
    auth_token = '7f9724a8f537cec4e85ac1d86c50b660'

    client = Client(account_sid, auth_token)

    mensagem = request.POST['mensagem']

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=mensagem,
        to=f'whatsapp:+55{telefone}'
    )

    Mensagem.objects.create(conversa=Conversa.objects.get(pk=conversa_id), sender=request.user, content=mensagem)

    conversa = Conversa.objects.get(id=conversa_id)

    conversa.save()
    return redirect(f'/side_minhas_conversas/chat_minhas_conversas/{conversa_id}/')
    account_sid = 'AC4001f4f9199704babdc1297dfffeabda'
    auth_token = '7f9724a8f537cec4e85ac1d86c50b660'

    client = Client(account_sid, auth_token)

    mensagem = request.POST['mensagem']

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=mensagem,
        to=f'whatsapp:+55{telefone}'
    )

    Mensagem.objects.create(conversa=Conversa.objects.get(pk = conversa_id), sender=request.user, content=mensagem)

    conversa = Conversa.objects.get(id = conversa_id)

    conversa.save()
    return redirect(f'/side_minhas_conversas/chat_minhas_conversas/{conversa_id}/')


@csrf_exempt
@staff_member_required
@login_required
def resolveNA(request, conversa_id):
    """
    Marca uma conversa como resolvida, atualizando a tabela de estatísticas e apagando a mesma conversa, logo em seguida.

    Parâmetros:
    - request: O objeto da requisição HTTP.
    - conversa_id: O ID da conversa a ser marcada como resolvida.

    Returns:
    - Uma resposta de redirect para a URL 'side_nao_atribuido'.

    Descrição:
    - Para marcar uma conversa como resolvida:
      1. Pega a conversa do banco de dados pelo 'conversa_ID'.
      2. Recupera as três últimas mensagens enviadas pelo usuário na conversa.
      3. Concatena essas três mensagens em uma única string.
      4. Classifica o conteúdo da conversa de acordo com tags definidas pelo classificador.
      5. Atualiza a tabela de estatísticas.
      7. Deletes the conversation object.
      8. Redireciona para a URL 'side_nao_atribuido'.

    Observação:
    - A função do classificador não está definida nesse arquivo, mas no arquivo 'classificador.py', dentro do diretório 'chatbot'.
    """

    msgs = ''
    conversa = Conversa.objects.get(pk=conversa_id)
    #pega as tres primeiras mensagens enviadas pelo usuario nessa conversa
    mensagens = conversa.mensagens.all().order_by('id')[:3]
    #concatena essas tres mensagens em uma string
    for mensagem in mensagens:
        msgs += mensagem.content

    tag = classifier(msgs)
    #atualiza as estatisticas
    stats = Stats.objects.first()
    if stats is None:
        stats = Stats.objects.create()
    else:
        if tag == 'Sobre o Ismart':
            stats.sobreosismart += 1
        elif tag == 'Ismart online':
            stats.ismartonline += 1
        elif tag == 'Processo seletivo':
            stats.processoseletivo += 1
        elif tag == 'Bolsas de estudo':
            stats.bolsasdeestudo += 1
        stats.save()
    
    conversa.resolved = True
    conversa.delete()
    return redirect('side_nao_atribuido')


@staff_member_required
@login_required
def resolveYOURS(request, conversa_id):
    """
    Marca uma conversa como resolvida, atualizando a tabela de estatísticas e apagando a mesma conversa, logo em seguida.

    Parâmetros:
    - request: O objeto da requisição HTTP.
    - conversa_id: O ID da conversa a ser marcada como resolvida.

    Returns:
    - Uma resposta de redirect para a URL 'side_nao_atribuido'.

    Descrição:
    - Para marcar uma conversa como resolvida:
      1. Pega a conversa do banco de dados pelo 'conversa_ID'.
      2. Recupera as três últimas mensagens enviadas pelo usuário na conversa.
      3. Concatena essas três mensagens em uma única string.
      4. Classifica o conteúdo da conversa de acordo com tags definidas pelo classificador.
      5. Atualiza a tabela de estatísticas.
      7. Deletes the conversation object.
      8. Redireciona para a URL 'side_minhas_converas'.

    Observação:
    - A função do classificador não está definida nesse arquivo, mas no arquivo 'classificador.py', dentro do diretório 'chatbot'.
    """

    account_sid = 'AC4001f4f9199704babdc1297dfffeabda'
    auth_token = '7f9724a8f537cec4e85ac1d86c50b660'

    client = Client(account_sid, auth_token)

    msgs = ''
    conversa = Conversa.objects.get(pk=conversa_id)
    #pega as tres primeiras mensagens enviadas pelo usuario nessa conversa
    mensagens = conversa.mensagens.all().order_by('id')[:3]
    #concatena essas tres mensagens em uma string
    for mensagem in mensagens:
        msgs += mensagem.content

    tag = classifier(msgs)
    #atualiza as estatisticas
    stats = Stats.objects.first()
    if stats is None:
        stats = Stats.objects.create()
    else:
        if tag == 'Sobre o Ismart':
            stats.sobreosismart += 1
            stats.totalresolvidos += 1
        elif tag == 'Ismart online':
            stats.ismartonline += 1
            stats.totalresolvidos += 1
        elif tag == 'Processo seletivo':
            stats.processoseletivo += 1
            stats.totalresolvidos += 1
        elif tag == 'Bolsas de estudo':
            stats.bolsasdeestudo += 1
            stats.totalresolvidos += 1
        stats.save()
    
    #qdo o colaborador marca a conversa como resolvida, manda uma msg pro usuario perguntando se a duvida foi resolvida ou nn 
    conversa.resolved = True

    telefone = CustomUser.objects.get(id = conversa.usuarios.id).telefone

    uuid = CustomUser.objects.get(id = conversa.usuarios.id).uuid
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'responda essa pesquisa de satisfacao para nos ajudar a melhorar nossos servicos: https://z6n5drvz-8000.brs.devtunnels.ms/satisfacao/{uuid}/',
        to=f'whatsapp:+55{telefone}'
    )
    conversa.is_avaliada = False
    conversa.save()
    return redirect('side_minhas_conversas')


@csrf_exempt
def receber_zap(request):
    """
    Recebe um POST contendo dados sobre uma mensagem recebida pelo whatsapp, e processa essa mensagem.

    Parâmetros:
        request: O objeto da requisição HTTP contendo os dados do POST.

    Retorna:
        HttpResponse: A resposta HTTP indicando o status da requisição.

    Descrição:
        Essa função processa o recebimento de mensagens do whatsapp. Aqui, é utilizada a API do Twilio para receber os dados do usuário que está enviando a mensagem. A função checa se existe algum usuário cadastrado no banco de dados com o telefone do whatsapp que enviou a mensagem, se sim atribui a conversa àquele usuário, caso contrário, é criado um novo usuário. Assim que criada, a conversa é encaminhada para ser respondida pelo gpt-3.5, sendo alimentado por um sistema de RAG(Retrieval Augmented Generation). A função também faz com que as repostas do GPT cheguem ao usuário pelo whatsapp. Após uma certa quantidade de respostas do GPT, o usuário é perguntado se gostaria de ser atendido por um atendente real, se sim, é redirecionado.

    Observação:
        A função que define o sistema de RAG não está definida nesse arquivo, mas sim, no arquivo 'raglogic.py', presente no diretório 'chatbot'.
        
    """

    account_sid = 'AC4001f4f9199704babdc1297dfffeabda'
    auth_token = '7f9724a8f537cec4e85ac1d86c50b660'

    client = Client(account_sid, auth_token)

    if request.method == 'POST':
        data = request.POST
        if CustomUser.objects.filter(telefone=data['From'][12:]).exists():
            user = CustomUser.objects.get(telefone=data['From'][12:])
        else:
            user = CustomUser.objects.create(telefone=data['From'][12:], is_colaborador=False, username = data['ProfileName'])

        c1 = Conversa.objects.filter(usuarios=user, resolved=False).first()

        # Se nao existe, cria uma, uma conversa recem criada eh mandada pro gpt
        if c1 is None:
            c1 = Conversa.objects.create(usuarios=user, is_zap=True, is_gpt = True)

        # Cria uma instancia de mensagem pro usuario
        Mensagem.objects.create(conversa=c1, sender=user, content=data['Body'])

        if c1.bot_response_count == 2:
            message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='Se desejar falar com um atendente real, digite Sim, e se quiser continuar tirando dúvidas comigo, digite Não.',
            to=f'whatsapp:+55{user.telefone}'
        )
        if data['Body'].lower() == 'sim' and c1.is_gpt:
                c1.is_gpt = False
                Mensagem.objects.filter(conversa = c1).delete()
                c1.save()
                message = client.messages.create(
                from_='whatsapp:+14155238886',
                body='olá! como posso te ajudar hoje?',
                to=f'whatsapp:+55{user.telefone}'
                )

        # Definindo o modelo do OpenAI
        modelos = {'openai_model': 'gpt-3.5-turbo'}

        messages = [{"role": "system", "content": "you are a helpful assistant"}, {'role': 'assistant', 'content': 'Sou a coruja, assistente virtual aqui do Ismart. Como posso te ajudar hoje? Pode perguntar qualquer coisa! 🦉'}]
        # se a flag da conversa is_gpt for true, manda a mensagem pro gpt
        if c1.is_gpt:
            messages.append({'role': 'user', 'content': get_prompt(data['Body'])})
            response = openai.chat.completions.create(
                model=modelos['openai_model'],
                messages=messages
            )
            # manda a resposta do gpt pro usuario
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=response.choices[0].message.content,
                to=f'whatsapp:+55{user.telefone}'
            )
            c1.bot_response_count += 1
            c1.save()
        return HttpResponse('200 OK')
    else:
        return HttpResponse('404 Not Found')

    
def chatbot(request, username):
    """Manda o aluno para ser atendido pelo GPT dentro do ambiente web, enviando seu nome. 
        Parâmetros:
            request: Objeto da requisição HTTP
            username: Nome de usuário do aluno que será atendido pelo chatbot
        
        Retorna:
            Uma resposta de redirect para a URL em que está hospedado o chatbot. 
    """

    return redirect(f'http://localhost:8501/?username={username}')


@staff_member_required
@login_required
def estatisticas(request):
    """
    View para renderizar a página de estatísticas

    Parâmetros:
    - request: O objeto da requisição HTTP.

    Retorna:
    - O template renderizado com os dados da tela de estatísticas.

    """
    
    stats = Stats.objects.first()
    notassigned = Conversa.objects.filter(assigned_to=None, resolved=False)
    satisfacao = stats.satisfacao_users
    
    topicos = {
        'Sobre o Ismart': stats.sobreosismart,
        'Ismart Online': stats.ismartonline,
        'Processo Seletivo': stats.processoseletivo,
        'Bolsas de Estudo': stats.bolsasdeestudo,
    }
    
    most_frequent_topic = max(topicos, key=topicos.get)
    return render(request, 'atendimento/estatisticas.html', {'stats': stats, 'notassigned': notassigned, 'mostfrequent': most_frequent_topic, 'satisfacao': satisfacao})



def check_and_resolve_conversations(request):
    """
    Verifica e resolve as conversas que estão pendentes de resolução pelo bot. Conversas que estão a mais de 12 horas sem interação alguma no whatsapp sao marcadas como resolvidas.

    Parâmetros:
        request: O objeto de requisição HTTP.

    Retorna:
        Uma resposta HTTP indicando o resultado da verificação e resolução das conversas.

    """

    #pega a hora de agora
    now = timezone.now()

    #pega as converas q tao como nao resolvidas e pelo bot
    unresolved_converas = Conversa.objects.filter(resolved = False, is_gpt=True)

    for conversa in unresolved_converas:
        last_message = conversa.mensagens.order_by('-timestamp').first()

        # se a ultima mensagem foi enviada a mais de um certo tempo
        if now - last_message.timestamp > timezone.timedelta(minutes=600):
            Stats.totalresolvidosgpt += 1
            return redirect('resolve', conversa.id)

        #se nao, so retorna qqr coisa 
        else:
            return HttpResponse('302 Found')

    return HttpResponse('Sem conversas pra resolver do bot (nenhuma c tempo suficiente)')


@staff_member_required
@login_required
def chat_nao_atribuido(request, conversa_id):
    """
    Renderiza a página de chat não atribuído, junto às mensagens enviadas nessa mesma conversa.

    Parâmetros:
    - request: O objeto HttpRequest contendo os dados da requisição HTTP.
    - conversa_id: O ID da conversa a ser exibida.

    Retorno:
    - Um objeto HttpResponse contendo a página renderizada.

    """

    conversa = Conversa.objects.get(pk=conversa_id)   
    colab = request.user.id 
    conversas = Conversa.objects.filter(assigned_to=colab, resolved=False)
    notassigned = conversas.filter(assigned_to=None, resolved=False) 
    return render(request, 'atendimento/chat_nao_atribuido.html', {'conversa': conversa, 'notassigned': notassigned, 'yours': conversas})


@staff_member_required
@login_required
def chat_minhas_conversas(request, conversa_id):
    """
    Renderiza a página de chat atribuído ao colaborador autenticado, junto às mensagens enviadas nessa mesma conversa.

    Parâmetros:
    - request: O objeto HttpRequest contendo os dados da requisição HTTP.
    - conversa_id: O ID da conversa a ser exibida.

    Retorno:
    - Um objeto HttpResponse contendo a página renderizada.

    """

    conversa = Conversa.objects.get(pk=conversa_id)
    colab = request.user.id 
    conversas = Conversa.objects.filter(assigned_to=colab, resolved=False)
    notassigned = conversas.filter(assigned_to=None, resolved=False) 
    return render(request, 'atendimento/chat_minhas_conversas.html', {'conversa': conversa, 'notassigned': notassigned, 'yours': conversas})


@staff_member_required
@login_required
def mandar_email(request, user_email, conversa_id):
    """
    Envia um email para o usuário que entrou em contato com o colaborador.

    Parâmetros:
        request (HttpRequest): O objeto HttpRequest que representa a requisição HTTP.
        user_email (str): O endereço de email do destinatário.
        conversa_id (int): O ID da conversa.

    Retorna:
        HttpResponseRedirect: Redireciona para a página 'side_minhas_conversas' após o envio do email.

    """

    user = request.user
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = settings.EMAIL_HOST_USER
            email_pass = settings.EMAIL_HOST_PASSWORD
            to_email = user_email

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = to_email
            msg.set_content(message)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(from_email, email_pass)
                smtp.send_message(msg)

            Mail.objects.create(conversa=Conversa.objects.get(pk=conversa_id), sender=user, subject=subject, content=message)
            return redirect('side_minhas_conversas')
    else:
        form = EmailForm()


def receive_email(request):
    """
    Função responsável por receber e processar e-mails.

    Parâmetros:
        request: O objeto de requisição HTTP.

    Retorna:
        Uma resposta HTTP com o status '200 OK'.
    """
    
    # Conectar ao servidor de e-mail
    mail = imaplib.IMAP4_SSL(settings.EMAIL_HOST)
    mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    mail.select("inbox")

    # Buscar os e-mails não lidos
    status, messages = mail.search(None, '(ALL)')

    email_data = []
    for num in messages[0].split():
        status, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        mail_content = mailparser.parse_from_bytes(msg_data[0][1])
        
        # Decodificar o assunto
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "latin-1")
        
        # Decodificar o remetente
        from_ = msg.get("From")
        
        # Processar o corpo da mensagem
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")
        

    user_mail = re.search(r'<(.*?)>', from_).group(1)

    if CustomUser.objects.filter(email=user_mail).exists():
        user = CustomUser.objects.get(email=user_mail)
    else:
        user = CustomUser.objects.create(email=user_mail, is_colaborador=False, username = user_mail)

    c1 = Conversa.objects.filter(usuarios=user).first()

    if c1 is None:
        c1 = Conversa.objects.create(usuarios=user, is_mail=True)

    #se essa msg ja existe na cvs ja retorna sem criar a mensagem
    if Mail.objects.filter(conversa=c1, subject = subject, content=body).exists():
        return HttpResponse('200 OK')
    else:    
        Mail.objects.create(conversa=c1, sender=user, subject = subject, content=body)

    email_data = Conversa.objects.all()

    # Desconectar do servidor de e-mail
    mail.close()
    mail.logout()

    return HttpResponse('200 OK')
    
def satisfacaozap(request, user_uuid):
    user = CustomUser.objects.get(uuid = user_uuid)
    c1 = Conversa.objects.filter(usuarios = user, is_avaliada = False).last()
    stats = Stats.objects.all().last()

    if request.method == 'POST':
        if 'satisfacao' in request.POST:
            if request.POST['satisfacao'] == 'Sim':
                c1.is_avaliada = True
                stats.totalresolvidos += 1
                c1.save()
                stats.save()
            if request.POST['satisfacao'] == 'Não':
                c1.is_avaliada = True
                stats.totalnaoresolvidos += 1
                c1.save()
                stats.save()
            return redirect('index')
        else:
            return redirect('index')
    return render(request, 'atendimento/satisfacao.html', {'usertel': user_uuid, 'conversa': c1})
