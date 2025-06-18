import os
import json
import logging
from params             import config
from src.utils.sendMail import sendMail

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

class validaPath:

    def __init__(self):
        self.email = sendMail()

    async def validar(self,path:str=None, mode:str=None, method:str=None, content=None):
        encoding = "utf-8"
        if not os.path.exists(path):
            logger.error("Arquivo não encontrado em %s.",path)
            await self.email.notificar()
            return False
        else:
            if mode == 'r' and not content:
                if method == 'full':
                    with open(file=path, mode=mode, encoding=encoding) as f:
                        content = f.read() 
                elif method == 'lines':
                    with open(file=path, mode=mode, encoding=encoding) as f:
                        content = f.readlines()
                elif method == 'json':
                    with open(file=path, mode=mode, encoding=encoding) as f:
                        content = json.load(f)
                elif method == 'q-split':
                    with open(file=path, mode=mode, encoding=encoding) as f:
                        content = f.read().splitlines()
                return content
            elif mode == 'w' and content:
                if method in ['full','lines']:
                    with open(file=path, mode=mode, encoding=encoding) as f:
                        f.write(content) 
                elif method == 'json':
                    with open(file=path, mode=mode, encoding=encoding) as f:
                        json.dump(content, f, indent=4, ensure_ascii=False)
                return content
            else:
                return None        
              