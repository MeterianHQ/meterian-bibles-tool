import json
class BiblesMerger:
    def __init__(self, output):
        self.output = output
    def merge(self, bibles):
        print("Generating merged version of the licenses bible")
        final = { "_status": "ok", "components" : {}, "licenses":[]}
        added_components = {}
        added_licenses=[]
        bibles_list = bibles["bibles"]
        full = bibles["full"]
        for bible in bibles_list:
            for language in bible["components"].keys():
                try:
                    final["components"].keys().index(language)
                except:
                    final["components"][language] = []
                try:
                    added_components.keys().index(language)
                except:
                    added_components[language] = []

                for component in bible["components"][language]:
                    try:
                        added_components[language].index(component["name"]+"_"+component["version"])
                    except:
                        added_components[language].append(component["name"]+"_"+component["version"])
                        final["components"][language].append(component)

            for license in bible["licenses"]:
                try:
                    added_licenses.index(license["name"])
                except:
                    added_licenses.append(license["name"])
                    final["licenses"].append(license)
                    
        final["_status"] = "partial" if not full else "ok"
        return final

    def dump(self, merged_bible):
        print("Dumping json file...")
        file = open(self.output, "w")
        file.write(json.dumps(merged_bible, indent=4, sort_keys=True))
        file.close()
        print("Merged Bible created @ "+self.output)
