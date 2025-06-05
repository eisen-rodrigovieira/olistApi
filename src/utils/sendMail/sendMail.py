import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from params               import config, configUtils
from keys                 import keys

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

def enviar(destinatario, corpo):
    """
    Envia um e-mail usando SMTP
    
    Parâmetros:
    - destinatario: str - Endereço de e-mail do destinatário
    - corpo: str - Corpo do e-mail
    """
    
    smtp_server = configUtils.SMTP_SERVER
    smtp_port   = configUtils.SMTP_PORT 
    email       = keys.SENDER_MAIL
    pwd         = keys.SENDER_PASSWORD
    subject     = configUtils.SUBJECT_ERROR

    # Criando o objeto da mensagem
    msg = MIMEMultipart()
    msg['From']    = email
    msg['To']      = destinatario
    msg['Subject'] = subject
    msg.attach(MIMEText(corpo, 'html'))

    try:
        # Conectando ao servidor SMTP com SSL
        servidor = smtplib.SMTP_SSL(smtp_server, smtp_port)
        servidor.login(email, pwd)
        servidor.send_message(msg)
        servidor.quit()        
    except Exception as e:
        logger.error("Falha ao enviar e-mail: %s",e)
