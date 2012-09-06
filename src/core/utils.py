# -*- coding: utf-8 -*-

from django.core.mail import send_mail

black_list = ['silveri@mail.ru']  # Явно попросившие ничего им не присылать
topics = [
    u'Анклав: Новая запись',
    u'Анклав: роль',
    u'Анклав: закрыто',
    u'Анклав: уведомление',
    u'Анклав: новое предложение',
]  # Почта, которую не надо отправлять админу

def email(subject, content, recipients, admins=True):
    for mail in recipients:
        if mail not in black_list:
            try:
                send_mail(subject, content, None, [mail])
            except Exception:
                pass

    if admins:
        if not 'linashyti@gmail.com' in recipients:
            send_mail(subject, content + "\n\nSended to " + ", ".join(recipients), None, ['linashyti@gmail.com'])

        if not 'glader.ru@gmail.com' in recipients and not any(subject.startswith(topic) for topic in topics):
                send_mail(subject, content + "\n\nSended to " + ", ".join(recipients), None, ['glader.ru@gmail.com'])


