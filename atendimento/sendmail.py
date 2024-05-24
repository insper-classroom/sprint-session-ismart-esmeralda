import os
import smtplib
from email.message import EmailMessage

to=["joaopedroamiguel@gmail.com"] #To whoever you want to send the mail

a="""O Tommy é um delicio"""
email_id='ismart.contactmail@gmail.com'
email_pass='usze xwin esxx ecxe'

for i in to:
    
    msg=EmailMessage()

msg['Subject']=';)'
msg['From']=email_id
msg['To']= i
msg.set_content(a)

# if you want to add an attachment
# files=['xxx.pdf']
# for file in files:
#     with open(file,'rb') as f:
#         data=f.read()
#         name=f.namemsg.add_attachment(data,maintype='application',subtype='octet-stream',filename=name)

with smtplib.SMTP_SSL('smtp.gmail.com',465)as smtp:
    smtp.login(email_id,email_pass)
    smtp.send_message(msg)
    smtp.quit()