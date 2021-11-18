# Meterian Bibles Merger Tool

Use this script to generate a licenses bible, in JSON format, comprehensive of all the bibles of all the projects bound to a tag.

## You will need a token to use these tools!

This tool will require an API token from Meterian. This is available for any paid plan, and it can be generated from the "Tokens" tab at https://meterian.com/dashboard 

Once you have the token, the best and secure way to use it is to put it into an environment variable, called METERIAN_API_TOKEN. In linux, for example, you can simply do something like this:

    export METERIAN_API_TOKEN=a902874d-50f2-464f-8707-780cd5f669a3
(no, this is not a real token eheh!)


## How to use

First of all run `pipenv install --python 3` to setup the virtual environment.
**This script only works with python3**

Then launch the generator `pipenv run python generate_bible.py [Options]`

## The script option
|Option|Required|Description|
|------|--------|-----------|
|`--tag=$TAG_NAME` | **Yes** | Specify the tag to which all the projects are bound |
|`--output=/path/to/bible.json` | No | Specify the path where the bible json should be generated. If not specified the file will be generated under /tmp |
|`--debug` | No | Set the log level to DEBUG |

## Output

The output file presents two sections:
- _status
- components
- licenses

The `_status` field indicates whether all the bibles were processed. 
`"_status": "ok"` indicates that all the bibles were processed correctly
`"_status": "partial"` indicates that the script was not able to process one or more bibles

The `components` section contains all the components, with respective licenses, categorized by language.

The `licenses` section contains all the licenses listed in all the processed bibles.
