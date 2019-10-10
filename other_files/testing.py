from datetime import date

from pymongo import MongoClient

try:
    con = MongoClient()
    db = con["tnp_management"]
    collection_candidate = db["registration_candidate"]
    collection_drive = db["drive_drive"]

    query = {
        "date": str(date.today()),
        "company_name" : "google",
    }

    eligible_companies = collection_drive.find(query)

    c = 0
    for i in eligible_companies:
        for j in i["eligible_student"]:
            c = c + 1
            print(j["_id"])
    print(c)
except Exception as e:
    print(e)

