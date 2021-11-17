import requests
import json

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
        print("Getting info for project "+uuid)
        request = requests.get("https://"+self.env+".meterian.io/api/v1/reports/"+uuid+"/full",headers={"Authorization": "token "+self.meterian_token})
        if request.status_code != 200:
            raise ValueError("Could not get download key for project "+uuid)
        report = request.json()
        return {
            "download_key": report["downloadKey"],
            "uuid": uuid,
            "branch": report["project"]["branch"]
        }

