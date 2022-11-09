from flask import session
from jinja2 import Template

# SEND MAIL FROM GMAIL
import smtplib
from email.message import EmailMessage
import ssl
email_sender = 'kenzhali1rustam@gmail.com'
email_pasword = 'lrqzmtujgfakuuau'


def code_confirm(email, subject, body):
    global email_sender, email_pasword
    from random import randint
    code = randint(100000, 999999)
    session['send_code'] = str(code)
    msg = body.render(code=code)
    # print('SAVE SESSION CODE: ' + session['send_code'] )
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email
    em['Subject'] = subject
    em.set_content(msg)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_pasword)
        smtp.sendmail(email_sender, email, em.as_string())


def phone_num_floorproof(phone):
    if phone[0] == '8' and len(phone) == 11 and phone[1:4] in ['727', '700', '708', '705', '771', '776', '777', '701', '702', '775', '778', '707', '747']:
        phone = '+7' + phone[1:]
        return True
    elif phone[0] == '+' and len(phone) == 12 and phone[1:5] in ['7727', '7700', '7708', '7705', '7771', '7776', '7777', '7701', '7702', '7775', '7778', '7707', '7747']:
        return True
    else:
        return False