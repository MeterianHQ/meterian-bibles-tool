#!/usr/bin/env python3

from src.BiblesGetter import BiblesGetter
from src.BiblesMerger import BiblesMerger
from src.ProjectsGetter import ProjectsGetter
import sys
import os
import logging
import json  
import re


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
    global tag, output, env, log_level, no_merge

    tag = None
    output = None
    env = "www"
    log_level = "INFO"
    no_merge = False

    # Process each argument (skipping the script name at args[0])
    for arg in args[1:]:
        if arg.startswith("--tag="):
            tag = arg.split("=", 1)[1]
        elif arg.startswith("--output="):
            output = arg.split("=", 1)[1]
        elif arg.startswith("--env="):
            env = arg.split("=", 1)[1]
            if env not in ["www", "qa", "local"]:
                env = "www"
        elif arg == "--debug":
            log_level = "DEBUG"
        else:
            print("Unexpected parameter: " + arg)
            sys.exit(1)

    if tag is None or len(tag) == 0:
        print("Tag not specified. Use `--tag=mytag` to specify a tag (use '*' for all projects)")
        sys.exit(1)
        
    # Set default output based on merge behavior
    if output is None or len(output) == 0:
        print("Output not specified. Use `--output=/path/to/folder` to specify where the reports are generated")
        sys.exit(1)


def parse_env_variables(vars):
    global meterian_token
    try:
        meterian_token = vars["METERIAN_API_TOKEN"]
    except KeyError:
        print("Meterian API Token not specified. Export METERIAN_API_TOKEN as environment variable.")
        sys.exit(1)

    if meterian_token is None or len(meterian_token) == 0:
        print("Meterian API Token not specified. Export METERIAN_API_TOKEN as environment variable.")
        sys.exit(1)


def store_bibles(bibles):

    bibles_list = bibles["bibles"]
    for bible in bibles_list:
        name = bible["project"]["name"]
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        
        output_file = os.path.join(output, f"{name}.bible.json")
        with open(output_file, "w") as f:
            json.dump(bible, f, indent=4)
        print(f"Saved bible for project '{name}' to {output_file}")
        
        
def store_reports(bibles_getter, project_uuids):
    if not os.path.exists(output):
        os.makedirs(output)

    count = 0
    for project_uuid in project_uuids:
        count = count + 1
        print(f"Preparing report {count} of {len(project_uuids)}")

        bibles_getter.prepare_bible(project_uuid)

        bible = bibles_getter.get_bible(project_uuid)
        
        name = bible["project"]["name"]
        name = re.sub(r'[<>:"/\\|?*]', '_', name)

        output_file = store_bible_onfs(bible, name)
        output_file = store_cyclonedx_onfs(bibles_getter, project_uuid, name)
        output_file = store_pdfreport_onfs(bibles_getter, project_uuid, name)
        
        print()
        
    print(f"All reports saved to {output}")

def store_cyclonedx_onfs(bibles_getter, project_uuid, name):
    bible = bibles_getter.get_cyclonedx(project_uuid)
    output_file = os.path.join(output, f"{name}.cdx.json")
    with open(output_file, "w") as f:
        json.dump(bible, f, indent=4)

    print(f"Saved cyclonedx report for project '{name}' to {output_file}")
    return output_file

    None
    
def store_pdfreport_onfs(bibles_getter, project_uuid, name):
    output_file = os.path.join(output, f"{name}.pdf")
    bibles_getter.get_pdfreport(project_uuid, output_file)

    print(f"Saved PDF report for project '{name}' to {output_file}")

def store_bible_onfs(bible, name):
    output_file = os.path.join(output, f"{name}.bible.json")
    with open(output_file, "w") as f:
        json.dump(bible, f, indent=4)

    print(f"Saved bible report for project '{name}' to {output_file}")
    return output_file


if __name__ == "__main__":
    print("Meterian - Report Producer")
    parse_env_variables(os.environ)
    parse_args(sys.argv)
    apply_logging_settings()
    print()

    try:
        project_getter = ProjectsGetter(meterian_token, env)
        project_uuids = project_getter.get(tag)
        print(f"Found {len(project_uuids)} projects\n")

        bibles_getter = BiblesGetter(project_getter, meterian_token, env)
        store_reports(bibles_getter, project_uuids)
            
    except Exception as e:
        print(e)
        sys.exit(1)
