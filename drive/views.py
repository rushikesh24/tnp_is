import math
import random
import string
from datetime import date

import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required
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

            #---------Branch--------------
            branch_ls = []
            Computer = request.POST.get("Computer")
            if Computer == None:
                Computer = False
            else:
                Computer = True
                branch_ls.append("computer")

            IT = request.POST.get("IT")
            if IT == None:
                IT = False
            else:
                IT = True
                branch_ls.append("it")

            CIVIL = request.POST.get("CIVIL")
            if CIVIL == None:
                CIVIL = False
            else:
                CIVIL = True
                branch_ls.append("civil")

            MECH = request.POST.get("MECH")
            if MECH == None:
                MECH = False
            else:
                MECH = True
                branch_ls.append("mechanical")

            INSTRU = request.POST.get("INSTRU")
            if INSTRU == None:
                INSTRU = False
            else:
                INSTRU = True
                branch_ls.append("instrumentation")

            PROD = request.POST.get("PROD")
            if PROD == None:
                PROD = False
            else:
                PROD = True
                branch_ls.append("production")

            ENTC = request.POST.get("ENTC")
            if ENTC == None:
                ENTC = False
            else:
                ENTC = True
                branch_ls.append("entc")

            date_ls = str(request.POST.get("drive_date")).split("-")
            drive_id = str(request.POST.get("name")) + str(date_ls[0])
            login_key = randomStringDigits()

            round_ls = str(request.POST.get("other")).split(',')
            round_dict = []
            if request.POST.get("round1"):
                round_dict.append({
                    "round_name": request.POST.get("round1"),
                    "round_number" : "1"
                })
                if request.POST.get("round2"):
                    round_dict.append({
                        "round_name": request.POST.get("round2"),
                        "round_number" : "2"
                    })
                    if request.POST.get("round3"):
                        round_dict.append({
                            "round_name": request.POST.get("round3"),
                            "round_number" : "3"
                        })

                        j = 3
                        for i in round_ls:
                            if i :
                                j = j + 1
                                round_dict.append({"round_name": i, "round_number" : str(j)})

            eligible_student = []
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
                'Computer' : Computer,
                'Civil' : CIVIL,
                'Mechanical' : MECH,
                'IT' : IT,
                'Instrumentation' : INSTRU,
                'Production' : PROD,
                'ENTC' : ENTC,
                'eligibility': [{
                    'tenth_marks': request.POST.get("tenth"),
                    'diploma_12': request.POST.get("diploma_12"),
                    'engineering': request.POST.get("engineering"),
                }],
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

            print("comapny",companyname)
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
                    flag = True

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


def volunteer_search(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_drive = db["drive_drive"]

            print("Connection established")
            query_company = {
                "login_key": request.POST.get("login_key"),
                "date" : str(date.today()),
            }
            round_number = 0
            rec_company = collection_drive.find(query_company)
            for i in rec_company:
                company_name = i["company_name"]
                for j in i['rounds']:
                    round_number = j['round_number']

            round_number_html = int(request.POST.get("rounds"))

            print("round_number",round_number_html)
            if round_number_html <= int(round_number):
                id_ls = []
                candidates = []
                rec_company = collection_drive.find(query_company)
                doc_name = "round"+str(round_number_html)+"_student"
                for i in rec_company:
                    for j in i[doc_name]:
                        id_ls.append(j['_id'])
                        candidate = dict(id=j["_id"], name=j["name"], branch=j["branch"])
                        candidates.append(candidate)
                print("Done")
                return render(request, 'drive/volunteer_update.html',
                                  {"company_name": company_name, "candidates": candidates,"round_number" : round_number_html,"login_key": request.POST.get("login_key")})

            else:
                return render(request, 'drive/volunteer.html', {"error": "This round is not available for today's company"})
        except Exception as e:
            print(e)
            return render(request, 'drive/volunteer.html', {"error": 'Company not found'})

    else:
        return render(request, 'drive/volunteer.html', {})


def volunteer_update(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_drive = db["drive_drive"]
            collection_candidate = db["registration_candidate"]

            query_company = {
                "login_key": request.POST.get("login_key"),
                "date": str(date.today()),
            }

            print("Connection established")
            company_record = collection_drive.find(query_company)

            round_number = 0
            for i in company_record:
                for j in i["rounds"]:
                    round_number = int(j["round_number"])

            if round_number > int(request.POST.get("round_number")):

                round_name = "round"+str(request.POST.get("round_number"))+"_student"
                next_rounud_name = "round" + str(int(request.POST.get("round_number")) + 1) + "_student"
                next_id = []
                id = []

                company_record = collection_drive.find(query_company)
                print("rounds",round_name,next_rounud_name)
                for i in company_record:
                    for k in i[next_rounud_name]:
                        next_id.append(str(k["_id"]))
                    print("next id " ,next_id)
                    for j in i[round_name]:
                        print(j)
                        can_id = str(j["_id"])
                        if can_id not in next_id and request.POST.get(j["_id"]) == 'selected':
                            id.append(can_id)

                print("id list" , id)
                if id:
                    company_record = collection_drive.find(query_company)
                    for i in company_record:
                        company_id = i["_id"]
                        print("company id : ",company_id)
                        for j in id:
                            candidate_record = collection_candidate.find({"_id" : j})
                            for k in candidate_record:
                                print("candidate id : ",k["_id"])
                                round = "round"+str(int(request.POST.get("round_number"))+1)
                                round_value = int(k[round]) + 1
                                collection_candidate.update({"_id": k["_id"]}, {"$set": { round: round_value}})
                                collection_drive.update({"_id": company_id}, {"$push": {next_rounud_name: {
                                    '_id': k["_id"],
                                    'name': k['name'],
                                    'branch': k['branch'], }}
                                })
                    return HttpResponse("Data Successfully updated")
                else:
                    return HttpResponse("Data already uploaded")
            else:
                return HttpResponse('You cannot access last round details')
        except Exception as e:
            print(e)
            return HttpResponse('Some error occurred')
    else:
        return render(request, 'drive/volunteer_update.html', {})

@login_required
def company_search(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_drive = db["drive_drive"]

            query_company = {
                "company_name" : request.POST.get("name") ,
                "date": request.POST.get("drive_date") ,
            }

            company_record = collection_drive.find(query_company)
            print("Connection established")

            round_number = 0
            for i in company_record:
                for j in i["rounds"]:
                    round_number = j["round_number"]

            candidate_ls = []
            print('last round : ',round_number)
            company_record = collection_drive.find(query_company)
            for i in company_record:
                print(i)
                for j in i["round"+round_number+"_student"]:
                    candidate_ls.append(dict(id=j["_id"],name=j["name"],branch=j["branch"]))

            print(candidate_ls)
            return render(request,'drive/placed_details.html',{"candidates" : candidate_ls,"company_name" : request.POST.get("name")})
        except Exception as e:
            print("exception",e)
            return HttpResponse('Some error occurred')
    else:
        return render(request,"drive/company_search.html",{})

@login_required
def placed_details(request):

    return HttpResponse("You are on placed")


