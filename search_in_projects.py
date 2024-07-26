from src.ProjectsGetter import ProjectsGetter
from src.DataLookup import DataLookup
import sys
import os
import logging

def apply_logging_settings():
    global log_level 

    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(log_level)

    
    logging_level = logging.INFO
    if log_level == "DEBUG":
        logging_level = logging.DEBUG
    if log_level == "ERROR":
        logging_level = logging.ERROR
    if log_level == "WARN" or log_level == "WARNING":
        logging_level = logging.WARNING

    logging.basicConfig(
        level=logging_level,
        format="%(asctime)-15s - %(levelname)-6s - %(name)s :: %(message)s" 
    )


    logging.getLogger("requests").setLevel("WARNING")
    logging.getLogger("urllib3").setLevel("WARNING")
    logging.getLogger("urllib3.connectionpool").setLevel("WARNING")

def parse_args(args):
    global tag
    global output
    global env
    global log_level
    global languages
    global key
    global domain
    global value

    tag=None
    output=None
    env="www"
    log_level = "INFO"
    languages=[]
    key=None
    domain="meterian.io"
    value=""

    for arg in args:
        if "--tag=" in arg:
            arg=arg.split("=")
            tag = arg[1]
            

        if "--output=" in arg:
            arg=arg.split("=")
            output = arg[1]

        if "--env=" in arg:
            arg=arg.split("=")
            env = arg[1]
        
        if "--domain=" in arg:
            arg=arg.split("=")
            domain = arg[1]

        if "--debug" in arg:
            log_level="DEBUG"

        if "--languages=" in arg:
            arg=arg.split("=")
            languages = arg[1].split(",")

        if "--key=" in arg:
            arg=arg.split("=")
            key = arg[1]

        if "--value=" in arg:
            arg=arg.split("=")
            value = arg[1]

    if key==None or len(key)==0:
        print("Key to lookup not specified. Use `--key=$KEY` to specify a key.")  
        sys.exit(1)
        
    if output == None or len(output) == 0:
        output=os.path.join("/tmp","meterian."+tag+".bible.json")
        print("No output has been specified. The bible will be created @ "+output)

def parse_env_variables(vars):
    global meterian_token
    try:
        meterian_token = vars["METERIAN_API_TOKEN"]
    except:
        print("Meterian API Token not specified. Export METERIAN_API_TOKEN as environment variable.")
        sys.exit(1)

    if meterian_token == None or len(meterian_token)==0:
        print("Meterian API Token not specified. Export METERIAN_API_TOKEN as environment variable.")
        sys.exit(1)

def is_project_language_among_requested(project):
    for language in project["languages"]:
        try:
            languages.index(language)
            return True
        except:
            pass
    return False

log = logging.getLogger("ProjectsLookupTool")
if __name__ == "__main__":
    print("Meterian - Projects Lookup Tool")
    print()
    parse_env_variables(os.environ)
    parse_args(sys.argv)
    apply_logging_settings()
    print()

    any_language = len(languages)==0
    any_value = len(value)==0

    result = []

    project_getter = ProjectsGetter(meterian_token, env, domain)
    data_lookup = DataLookup()
    try:
        log.info("Getting projects")
        projects = project_getter.get_projects()
        log.info("Found "+str(len(projects))+" projects")
        for project in projects:
            if not any_language and not is_project_language_among_requested(project):
                continue
            log.info("Getting report for project "+project["uuid"])
            report = project_getter.get_report(project["uuid"], project["branch"])
            if not report:
                continue
            log.info("Performing lookup in "+report["uuid"]+ "key: "+key + " value: "+value)
            lookup_results = data_lookup.search(key.split("."), report, lookup_value=value)
            result += [{
                "report": report["uuid"],
                "key": key,
                "results": lookup_results
            }]
            
        data_lookup.dump(result, output)

    except Exception as e:
        log.error(e, exc_info=True)
        sys.exit(1)