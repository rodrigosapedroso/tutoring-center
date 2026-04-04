import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

def send_email(to_email: str, name: str, temporary_password: str):
    try:
        # Create message container
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = to_email
        message["Subject"] = f"Acesso à plataforma"

        body = f"""
        Bem-vindo à plataforma, {name}!<br><br>
        A sua conta foi criada com sucesso na nossa plataforma.<br>

        Os seus dados de acesso:<br>
        Email: {to_email}<br>
        Password temporária: <b>{temporary_password}</b><br><br>

        Por favor altere a password no primeiro login, para uma à sua escolha.<br><br>
        Cumprimentos,<br>
        Da equipa do centro de aprendizagem
        """
        message.attach(MIMEText(body, "html"))  

        # Conect to Gmail SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # initialize TLS for encryption
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, message.as_string())

        print(f"Email sent successfully to {to_email}")

    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        raise 