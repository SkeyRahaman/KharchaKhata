import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from flask import session
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer
from flaskr import app


def send_mail(to, name, reset_url):
    login = False
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    try:
        server.login(user=app.config['EMAIL_USERNAME'], password=app.config['EMAIL_PASSWORD'])
        login = True
    except Exception as e:
        print(e)
    if login:
        msg = MIMEMultipart()
        msg['From'] = app.config['EMAIL_USERNAME']
        msg['To'] = to
        msg['subject'] = "Password Reset Email.Do not Reply."
        messege = read_template("flaskr/templates/password_reset_email.html").substitute(PERSON_NAME=name,
                                                                                         PASSWORD=reset_url,
                                                                                         EMAIL=to)
        msg.attach(MIMEText(messege, 'html'))
        server.send_message(msg)
        del msg
    if login:
        server.quit()


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_welcome_email(email, fname, conform_url):
    login = False
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    try:
        server.login(user=app.config['EMAIL_USERNAME'], password=app.config['EMAIL_PASSWORD'])
        login = True
    except Exception as e:
        print(e)
    if login:
        msg = MIMEMultipart()
        msg['From'] = app.config['EMAIL_USERNAME']
        msg['To'] = email
        msg['subject'] = "Welcome to Kharchakhata.com"
        message = read_template("flaskr/authentication/templates/welcome.html").substitute(PERSON_NAME=fname,
                                                                                           email_link=conform_url, )
        msg.attach(MIMEText(message, 'html'))
        server.send_message(msg)
        del msg
    if login:
        server.quit()


def send_welcome_email_for_conformed_emails(email, fname):
    login = False
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    try:
        server.login(user=app.config['EMAIL_USERNAME'], password=app.config['EMAIL_PASSWORD'])
        login = True
    except Exception as e:
        print(e)
    if login:
        msg = MIMEMultipart()
        msg['From'] = app.config['EMAIL_USERNAME']
        msg['To'] = email
        msg['subject'] = "Welcome to Kharchakhata.com"
        message = read_template("flaskr/authentication/templates/welcome_without_conformation.html").substitute(PERSON_NAME=fname)
        msg.attach(MIMEText(message, 'html'))
        server.send_message(msg)
        del msg
    if login:
        server.quit()
