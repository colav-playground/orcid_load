from kahi_impactu_utils.Utils import get_id_from_url
from pymongo import MongoClient

# Database configuration
db_uri = "mongodb://localhost:27017/"
dbclient = MongoClient(db_uri)

# Databases
orcid_db = dbclient["orcid"]
openalexco = dbclient["openalexco"]
scienti_dbs = [
    dbclient["scienti_udea_2024"],
    dbclient["scienti_uec_2024"],
    dbclient["scienti_unaula_2024"],
    dbclient["scienti_univalle_2024"]
]
yuku = dbclient["yuku"]


def normalize_orcid(raw: str) -> str | None:
    """Normalizes a raw ORCID string to its full HTTPS format."""
    if not raw:
        return None
    if "orcid" in raw:
        return get_id_from_url(raw)
    return get_id_from_url(f"https://orcid.org/{raw}")


def get_orcids_from_scienti(dbs) -> set:
    """Extracts unique ORCID identifiers from multiple Scienti databases."""
    result = set()
    for db in dbs:
        raw_list = db["product"].distinct("author.COD_ORCID", {"author.COD_ORCID": {"$ne": None}})
        for raw in raw_list:
            normalized = normalize_orcid(raw)
            if normalized:
                result.add(normalized)
    return result


def get_orcids_from_minciencias() -> set:
    """Extracts ORCID identifiers from the CVLAC records in Minciencias."""
    field = "red_identificadores.Open Researcher and Contributor ID (ORCID)"
    raw_list = yuku["cvlac_stage"].distinct(field, {field: {"$ne": None}})
    return {normalize_orcid(r) for r in raw_list if normalize_orcid(r)}


def get_orcids_from_openalex() -> set:
    """Extracts ORCID identifiers from OpenAlex using an aggregation pipeline."""
    pipeline = [
        {"$match": {"ids.orcid": {"$exists": True}}},
        {"$group": {"_id": "$ids.orcid"}}
    ]
    return {doc["_id"] for doc in openalexco["authors"].aggregate(pipeline)}


def sync_orcid_records(orcids: set):
    """Copies ORCID records from the 'orcid' database into 'orcidco' if not already present."""
    dest_col = dbclient["orcidco_test"]["summaries"]
    src_col = orcid_db["summaries"]

    for orcid_id in orcids:
        if not dest_col.find_one({"record:record.common:orcid-identifier.common:uri": orcid_id}):
            record = src_col.find_one({"record:record.common:orcid-identifier.common:uri": orcid_id})
            if record:
                dest_col.insert_one(record)


def main():
    orcids = set()
    orcids.update(get_orcids_from_openalex())
    orcids.update(get_orcids_from_scienti(scienti_dbs))
    orcids.update(get_orcids_from_minciencias())

    print(f"Total unique ORCIDs found: {len(orcids)}")
    sync_orcid_records(orcids)
    print("ORCID records synced successfully.")


if __name__ == "__main__":
    main()
