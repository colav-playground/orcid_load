import glob
import xmltodict
from pymongo import MongoClient
from joblib import Parallel, delayed

orcid_summaries_path = "/storage/orcid/ORCID_2024_10_summaries/"
db_name = "orcid"
col_name = "summaries"
col_name_locked = "summaries_locked"
jobs=72


db = MongoClient()[db_name]
col = db[col_name]
col_locked = db[col_name_locked]
summaries = glob.glob(orcid_summaries_path + "/*/*.xml")

print("INFO: processing {} files from {}".format(len(summaries),orcid_summaries_path))

def get_xml_data(file):
    f = open(file)
    data = f.read()
    f.close()
    return data


def parse_xmltodict(file):
    data = get_xml_data(file)
    return xmltodict.parse(data)


def process_one(col, file):
    data = parse_xmltodict(file)
    if 'record:record' in data:
        del data['record:record']['activities:activities-summary'] # produces "BSON document too large" in MongoDB
        col.insert_one(data)
    else:
        print("WARNING: 'record:record' not found, probably locked")
        col_locked.insert_one(data)


Parallel(n_jobs=jobs, verbose=10, backend="threading")(
    delayed(process_one)(col, file) for file in summaries
)
col.create_index("record:record.common:orcid-identifier.common:uri")
