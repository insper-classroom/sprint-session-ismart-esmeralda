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

# Create your views here.
def index(request):
    return render(request, 'atendimento/index.html')

@login_required
def duvidas(request):
    return render(request, 'atendimento/sobre_duvida.html')

@login_required
def aluno(request):
    print(request.user.uuid)
    return render(request, 'atendimento/aluno.html')

#Mostra as conversas daquele colaborador, filtrando por nao atribuidas e atribuidas
def side_nao_atribuido(request):
    colab = request.user.id
    conversas = Conversa.objects.all()
    notassigned = conversas.filter(assigned_to=None, resolved=False, is_gpt= False)

    return render(request, 'atendimento/side_nao_atribuido.html', {'notassigned': notassigned})

def side_minhas_conversas(request):
    colab = request.user.id 
    conversas = Conversa.objects.filter(assigned_to=colab, resolved=False, is_gpt= False)
    notassigned = conversas.filter(assigned_to=None, resolved=False, is_gpt= False)

    return render(request, 'atendimento/side_minhas_conversas.html', {'yours': conversas, 'notassigned': notassigned})


#view pro colaborador atribuir uma nao atribuida a ele
@csrf_exempt
# @staff_member_required
def assign_conversa(request, conversa_id):
    conversa = Conversa.objects.get(id = conversa_id)
    conversa.assigned_to = request.user
    conversa.save()
    return redirect('side_nao_atribuido')

#view pro colaborador enviar uma mensagem via zap
@csrf_exempt
@staff_member_required
def send_msg(request, telefone, conversa_id):
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
#views para resolver uma duvida da side nao atribuido
def resolveNA(request, conversa_id):
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
    
    conversa.resolved = True
    conversa.delete()
    return redirect('side_nao_atribuido')


#view para resolver uma duvida da side minhas conversas
def resolveYOURS(request, conversa_id):
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
    
    conversa.resolved = True
    conversa.delete()
    return redirect('side_minhas_conversas')


#recebe o id do twilio e cria uma cvs c as tag q veio do twilio, DPS Pega essa conversa q criou e usa a receber_zap pra criar mesagens naquela instancia da cvs
@csrf_exempt
def receber_zap(request):
    account_sid = 'AC4001f4f9199704babdc1297dfffeabda'
    auth_token = '7f9724a8f537cec4e85ac1d86c50b660'


    client = Client(account_sid, auth_token)

    if request.method == 'POST':
        data = request.POST
        if CustomUser.objects.filter(telefone=data['From'][12:]).exists():
            user = CustomUser.objects.get(telefone=data['From'][12:])
        else:
            user = CustomUser.objects.create(telefone=data['From'][12:], is_colaborador=False, username = data['ProfileName'])

        # Checa se ja existe uma conversa com o usuario
        c1 = Conversa.objects.filter(usuarios=user, tag='online').first()

        # Se nao existe, cria uma, uma conversa recem criada eh mandada pro gpt
        if c1 is None:
            c1 = Conversa.objects.create(usuarios=user, tag='online', is_zap=True, is_gpt = True)

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

    
#views pra mandar pra url do chatbot c as informacoes do usuario na url
def chatbot(request, username, useruuid):
    
    return redirect(f'http://localhost:8501/?username={username}/')


#views pra renderizar os sides de acordo com a classificacao
def side_nao_atribuido(request):
    colab = request.user.id
    conversas = Conversa.objects.all()
    notassigned = conversas.filter(assigned_to=None, resolved=False, is_gpt= False)

    return render(request, 'atendimento/side_nao_atribuido.html', {'notassigned': notassigned})


#views pra tela de estatisticas
def estatisticas(request):
    stats = Stats.objects.first()
    notassigned = Conversa.objects.filter(assigned_to=None, resolved=False)
    return render(request, 'atendimento/estatisticas.html', {'stats': stats, 'notassigned': notassigned})


#views pra checar periodicamente se tem conversas q tao a mais de 12 horas sem nenhuma mensagem nova
def check_and_resolve_conversations(request):
    #pega a hora de agora
    now = timezone.now()

    #pega as converas q tao como nao resolvidas e pelo bot
    unresolved_converas = Conversa.objects.filter(resolved = False, is_gpt=True)

    for conversa in unresolved_converas:
        last_message = conversa.mensagens.order_by('-timestamp').first()

        # se a ultima mensagem foi enviada a mais de um certo tempo
        if now - last_message.timestamp > timezone.timedelta(minutes=600):
            return HttpResponse('200 OK')

        #se nao, so retorna qqr coisa 
        else:
            return HttpResponse('302 Found')

    return HttpResponse('Sem conversas pra resolver do bot (nenhuma c tempo suficiente)')


#views para abrir os chats a partir do side nao atribuido
def chat_nao_atribuido(request, conversa_id):
    conversa = Conversa.objects.get(pk=conversa_id)   
    colab = request.user.id 
    conversas = Conversa.objects.filter(assigned_to=colab, resolved=False)
    notassigned = conversas.filter(assigned_to=None, resolved=False) 
    return render(request, 'atendimento/chat_nao_atribuido.html', {'conversa': conversa, 'notassigned': notassigned, 'yours': conversas})

#views para abrir os chats a partir da side minhas conversas
def chat_minhas_conversas(request, conversa_id):
    conversa = Conversa.objects.get(pk=conversa_id)
    colab = request.user.id 
    conversas = Conversa.objects.filter(assigned_to=colab, resolved=False)
    notassigned = conversas.filter(assigned_to=None, resolved=False) 
    return render(request, 'atendimento/chat_minhas_conversas.html', {'conversa': conversa, 'notassigned': notassigned, 'yours': conversas})


#views para mandar emails
def mandar_email(request, user_email, conversa_id):
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

            Mail.objects.create(conversa=Conversa.objects.get(pk = conversa_id), sender=user, subject = subject, content=message)
            return redirect('side_minhas_conversas')
    else:
        form = EmailForm()




#views para receber emails
def receive_email(request):
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
            c1 = Conversa.objects.create(usuarios=user, tag='n sei', is_mail=True)

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
    

