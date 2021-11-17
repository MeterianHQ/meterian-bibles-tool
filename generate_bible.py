from src.BiblesGetter import BiblesGetter
from src.BiblesMerger import BiblesMerger
from src.ProjectsGetter import ProjectsGetter
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
    global meterian_token
    global output
    global env
    global log_level

    tag=None
    meterian_token=None
    output=None
    env="www"
    log_level = "INFO"

    for arg in args:
        if "--tag=" in arg:
            arg=arg.split("=")
            tag = arg[1]
            if len(tag)==0:
                print("Tag not specified. Use `--tag=$TAG` to specify a tag.")
                sys.exit(1)

        if "--meterian-token=" in arg:
            arg=arg.split("=")
            meterian_token = arg[1]
            if len(meterian_token)==0:
                print("Meterian API Token not specified. Use `--meterian-token=$METERIAN_API_TOKEN` to specify the Meterian API Token.")
                sys.exit(1)

        if "--output=" in arg:
            arg=arg.split("=")
            output = arg[1]

        if "--env=" in arg:
            arg=arg.split("=")
            env = arg[1]
            if env != "www" and env != "qa" and env != "local":
                env="www"

        if "--debug" in arg:
            log_level="DEBUG"
        
    if output == None or len(output) == 0:
        output=os.path.join("/tmp","meterian."+tag+".bible.json")
        print("No output has been specified. The bible will be created @ "+output)

if __name__ == "__main__":
    print("Meterian - Bibles Tool")
    print()
    parse_args(sys.argv)
    apply_logging_settings()
    print()

    project_getter = ProjectsGetter(meterian_token, env)
    bibles_getter = BiblesGetter(project_getter, meterian_token, env)
    bibles_merger = BiblesMerger(output)
    try:
        projects = project_getter.get(tag)
        bibles = bibles_getter.get_all(projects)
        merged_bible = bibles_merger.merge(bibles)
        bibles_merger.dump(merged_bible)
    except Exception as e:
        print(e)
        sys.exit(1)