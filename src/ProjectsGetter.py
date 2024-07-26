import requests
import json
import logging
log=logging.getLogger("ProjectsGetter")

class ProjectsGetter:
    def __init__(self, meterian_token, env, domain):
        self.meterian_token = meterian_token
        self.env = env
        self.domain = domain

    def get(self, tag):
        if not tag or len(tag)==0:
            raise ValueError("Tag invalid or not specified")
        print("Getting projects linked to tag "+tag)
        tag_info_request = requests.get("https://"+self.env+"."+self.domain+"/api/v1/accounts/me/tags/"+tag, headers={"Authorization": "token "+self.meterian_token})
        tag_info = tag_info_request.json()
        return tag_info["projects"]
    
    def get_projects(self):
        projects_request = requests.get("https://"+self.env+"."+self.domain+"/api/v2/reports?sinceDaysAgo=3650", headers={"Authorization": "Bearer "+self.meterian_token})
        if projects_request.status_code != 200:
            log.debug(projects_request.url)
            log.debug(projects_request.text)
            raise ValueError("Could not get list of projects")
        projects = projects_request.json()
        return projects

    def get_project_info(self, uuid):
        request = requests.get("https://"+self.env+"."+self.domain+"/api/v1/projects/"+uuid,headers={"Authorization": "token "+self.meterian_token})
        if request.status_code != 200:
            log.debug(request.text)
            raise ValueError("Could not get info for project "+uuid)
        project_info = request.json()
        return project_info
    
    def get_report(self, uuid, branch=None):
        try:
            url = "https://"+self.env+"."+self.domain+"/api/v1/reports/"+uuid+"/full"
            if branch:
                url = url+"?branch="+branch
            request = requests.get(url, headers={"Authorization": "Bearer "+self.meterian_token})
            if request.status_code != 200:
                log.debug(request.text)
                raise ValueError("Could not get report "+uuid)
            report = request.json()
            return report
        except:
            return None

    def parse_project_url(self, project_info):
        project_url = project_info["url"].split("?")[0]
        if ":" in project_url:
            project_url = project_url.split(":")[1]

        return project_url
    

