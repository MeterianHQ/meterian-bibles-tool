# Tool to lookup details among reports of a Meterian account

# Usage example

`pipenv run python search_in_projects.py --key=security.locations --value=.ipynb --env=qa --domain=meterian.com --output=$(pwd)/../qa.notebooks.json --languages=python`


- key indicates a set of keys to look for in the report. The last key is the one that will be used to collect data. The other values are used to indicate where in the report to look for the data.
- value indicates the value to use to filter the results of the lookup. If no value is specified, then all the results will be returned.
- output is used to specify the output file. 
- languages is used to specify a list of comma separated languages to consider in the lookup. If no languages are specified, then all the languages will be used. 

- use `METERIAN_API_TOKEN` to specify the Authorization Bearer. This script will not work with authentication tokens.