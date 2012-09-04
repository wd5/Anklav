# -*- coding: utf-8 -*-

from django.core.mail import send_mail

black_list = ['silveri@mail.ru']  # Явно попросившие ничего им не присылать

def email(subject, content, recipients):
    for mail in recipients:
        if mail not in black_list:
            send_mail(subject, content, None, [mail])

    for mail in ('linashyti@gmail.com', 'glader.ru@gmail.com'):
        if not mail in recipients:
            send_mail(subject, content + "\n\nSended to " + ", ".join(recipients), None, [mail])

