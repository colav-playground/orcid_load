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

# Download ORCID data

go to https://info.orcid.org/documentation/integration-guide/working-with-bulk-data/

select the year of the data example: https://orcid.figshare.com/articles/dataset/ORCID_Public_Data_File_2024/27151305/1

download the zip file and extract the contents to a folder
you will see files like 
```
ORCID_2024_10_activities_3.tar.gz  ORCID_2024_10_activities_7.tar.gz  
ORCID_2024_10_activities_0.tar.gz  ORCID_2024_10_activities_4.tar.gz  ORCID_2024_10_activities_8.tar.gz  ORCID_2024_10_summaries.tar.gz
ORCID_2024_10_activities_1.tar.gz  ORCID_2024_10_activities_5.tar.gz  ORCID_2024_10_activities_9.tar.gz  orcid_2024.zip
ORCID_2024_10_activities_2.tar.gz  ORCID_2024_10_activities_6.tar.gz  ORCID_2024_10_activities_X.tar.gz  
```

extract the summaries file ORCID_2024_10_summaries.tar.gz

```
tar -xvf ORCID_2024_10_summaries.tar.gz
```

This is the information required to load the data in MongoDB from authors.
