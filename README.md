# Meterian Bibles Tools

## Two scripts to batch generate reports
Use these scripts to manage an aggregate bible and other reports from your projects in Meterian:

1. **generate_bible** can generate a licenses bible, in JSON format, comprehensive of all the bibles of all the projects bound to a tag.
2. **produce_reports** can generate a number of reports (PDF, CDX/JSON and bible/JSON) of all the projects bound to a tag. 

## You will need a token to use this tool!

This tool will require an API token from Meterian. This is available for any paid plan, and it can be generated from the "Tokens" tab at https://meterian.com/dashboard. Once you have the token, the best and secure way to use it is to put it into an environment variable, called METERIAN_API_TOKEN. In linux, for example, you can simply do something like this:

    export METERIAN_API_TOKEN=a902874d-50f2-464f-8707-780cd5f669a3
(no, this is not a real token eheh!)


## How to use the 'generate_bible' script

First of all run `pipenv install --python 3` to setup the virtual environment.
**This script only works with python3**

Then launch the generator `pipenv run python generate_bible.py [Options]`

### The script option
|Option|Required|Description|
|------|--------|-----------|
|`--tag=your-tag-name` | **Yes** | Specify the tag to which all the projects are bound |
|`--output=/path/to/bible.json` | No | Specify the path where the bible JSON file should be generated. If not specified the file will be generated under /tmp |
|`--debug` | No | Set the log level to DEBUG |

### Output

The output is a single JSON file presenting these sections:
- the `_status` field indicates whether all the bibles were processed. 
`"_status": "ok"` indicates that all the bibles were processed correctly
`"_status": "partial"` indicates that the script was not able to process one or more bibles

- the `components` section contains all the components, with respective licenses, categorized by language.

- the `licenses` section contains all the licenses listed in all the processed bibles.

## How to use the 'produce_reports' script

First of all run `pipenv install --python 3` to setup the virtual environment.
**This script only works with python3**

Then launch the generator `pipenv run python generate_bible.py [Options]`

### The script option
|Option|Required|Description|
|------|--------|-----------|
|`--tag=your-tag-name` | **Yes** | Specify the tag to which all the projects are bound ('*' means all projects) |
|`--output=/path/to/folder` | **Yes** | Specify the folder where the reports should be generated.|
|`--no-overwrite` | No | If specified the system will skip when a bible report is already present in the folder.|
|`--debug` | No | Set the log level to DEBUG |

### Output

The folder will present three files for each project:
- the Meterian bible report in JSON format, ending with '.bible.json"
- the Meterian project report in PDF format, ending with '.pdf"
- the CycloneDX report in JSON format, ending with '.cdx.json"
