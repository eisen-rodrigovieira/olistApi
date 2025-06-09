import os
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

class sendMail:

    def __init__(self):
        self.email_body_path = configUtils.BODY_HTML
        self.smtp_server     = configUtils.SMTP_SERVER
        self.smtp_port       = configUtils.SMTP_PORT 
        self.email           = keys.SENDER_MAIL
        self.pwd             = keys.SENDER_PASSWORD        
        self.default_to      = configUtils.TO_DEFAULT
        
        
    async def enviar(self,destinatario:str=None, corpo=None, assunto:str=None):
        """
        Envia um e-mail usando SMTP
        
        Parâmetros:
        - destinatario: str - Endereço de e-mail do destinatário
        - corpo: str - Corpo do e-mail
        """

        # Criando o objeto da mensagem
        msg = MIMEMultipart()
        msg['From']    = self.email
        msg['To']      = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'html'))

        try:
            # Conectando ao servidor SMTP com SSL
            servidor = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            servidor.login(self.email, self.pwd)
            servidor.send_message(msg)
            servidor.quit()        
        except Exception as e:
            logger.error("Falha ao enviar e-mail: %s",e)

    async def notificar(self, destinatario:str=None, tipo:str='erro'):

        assunto = None
        if not os.path.exists(self.email_body_path):
            logger.error("Arquivo não encontrado em %s.",self.email_body_path)            
        else:
            with open(file=self.email_body_path, mode='r', encoding='utf-8') as f:
                body = f.read() 

        if not os.path.exists(config.PATH_LOGS):
            logger.error("Arquivo não encontrado em %s.",config.PATH_LOGS)            
        else:
            with open(file=config.PATH_LOGS, mode='r', encoding='utf-8') as f:
                log_data = f.readlines()

        match tipo:
            case 'erro':
                assunto = configUtils.SUBJECT_ERROR["text"]
                cor = configUtils.SUBJECT_ERROR["color"]
            case 'alerta':
                assunto = configUtils.SUBJECT_WARN["text"]
                cor = configUtils.SUBJECT_WARN["color"]
            case _:
                None
        
        if body and log_data and assunto:

            await self.enviar(destinatario=destinatario or self.default_to,
                              corpo=body.format(cor,log_data[-1]),
                              assunto=assunto)