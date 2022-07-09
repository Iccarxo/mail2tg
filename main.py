import imaplib
import email
import time
from email.header import decode_header
import base64
import telebot


telegram_id = 11111111
TOKEN = ''

# Mail
FROM_EMAIL = "mail" + "@domain.com"

# Application password of email
FROM_PWD = ""

# SMTP-server
SMTP_SERVER = "imap.mail.ru"

# Port of SMTP-Server
SMTP_PORT = 993

bot = telebot.TeleBot(TOKEN)

def main_programm():


    def get_mail():
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')
        type, data = mail.search(None, 'ALL')

        typ, msg_data = mail.fetch(data[0].split()[-1], '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

            maintype = msg.get_content_maintype()

            if maintype == 'multipart':
                for part in msg.get_payload():
                    if part.get_content_maintype() == 'text':
                        return msg['subject'], part.get_payload().strip(), msg['from']

            elif maintype == 'text':
                return msg['subject'], msg.get_payload().strip(), msg['from']

    prev = ()

    while True:
        message = get_mail()
        if message != prev:

            tema_coded = decode_header(message[0])[0][0]
            b = message[1]
            c = base64.b64decode(b)
            mail_message = c.decode("utf8")
            tema_encoded = tema_coded.decode("utf8")

            sender_mail = decode_header(message[2])[1][0].decode("utf8").replace('<', '').replace('>', '')
            sender_name = decode_header(message[2])[0][0].decode("utf8").strip().replace('  ', ' ')

            bot.send_message(telegram_id, f'{tema_encoded}\n{sender_name}\n{sender_mail}\n\n{mail_message}')

            prev = message

        else:
            pass

        time.sleep(5)


if __name__ == '__main__':
    main_programm()
