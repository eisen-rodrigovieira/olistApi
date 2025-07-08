import subprocess
import json
import re
from datetime import datetime
import logging
from params import config

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

class taskManager:

    def __init__(self):
        self.task = None
        self.tasks = config.TASKS
        pass

    def run(self):
        cmd = self.make_script()
        completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
        return completed
    
    def get(self, task:str=None):
        number = None
        self.task = self.task or task
        try:
            int(self.task)
            number = True
        except:
            if self.task in self.tasks:
                pass
            else:
                self.task = input("Informe o nome da task")
        finally:        
            if self.task and not number:
                complete = self.run()
                if complete.returncode != 0:
                    return f"An error occured: {res.stderr}"
                else:
                    regex_repetition = r'\d+\w+'
                    regex_interval = r'\d+'
                    res = json.loads(complete.stdout)
                    res_list = []
                    if type(res) == list:
                        for r in res:
                            res_list.append({
                                'Habilitado' : r.get('Enabled'),
                                'Frequencia' : f"{re.search(regex_interval,r.get('CimInstanceProperties')[-2]).group()}D",
                                'Inicio'     : datetime.strptime(r.get('StartBoundary'),'%Y-%m-%dT%H:%M:%S')
                            })
                    else:
                        res_list.append({
                            'Habilitado' : res.get('Enabled'),
                            'Frequencia' : re.search(regex_repetition,res.get('Repetition').get('CimInstanceProperties')[1]).group(),
                            'Inicio'     : datetime.strptime(res.get('StartBoundary'),'%Y-%m-%dT%H:%M:%S')
                        })                        
                    return res_list
            else:
                print("?")
        
        
    def make_script(self):
        return f'''(Get-ScheduledTask -TaskName "{self.task}").Triggers |
                  Select-Object Enabled, StartBoundary, Repetition, CimInstanceProperties |
                  ConvertTo-Json
                '''

if __name__ == '__main__':
    tsk = taskManager()
    info = tsk.run(task=input("Digite o nome da task:"))
    ret = tsk.get(res=info)