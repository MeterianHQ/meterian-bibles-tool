import requests
from datetime import  datetime
import time
import logging

import json

log = logging.getLogger("BiblesGetter")

class BiblesGetter:
    def __init__(self, project_getter, meterian_token, env="www"):
        self.meterian_token=meterian_token
        self.env=env
        self.project_getter = project_getter

    

    def ask_bible_generation(self, uuid):
        log.debug("Requested creation of bible content for project "+uuid)
        request = requests.post("https://"+self.env+".meterian.com/api/v1/reports/"+uuid+"/bible", headers={"Authorization": "token "+self.meterian_token})
        if request.status_code != 200:
            log.debug(request.__dict__)
            raise ValueError("Could not get bible for project "+uuid)
        gen_id = request.text
        return gen_id

    def ask_bible_status(self, uuid, id):
        request = requests.get("https://"+self.env+".meterian.com/api/v1/reports/"+uuid+"/bible/"+id, headers={"Authorization": "token "+self.meterian_token})
        
        if request.status_code == 200:
            return True
        if request.status_code == 404:
            return False
        
        raise ValueError("Could not get bible for project "+uuid)
        
    def get_bible(self, uuid):
        log.debug("Getting bible...")
        request = requests.get("https://"+self.env+".meterian.com/api/v1/reports/"+uuid+"/bible", headers = {"Authorization": "token "+self.meterian_token})
        if request.status_code != 200:
            log.debug(request.__dict__)
            raise ValueError("Could not get bible for project "+uuid)
        bible = request.json()
        return bible
    
    def get_all(self, projects):
        bibles = []
        full = True
        for project in projects:
            try:
                print("Getting licenses bible for project "+ project)
                gen_id = self.ask_bible_generation(project)
                ready = False
                wait_feedback = "       "
                i=0
                while not ready:
                    if wait_feedback==". . . . ":
                        wait_feedback= "       "
                    print("Waiting for bible content to be generated "+project+wait_feedback, end="\r")
                    if wait_feedback == "       ":
                        wait_feedback= ""
                    wait_feedback+=". "
                    i+=1
                    if i==15:
                        ready = self.ask_bible_status(project, gen_id)
                        i=0
                    time.sleep(1)
                print()
                bible = self.get_bible(project)
                bibles.append(bible)
                print("Project "+project+" done")
                print()
            except Exception as e:
                print("Project "+project+" skipped. Bible will be incomplete.")
                print(e)
                print()
                full = False
                continue

        return {"bibles": bibles, "full": full}