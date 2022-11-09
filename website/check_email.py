# # lrqzmtujgfakuuau
# import smtplib
# from email.message import EmailMessage
# import ssl
#
# email_sender = 'kenzhali1rustam@gmail.com'
# email_pasword = 'lrqzmtujgfakuuau'
#
# subject = 'Check out my new video'
# body = 'BODY'
#
# em = EmailMessage()
# em['From'] = email_sender
# em['To'] = email_sender
# em['Subject'] = subject
# em.set_content(body)
#
# context = ssl.create_default_context()
#
# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#     smtp.login(email_sender, email_pasword)
#     smtp.sendmail(email_sender, email_sender, em.as_string())
