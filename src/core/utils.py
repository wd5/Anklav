# -*- coding: utf-8 -*-

from django.core.mail import send_mail

def email(subject, content, recipients):
    for mail in recipients:
        send_mail(subject, content, None, [mail])

    for mail in ('linashyti@gmail.com', 'glader.ru@gmail.com'):
        if not mail in recipients:
            send_mail(subject, content + "\n\nSended to " + ", ".join(recipients), None, [mail])

