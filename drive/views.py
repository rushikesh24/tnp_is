import math
import random
import string
from datetime import date

import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient


# Drive Upload
def drive_upload(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_candidate = db["registration_candidate"]
            collection = db["drive_drive"]

            date_ls = str(request.POST.get("drive_date")).split("-")
            drive_id = str(request.POST.get("name")) + str(date_ls[0])
            login_key = randomStringDigits()

            round_ls = str(request.POST.get("other")).split(',')
            round_dict = {}
            if request.POST.get("round1"):
                round_dict.update({
                    "round1": request.POST.get("round1"),
                })
                if request.POST.get("round2"):
                    round_dict.update({
                        "round2": request.POST.get("round2"),
                    })
                    if request.POST.get("round3"):
                        round_dict.update({
                            "round3": request.POST.get("round3"),
                        })

                        j = 3
                        for i in round_ls:
                            if i :
                                j = j + 1
                                round_name = "round" + str(j)
                                round_dict.update({round_name: i})

            eligible_student = []
            branch_ls = str(request.POST.get("branch")).split(',')
            print(branch_ls)
            query = {
                "tenth": {"$gte": request.POST.get('tenth')},
                "diploma_12": {"$gte": request.POST.get("diploma_12")},
                "engineering": {"$gte": request.POST.get("engineering")},
                "branch": {"$in": branch_ls},
            }

            student_details = collection_candidate.find(query)
            for i in student_details:
                print(i)
                id = i["_id"]
                name = i["name"]
                branch = i["branch"]
                eligible = int(i["eligible"]) + 1
                collection_candidate.update({"_id": id}, {"$set": {"eligible": eligible}})
                student_temp = {"_id": id, "name": name, "branch": branch}
                eligible_student.append(student_temp)

            drive_dic = {
                '_id': drive_id,
                'company_name': request.POST.get("name"),
                'date': request.POST.get("drive_date"),
                'venue': request.POST.get("place"),
                'time': request.POST.get("drive_time"),
                'rounds': round_dict,
                'login_key': login_key,
                'branch': request.POST.get("branch"),
                'eligibility': {
                    'tenth_marks': request.POST.get("tenth"),
                    'diploma_12': request.POST.get("diploma_12"),
                    'enggineering': request.POST.get("engineering"),
                },
                'base_package': request.POST.get("package"),
                'campus_type': request.POST.get("campus"),
                'eligible_student': eligible_student,
                "round1_student": [],
                "round2_student": [],
                "round3_student": [],
                "round4_student": [],
                "round5_student": [],
                "round6_student": [],
                "round7_student": [],
                "round8_student": [],
                "placed_student": [],
            }
            rec = collection.insert_one(drive_dic)
            print(rec)
            return render(request, 'drive/round_details.html', {'login_key': login_key, })
        except Exception as e:
            print(e)
            return render(request, 'drive/drive_upload.html', {"error": "Drive_id number is already registered"})
    else:
        return render(request, 'drive/drive_upload.html', {})


def randomStringDigits(stringLength=8):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


companyname = []



def student_attendence(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_candidate = db["registration_candidate"]
            collection_drive = db["drive_drive"]

            query_student = {"_id": request.POST.get('pnr'), }

            student_information = collection_candidate.find(query_student)

            query = {
                "date": str(date.today()),
                "eligible_student._id": request.POST.get('pnr'),
            }

            eligible_companies = collection_drive.find(query)

            id = request.POST.get('pnr')
            name = None
            branch = None

            for i in student_information:
                name = i["name"]
                branch = i["branch"]

            companyname.clear()
            companies = []

            for i in eligible_companies:
                companyname.append(i["company_name"])
                cmp = dict(cname=i["company_name"], time=i["time"], location=i["venue"])
                companies.append(cmp)
            return render(request, 'drive/student_list.html',
                          {"id": id, 'name': name, 'branch': branch, 'companies': companies })
        except Exception as e:
            print(e)
            return render(request, 'drive/student_attendance.html', {"error": 'Some error occured'})

    else:
        return render(request, 'drive/student_attendance.html', {})


def student_list(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_drive = db["drive_drive"]
            collection_candidate = db["registration_candidate"]

        except Exception as e:
            print({"exception": e})  # Console log
            return render(request, 'drive/student_list.html', {"error": "Connection Failed"})

        try:
            print("Connection established")

            date_ls = str(date.today()).split("-")
            year = str(date_ls[0])
            j = 0

            print(companyname)
            for i in companyname:
                print(i, request.POST.get(str(i)))
                if request.POST.get(str(i)) == 'Yes':
                    rec = collection_drive.find({"$and" : [{"_id": str(i) + year},{"round1_student._id" : request.POST.get('id')}]})
                    flag  = True

                    for i in rec:
                        flag = False
                        break

                    if flag:
                        collection_drive.update({"_id": str(i) + year}, {"$push": {"round1_student": {
                            '_id': request.POST.get('id'),
                            'name': request.POST.get('name'),
                            'branch': request.POST.get('branch'), }}
                        })
                        j = j + 1
                        student_records = collection_candidate.find({"_id": request.POST.get('id')})
                        for i in student_records:
                            print(i)
                            id = i["_id"]
                            round1 = int(i["round1"]) + j
                            collection_candidate.update({"_id": id}, {"$set": {"round1": round1}})

                        return HttpResponse("Congratulations.....You are in!!")
                    else:
                        return HttpResponse("You are already added to list")
        except Exception as e:
            print({"exception": e})
            return render(request, 'drive/student_list.html', {"error": 'Some error occured'})

    else:
        return render(request, 'drive/student_list.html', {})



def report_generation_placed(request):
    try:
        con = MongoClient()
        db = con["tnp_management"]
        collection_candidate = db["registration_candidate"]

    except Exception as e:
        print({"exception": e})  # Console log
        return render(request, 'drive/student_list.html', {"error": "Connection Failed"})

    eligible = []
    round1 = []
    round2 = []
    round3 = []
    round4 = []
    round5 = []
    round6 = []
    round7 = []
    round8 = []
    placed = []
    student_details = collection_candidate.find()
    for i in student_details:
        print(i)
        eligible.append(int(i["eligible"]))
        round1.append(int(i["round1"]))
        round2.append(int(i["round2"]))
        round3.append(int(i["round3"]))
        round4.append(int(i["round4"]))
        round5.append(int(i["round5"]))
        round6.append(int(i["round6"]))
        round7.append(int(i["round7"]))
        round8.append(int(i["round8"]))
        placed.append(int(i["placed"]))

    plt.hist([eligible, placed], bins=round(1 + 3.322 * math.log(len(eligible))), label=['Eligible', 'Placed'])
    plt.savefig('templates/drive/graphs/result.png')

    return HttpResponse("200")
