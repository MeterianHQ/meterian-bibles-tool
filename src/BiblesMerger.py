import json
class BiblesMerger:
    def __init__(self, output):
        self.output = output
    def merge(self, bibles):
        print("Generating merged version of the licenses bible")
        final = { "components" : {}}
        added = {}
        bibles_list = bibles["bibles"]
        full = bibles["full"]
        for bible in bibles_list:
            for language in bible["components"].keys():
                
                try:
                    final["components"].keys().index(language)
                except:
                    final["components"][language] = []
                try:
                    added.keys().index(language)
                except:
                    added[language] = []

                for component in bible["components"][language]:
                    try:
                        added[language].index(component["name"]+"_"+component["version"])
                    except:
                        added[language].append(component["name"]+"_"+component["version"])
                        final["components"][language].append(component)
        final["_status"] = "partial" if not full else "ok"
        return final

    def dump(self, merged_bible):
        print("Dumping json file...")
        file = open(self.output, "w")
        file.write(json.dumps(merged_bible, indent=4, sort_keys=True))
        file.close()
        print("Merged Bible created @ "+self.output)
