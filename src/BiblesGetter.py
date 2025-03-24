import requests
import time
import logging
import traceback

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

    def get_cyclonedx(self, uuid):
        log.debug("Getting cycloneDX report...")
        request = requests.get("https://"+self.env+".meterian.com/api/v1/reports/"+uuid+"/sbom-cdx.json", headers = {"Authorization": "token "+self.meterian_token})
        if request.status_code != 200:
            log.debug(request.__dict__)
            raise ValueError("Could not get cyclonedx for project "+uuid)
        report = request.json()
        return report

    def get_pdfreport(self, uuid, output_file_path):
        log.debug("Getting PDF report...")
        url = f"https://{self.env}.meterian.com/api/v1/reports/{uuid}/pdf"
        response = requests.get(url, headers={"Authorization": "token " + self.meterian_token}, stream=True)
        if response.status_code != 200:
            log.debug(response.__dict__)
            raise ValueError("Could not get PDF report for project " + uuid)
        
        with open(output_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive chunks
                    f.write(chunk)
                    
    def get_all(self, projects):
        bibles = []
        full = True
        counter = 1
        for uuid in projects:
            try:
                print("Project %s of %s" % (counter, len(projects)))
                counter+=1
        
                project_url = self.prepare_bible(uuid)
        
                bible = self.get_bible(uuid)
                bibles.append(bible)
                print("Project "+project_url+" done")
        
                print()
            except Exception as e:
                print("Project skipped. Bible will be incomplete.")
                print(e)
                traceback.print_exc()
                print()
                full = False
                continue

        return {"bibles": bibles, "full": full}

    def prepare_bible(self, uuid):
        project_info = self.project_getter.get_project_info(uuid)
        project_name = self.project_getter.parse_project_url(project_info)
        return self.prepare_bible_now(uuid, project_name)
    
    
    def prepare_bible_now(self, uuid, project_name):
        gen_id = self.ask_bible_generation(uuid)
        ready = False
        wait_feedback = "       "
        i=0
        while not ready:
            if wait_feedback==".....":
                wait_feedback= "       "
            print("Waiting for bible content to be generated on '"+project_name+"'"+wait_feedback, end="\r")
            if wait_feedback == "       ":
                wait_feedback= ""
            wait_feedback+="."
            i+=1
            if i==15:
                ready = self.ask_bible_status(uuid, gen_id)
                i=0
            time.sleep(1.5)
        print()
        return project_name
