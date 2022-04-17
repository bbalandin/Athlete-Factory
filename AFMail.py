import smtplib
from email.mime.text import MIMEText


def send_email(to, use_telegram, body="Спасибо за регистрацию!"):
    if use_telegram:
        body += "\nКстати, это наш бот, который вам поможет: http://t.me/athlete_factory_bot"
    # статичные данные
    smtp_host = "smtp.gmail.com"
    af_mail = "athlete.factory.messages@gmail.com"
    mail_login, mail_password = "athlete.factory.messages@gmail.com", "afga2022forgmailprostonado"
    # подключение и отправка сообщения
    server = smtplib.SMTP(host=smtp_host, port=587)
    server.starttls()
    server.login(mail_login, mail_password)
    server.sendmail(from_addr=af_mail, to_addrs=[to], msg=str(MIMEText(body, _charset="utf-8")), mail_options=(""))
    server.quit()