from email.message import EmailMessage
import smtplib

def SMTPmail(from_add):
    to_addr = str(input("Enter recepient - "))
    message = EmailMessage()
    message['Subject'] = 'Hello from VS Code!'
    message['From'] = from_add
    message['To'] = to_addr
    message.set_content('This is the email body.')
    return message


def buildProtocol(username, password):
    with smtplib.SMTP('smtp.gmail.2com', 587) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        message = SMTPmail(username)
        smtp.send_message(message)


username = str(input("Enter the username - "))
password = str(input("Enter the password - "))
buildProtocol(username, password)                # It gives an Autentication Error as Output