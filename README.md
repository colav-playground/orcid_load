# orcid_load
scripts to load ORCID in MongoDB

# install dependencies with 
pip install xmltodict joblib pymongo


edit load.py to set the path to the ORCID data files and the MongoDB connection string

run with
``` 
python load.py
``` 

NOTE:

* checkpoint is not supported yet
* we are only loading the summaries (authors information) not works.
* if something fails pelase start again from the beginning
* the index "record:record.common:orcid-identifier.common:uri" is created to speed up the queries search with orcid with full url ex: https://orcid.org/0000-0002-1825-0097
