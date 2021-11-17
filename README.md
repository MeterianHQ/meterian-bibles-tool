# Meterian Bibles Merger Tool

Use this script to generate a licenses bible, in JSON format, comprehensive of all the bibles of all the projects bound to a tag.

## How to use

First of all run `pipenv install --python 3` to setup the virtual environment.
**This script only works with python3**

Then launch the generator `pipenv run python generate_bible.py [Options]`

## The script option
|Option|Required|Description|
|------|--------|-----------|
|`--tag=$TAG_NAME` | **Yes** | Specify the tag to which all the projects are bound |
|`--meterian-token=$METERIAN_API_TOKEN` | **Yes** | Specify the Meterian API Token to use |
|`--output=/path/to/bible.json` | No | Specify the path where the bible json should be generated. If not specified the file will be generated under /tmp |

## Output

The output file presents two sections:
- _status
- components

The `_status` field indicates whether all the bibles were processed. 
`"_status": "ok"` indicates that all the bibles were generated.
`"_status": "partial"` indicates that the script was not able to process one or more bibles

The `components` field contains all the components, with respective liceses, categorized by language.
