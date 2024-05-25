from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Conversa, Mensagem, Stats, EmailForm, Mail
from django.contrib.contenttypes.models import ContentType
from chatbot.classificador import classifier
from users.models import CustomUser
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
import json
from chatbot.classificador import classifier
from twilio.rest import Client
import os
import smtplib
import imaplib
from email.message import EmailMessage
from django.core.mail import send_mail
import mailparser
import email
from email.header import decode_header
from ismart import settings
import re


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


#assim q  o colaborador entrar na tela vai ver as nao atribuidas e o chat em branco
@login_required
def mostra_conversas_home(request):
    colab = request.user.id
    conversas = Conversa.objects.all()
    notassigned = conversas.filter(assigned_to=None, resolved=False)

    return render(request, 'atendimento/info_section.html', {'notassigned': notassigned})

#se clicar p ver as conversas em yours, carrega o template de yours e mostra as conversas tal 
def mostra_conversas_yours(request):
    colab = request.user.id
    conversas = conversas.objects.filter(assigned_to = colab, resolved = False)
    return render(request, 'atendimento/info_sectionyours.html', {'yours': yours})

#extenda o tempalte do chat de acordo c o id do caht q ele requisitou na url 
def mostra_chat(request, conversa_id):
    colab = request.user.id
    conversa = Conversa.objects.get(pk = conversa_id)

    if conversa.assigned_to != request.user:
        conversa.assigned_to = request.user
    convesa.save()

    if conversa.mensagens.exists():
        mensagens = conversa.mensagens.all()    
    elif conversa.mail.exists():
        mensagens = conversa.mail.all()

    return render(request, 'atendimento/chat.html', {'conversa': conversa, 'mensagens': mensagens})
    

#view pro colaborador atribuir uma nao atribuida a ele
@csrf_exempt
@staff_member_required
def assign_conversa(request, conversa_id):
    conversa = Conversa.objects.get(id = conversa_id)
    conversa.assigned_to = request.user
    conversa.save()
    return redirect('tela_colaborador')

#view pro colaborador enviar uma mensagem
@csrf_exempt
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
    return redirect('tela_colaborador')

#view pro colaborador marcar uma conversa como resolvida
@csrf_exempt
@staff_member_required
def resolve(request, conversa_id):
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
    return redirect('tela_colaborador')


#recebe o id do twilio e cria uma cvs c as tag q veio do twilio, DPS Pega essa conversa q criou e usa a receber_zap pra criar mesagens naquela instancia da cvs
@csrf_exempt
def receber_zap(request):
    if request.method == 'POST':
        data = request.POST
        if CustomUser.objects.filter(telefone=data['From'][12:]).exists():
            user = CustomUser.objects.get(telefone=data['From'][12:])
        else:
            user = CustomUser.objects.create(telefone=data['From'][12:], is_colaborador=False, username = data['ProfileName'])

        # Check if a Conversa already exists for the user
        c1 = Conversa.objects.filter(usuarios=user, tag='online').first()

        # If it doesn't exist, create a new one
        if c1 is None:
            c1 = Conversa.objects.create(usuarios=user, tag='online', is_zap=True)   

        Mensagem.objects.create(conversa=c1, sender=user, content=data['Body'])
        return redirect('tela_colaborador')
    else:
        return redirect('tela_colaborador')

    
#views pra mandar pra url do chatbot c as informacoes do usuario na url
def chatbot(request, username, useruuid):
    
    return redirect(f'http://localhost:8501/?username={username}&useruuid={useruuid}')


    

def chat_nao_atribuido(request):
    return render(request, 'atendimento/chat_nao_atribuido.html')

    
    print(f'olá. {username} tem dúvida sobre {tag}')
    return redirect('index')

def mandar_email(request):
    if request.method == "POST":
        form = EmailForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = None
            to_email = 'joaopedroamiguel@gmail.com'

            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )
            redirect ('enviar_email')
    else:
        form = EmailForm()

    return render(request, 'atendimento/sendmailtest.html', {'form': form})

def receive_email(request):
    try:
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
                subject = subject.decode(encoding if encoding else "utf-8")
            
            # Decodificar o remetente
            from_ = msg.get("From")
            
            # Processar o corpo da mensagem
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()
            

        user_mail = re.search(r'<(.*?)>', from_).group(1)

        if CustomUser.objects.filter(email=user_mail).exists():
            user = CustomUser.objects.get(email=user_mail)
        else:
            user = CustomUser.objects.create(email=user_mail, is_colaborador=False, username = 'dasdas')

        c1 = Conversa.objects.filter(usuarios=user).first()

        if c1 is None:
            c1 = Conversa.objects.create(usuarios=user, tag='n sei', is_mail=True)

        Mail.objects.create(conversa=c1, sender=user, subject = subject, content=body)

        email_data = Conversa.objects.all()

        # Desconectar do servidor de e-mail
        mail.close()
        mail.logout()

        # Renderizar os dados no template
        return render(request, 'atendimento/receivemailtest.html', {'emails': email_data})
    
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")