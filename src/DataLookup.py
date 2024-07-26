import json
import logging

log=logging.getLogger("DataLookup")

class DataLookup:
    def search(self, lookup_keys, data, lookup_value=None):
        key=lookup_keys[0]
        values = []

        if type(data) != list:
            data = [data]
        for item in data:
            if type(item) == list:
                values += self.search(lookup_keys, item, lookup_value=lookup_value)
                
            if type(item) == dict:
                keys = list(item.keys())
                try:
                    keys.index(key)
                    if len(lookup_keys)>1:
                        lookup_keys.pop(0)
                        values = self.search(lookup_keys, item[key], lookup_value=lookup_value)
                        break
                    if lookup_value and lookup_value not in str(item[key]):
                        continue
                    values.append(item[key])
                except:
                    for item_key in item.keys():
                        values += self.search(lookup_keys, item[item_key], lookup_value=lookup_value)
                    
        
        return values
    
    def dump(self, data, output):
        with open(output, "w") as f:
            json.dump(data, f, indent=4)

