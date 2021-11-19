import requests
import json
import logging
log=logging.getLogger("ProjectsGetter")

class ProjectsGetter:
    def __init__(self, meterian_token, env="www"):
        self.meterian_token = meterian_token
        self.env = env

    def get(self, tag):
        if not tag or len(tag)==0:
            raise ValueError("Tag invalid or not specified")
        print("Getting projects linked to tag "+tag)
        tag_info_request = requests.get("https://"+self.env+".meterian.com/api/v1/accounts/me/tags/"+tag, headers={"Authorization": "token "+self.meterian_token})
        tag_info = tag_info_request.json()
        return tag_info["projects"]

    def get_project_info(self, uuid):
        request = requests.get("https://"+self.env+".meterian.io/api/v1/projects/"+uuid,headers={"Authorization": "token "+self.meterian_token})
        if request.status_code != 200:
            log.debug(request.text)
            raise ValueError("Could not get info for project "+uuid)
        project_info = request.json()
        return project_info

    def parse_project_url(self, project_info):
        project_url = project_info["url"].split("?")[0]
        if ":" in project_url:
            project_url = project_url.split(":")[1]

        return project_url
    

