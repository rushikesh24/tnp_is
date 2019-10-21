import os
import random
import string
from datetime import date
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from pymongo import MongoClient
from xhtml2pdf import pisa


# Drive Upload
@login_required
def drive_upload(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_candidate = db["registration_candidate"]
            collection = db["drive_drive"]

            # ---------Branch--------------
            branch_ls = []
            computer = request.POST.get("Computer")
            if computer == None:
                computer = False
            else:
                computer = True
                branch_ls.append("computer")

            IT = request.POST.get("IT")
            if IT == None:
                IT = False
            else:
                IT = True
                branch_ls.append("information technology")

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
            drive_id = str(request.POST.get("name")).lower() + str(date_ls[0])
            login_key = randomStringDigits()

            round_ls = str(request.POST.get("other")).split(',')
            round_dict = []
            if request.POST.get("round1"):
                round_dict.append({
                    "round_name": request.POST.get("round1"),
                    "round_number": "1"
                })
                if request.POST.get("round2"):
                    round_dict.append({
                        "round_name": request.POST.get("round2"),
                        "round_number": "2"
                    })
                    if request.POST.get("round3"):
                        round_dict.append({
                            "round_name": request.POST.get("round3"),
                            "round_number": "3"
                        })

                        j = 3
                        for i in round_ls:
                            if i:
                                j = j + 1
                                round_dict.append({"round_name": i, "round_number": str(j)})

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
                'company_name': str(request.POST.get("name")).lower(),
                'date': request.POST.get("drive_date"),
                'venue': request.POST.get("place"),
                'time': request.POST.get("drive_time"),
                'rounds': round_dict,
                'login_key': login_key,
                'Computer': computer,
                'Civil': CIVIL,
                'Mechanical': MECH,
                'IT': IT,
                'Instrumentation': INSTRU,
                'Production': PROD,
                'ENTC': ENTC,
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
                print(i)
                companyname.append(i["company_name"])
                cmp = dict(cname=i["company_name"], time=i["time"], location=i["venue"])
                companies.append(cmp)

            print("comapny", companyname)
            return render(request, 'drive/student_list.html',
                          {"id": id, 'name': name, 'branch': branch, 'companies': companies})
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
                    rec = collection_drive.find(
                        {"$and": [{"_id": str(i) + year}, {"round1_student._id": request.POST.get('id')}]})
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


def volunteer_search(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_drive = db["drive_drive"]

            print("Connection established")
            query_company = {
                "login_key": request.POST.get("login_key"),
                "date": str(date.today()),
            }
            round_number = 0
            rec_company = collection_drive.find(query_company)
            for i in rec_company:
                company_name = i["company_name"]
                for j in i['rounds']:
                    round_number = j['round_number']

            round_number_html = int(request.POST.get("rounds"))

            print("round_number", round_number_html)
            if round_number_html <= int(round_number):
                id_ls = []
                candidates = []
                rec_company = collection_drive.find(query_company)
                doc_name = "round" + str(round_number_html) + "_student"
                for i in rec_company:
                    for j in i[doc_name]:
                        id_ls.append(j['_id'])
                        candidate = dict(id=j["_id"], name=j["name"], branch=j["branch"])
                        candidates.append(candidate)
                print("Done")
                return render(request, 'drive/volunteer_update.html',
                              {"company_name": company_name, "candidates": candidates,
                               "round_number": round_number_html, "login_key": request.POST.get("login_key")})

            else:
                return render(request, 'drive/volunteer.html',
                              {"error": "This round is not available for today's company"})
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
                round_name = "round" + str(request.POST.get("round_number")) + "_student"
                next_rounud_name = "round" + str(int(request.POST.get("round_number")) + 1) + "_student"
                next_id = []
                id = []

                company_record = collection_drive.find(query_company)
                print("rounds", round_name, next_rounud_name)
                for i in company_record:
                    for k in i[next_rounud_name]:
                        next_id.append(str(k["_id"]))
                    print("next id ", next_id)
                    for j in i[round_name]:
                        print(j)
                        can_id = str(j["_id"])
                        if can_id not in next_id and request.POST.get(j["_id"]) == 'selected':
                            id.append(can_id)

                print("id list", id)
                if id:
                    company_record = collection_drive.find(query_company)
                    for i in company_record:
                        company_id = i["_id"]
                        print("company id : ", company_id)
                        for j in id:
                            candidate_record = collection_candidate.find({"_id": j})
                            for k in candidate_record:
                                print("candidate id : ", k["_id"])
                                round = "round" + str(int(request.POST.get("round_number")) + 1)
                                round_value = int(k[round]) + 1
                                collection_candidate.update({"_id": k["_id"]}, {"$set": {round: round_value}})
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


candidates = []


@login_required
def company_search(request):
    if request.method == 'POST':
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_drive = db["drive_drive"]

            query_company = {
                "company_name": str(request.POST.get("name")).lower(),
                "date": request.POST.get("drive_date"),
            }

            company_record = collection_drive.find(query_company)
            print("Connection established")

            round_number = 0
            for i in company_record:
                for j in i["rounds"]:
                    round_number = j["round_number"]

            candidate_ls = []
            candidates.clear()
            print('last round : ', round_number)
            company_record = collection_drive.find(query_company)
            for i in company_record:
                print(i)
                for j in i["round" + round_number + "_student"]:
                    candidate_ls.append(dict(id=j["_id"], name=j["name"], branch=j["branch"]))
                    candidates.append(j["_id"])

            print(candidate_ls)
            return render(request, 'drive/placed_details.html',
                          {"candidates": candidate_ls, "company_name": request.POST.get("name"),
                           "drive_date": request.POST.get("drive_date")})
        except Exception as e:
            print("exception", e)
            return HttpResponse('Some error occurred')
    else:
        return render(request, "drive/company_search.html", {})


@login_required
def placed_details(request):
    if request.method:
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_drive = db["drive_drive"]
            collection_candidate = db['registration_candidate']
            query_company = {
                "company_name": str(request.POST.get("company_name")).lower(),
                "date": request.POST.get("drive_date"),
            }

            print("Connection established in placed", query_company)
            company_record = collection_drive.find(query_company)
            placed_ls = []
            for i in company_record:
                for j in i['placed_student']:
                    placed_ls.append(j["_id"])

            print("placed list", placed_ls)
            print("candidates list", candidates)
            company_record = collection_drive.find(query_company)
            error = None
            for i in company_record:
                company_id = i['_id']
                print('company id', company_id)
                for j in candidates:
                    print("candidate list", j)
                    if j not in placed_ls and request.POST.get(j) == 'selected':
                        candidate_record = collection_candidate.find({"_id": j})
                        for k in candidate_record:
                            print("candidate id : ", k["_id"])
                            placed = int(k['placed']) + 1
                            collection_candidate.update({"_id": k["_id"]}, {"$set": {"placed": placed}})
                            collection_drive.update({"_id": company_id}, {"$push": {"placed_student": {
                                '_id': k["_id"],
                                'name': k['name'],
                                'branch': k['branch'] }}
                            })
                        error = 'Data uploaded successfully'
                    else:
                        error = 'Data already uploaded'
            return HttpResponse(error)
            #return render(request, "drive/placed_analysis.html", {})
        except Exception as e:
            print("exception in placed details", e)
            return HttpResponse('Some error occurred')
    else:
        return render(request, "drive/company_search.html", {})

@login_required
def placed_analysis(request) :
    if request.method == "POST":
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_drive = db["drive_drive"]

            query_company = {
                "company_name": str(request.POST.get("name")).lower(),
                "date": request.POST.get("drive_date"),
            }

            print("Connection established")
            company_record = collection_drive.find(query_company)
            round_number = []
            labels = ['Eligible']
            for i in company_record:
                for j in i["rounds"]:
                    print("j in ", j)
                    round_number.append("round"+j["round_number"]+"_student")
                    labels.append("Round "+j["round_number"])
                labels.append('Placed')

            company_record = collection_drive.find(query_company)
            print("round number", round_number)
            sizes = []
            for i in company_record:
                company_name = i['company_name']
                sizes.append(len(i["eligible_student"]))
                for j in round_number:
                    print(j)
                    sizes.append(len(i[j]))
                sizes.append(len(i["placed_student"]))

            index = np.arange(len(labels))
            plt.bar(index, sizes)
            plt.xlabel('Rounds', fontsize=7)
            plt.ylabel('No of Students', fontsize=15)
            plt.xticks(index, labels, fontsize=7, rotation=30)
            plt.title("Analysis of Placed Students in as per company")
            plt.title('Students Placed In ' + company_name)
            plt.savefig('static/drive/graphs/result_round.png')
            plt.close()
            return render(request, 'drive/placed_graph.html', {"company_name": request.POST.get("name")})
        except Exception as e:
            print({"exception": e})  # Console log
            return render(request, 'drive/placed_analysis.html', {"error": "Connection Failed"})
    else:
        return render(request, 'drive/placed_analysis.html', {})

@login_required
def college_analysis(request) :
    if request.method == "POST":
        try:
            con = MongoClient()
            db = con["tnp_management"]
            collection_drive = db["drive_drive"]
            collection_candidate = db["registration_candidate"]

            query_company = {
                "company_name": str(request.POST.get("name")).lower(),
                "date": request.POST.get("drive_date"),
            }

            query_candidate = {
                'college_name' : request.POST.get('clgname')
            }

            dypcoe = 0
            dypiemr = 0
            record_drive = collection_drive.find(query_company)
            cmp = []
            for x in record_drive:
                cmp.append(x)
            cmp = cmp[0]
            students = cmp['placed_student']
            colleges = []
            for x in students:
                college = collection_candidate.find({'_id': x['_id']})

                cmp = []
                for x in college:
                    cmp.append(x)
                cmp = cmp[0]

                colleges.append(cmp)
            for college in colleges:
                if college['college_name'] == 'dypcoe':
                    dypcoe += 1
                elif college['college_name'] == 'dypiemr':
                    dypiemr += 1
            print("dypcoe = "+ str(dypcoe))
            print("dypiemr = " + str(dypiemr))


           # print(int(str(total_placed_candidate_dypcoe)) , int(str(total_placed_candidate_dypcoe)))
            labels = ["DYPCOE = {}".format(dypcoe), "DYPIEMR = {}".format(dypiemr)]

            #fig1, ax1 = plt.subplots()
            plt.pie([dypcoe, dypiemr],  labels=labels, shadow=True, startangle = 90)
            plt.title("Analysis Report as per the College")
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.savefig('static/drive/graphs/result_college.png')
            plt.close()
            #return HttpResponse("done")
            return render(request, 'drive/college_graph.html', {"company_name": request.POST.get("name")})
        except Exception as e:
            print({"exception": e})  # Console log
            return render(request, 'drive/college_analysis.html', {"error": "Connection Failed"})
    else:
        return render(request, 'drive/college_analysis.html', {})


@login_required
def total_analysis(request):
    try:
        client = MongoClient()
        db = client['tnp_management']
        collection_drive = db['drive_drive']
        collection_student = db['registration_candidate']

        total_companies = 0
        record_drive = collection_drive.find()
        for i in record_drive:
            total_companies += 1

        total_eligible_candidates = 0
        total_placed_candidates = 0

        record_candidate = collection_student.find()
        for i in record_candidate:
            if int(i["eligible"]) > 0:
                total_eligible_candidates += 1
            if int(i["placed"]) > 0:
                total_placed_candidates += 1

        fig1, ax1 = plt.subplots()
        ax1.pie([total_eligible_candidates, total_placed_candidates],
                labels=["Eligible (" + str(total_eligible_candidates) + ")",
                        "Placed (" + str(total_placed_candidates) + ")"],
                shadow=True, startangle=90)
        plt.title("Analysis of Total Students - Eligible and Placed")
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig('static/drive/graphs/result_total_analysis.png')
        plt.close(fig1)
        return render(request, 'drive/total_graph.html', {})
    except Exception as e:
        print("exception", e)
        return HttpResponse("Error occurred")


@login_required
def company_analysis(request):
    try:
        client = MongoClient()
        db = client['tnp_management']
        collection_drive = db['drive_drive']

        total_companies = 0
        companies = dict(computer=0, it=0, entc=0, production=0, instrumentation=0, civil=0, mechanical=0)
        record_drive = collection_drive.find()
        for i in record_drive:
            total_companies += 1
            if i["Computer"]:
                companies['computer'] += 1
            if i["Civil"]:
                companies['civil'] += 1
            if i["ENTC"]:
                companies['entc'] +=1
            if i["IT"]:
                companies['it'] += 1
            if i["Instrumentation"]:
                companies['instrumentation'] +=1
            if i["Mechanical"]:
                companies['mechanical'] += 1
            if i["Production"]:
                companies['production'] += 1

        print(list(companies.values()), list(companies))
        companies_ls = list(companies)
        it = companies_ls.index("it")
        entc = companies_ls.index("entc")

        if it >= 0:
            companies_ls[it] = "IT"
        if entc >= 0:
            companies_ls[entc] = 'E&TC'

        index = np.arange(len(list(companies_ls)))
        plt.bar(index, list(companies.values()))
        plt.xlabel('Departments', fontsize=7)
        plt.ylabel('No of Students', fontsize=15)
        plt.xticks(index, (list(companies_ls)), fontsize=7)
        plt.title('Students Placed Branch wise')

        plt.savefig('static/drive/graphs/result_company_analysis.png')
        plt.close()
        return render(request,'drive/company_graph.html',{})
    except Exception as e:
        print("exception", e)
        return HttpResponse("Error occurred")
#----------------------------------------------------------------------------------

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    print("callback")
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=link_callback)
    if not pdf.err:
        print("Successful")
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        print("Unuccessful")
        return None



def report_pdf(request):
    if request.method == "POST":
        try:
            client = MongoClient()
            db = client['tnp_management']
            collection_drive = db['drive_drive']

            query = {
                "company_name":request.POST.get("name").lower(),
                "date" : request.POST.get("drive_date"),
            }

            company_cur = collection_drive.find(query)
            company = {}
            for i in company_cur:
                company = i

            company_name = company['company_name'].upper()
            drive_date = company['date']
            year = drive_date.split("-")[0]
            criteria = "10th : " + str(company['eligibility'][0]['tenth_marks']) + ", 12th or Diploma : "+ str(company['eligibility'][0]['diploma_12']) + ", Engineering : " + str(company['eligibility'][0]['engineering'])
            today_date =  str(date.today())
            branch_ls = []
            if company['Computer']:
                branch_ls.append("Computer")
            if company['Civil']:
                branch_ls.append("Civil")
            if company['Mechanical']:
                branch_ls.append("Mechanical")
            if company['IT']:
                branch_ls.append("IT")
            if company['Instrumentation']:
                branch_ls.append("Instrumentation")
            if company['Production']:
                branch_ls.append("Production")
            if company['ENTC']:
                branch_ls.append("E&TC")

            branches = ""
            for i in branch_ls:
                branches = branches + i + "/"
            branches = branches[:-1]

            total_row = ['Total']
            comp_ls =['computer']
            it_ls = ['Information Technology']
            civil_ls = ['civil']
            mech_ls = ['Mechanical']
            prod_ls = ['Production']
            instru_ls = ["Instrumentation"]
            entc_ls = ['E&TC']

            #eligiblity count

            comp = it = civil = mech = prod = instru = entc = 0
            for j in company['eligible_student']:
                if j['branch'] == "computer":
                    comp = comp + 1
                if j['branch'] == "information technology":
                    it = it + 1
                if j['branch'] == "entc":
                    entc = entc + 1
                if j['branch'] == "mechanical engineering":
                    mech = mech + 1
                if j['branch'] == "civil engineering":
                    civil = civil + 1
                if j['branch'] == "production engineering":
                    prod = prod + 1
                if j['branch'] == "instrumentation engineering":
                    instru = instru + 1
            total_row.append(comp + it + civil + mech + prod + instru + entc)


            comp_ls.append(comp)
            it_ls.append(it)
            civil_ls.append(civil)
            mech_ls.append(mech)
            prod_ls.append(prod)
            instru_ls.append(instru)
            entc_ls.append(entc)

            #round count
            procedure = ""
            rounds = []
            for i in company['rounds']:
                procedure = procedure + i['round_name'] +"/"
                rounds.append(i['round_name'])
                attr_name = "round"+i['round_number']+"_student"
                comp = it = civil = mech = prod = instru = entc = 0
                for j in company[attr_name]:
                    if j['branch'] == "computer":
                        comp = comp + 1
                    if j['branch'] == "information technology" or j['branch'] == 'information' :
                        it = it + 1
                    if j['branch'] == "entc":
                        entc = entc + 1
                    if j['branch'] == "mechanical engineering":
                        mech = mech + 1
                    if j['branch'] == "civil engineering":
                        civil = civil + 1
                    if j['branch'] == "production engineering":
                        prod = prod + 1
                    if j['branch'] == "instrumentation engineering":
                        instru = instru + 1

                comp_ls.append(comp)
                it_ls.append(it)
                civil_ls.append(civil)
                mech_ls.append(mech)
                prod_ls.append(prod)
                instru_ls.append(instru)
                entc_ls.append(entc)
                total_row.append(comp + it + civil + mech + prod + instru + entc)

            #placed count
            comp = it = civil = mech = prod = instru = entc = 0
            for j in company['placed_student']:
                if j['branch'] == "computer":
                    comp = comp + 1
                if j['branch'] == "information technology":
                    it = it + 1
                if j['branch'] == "entc":
                    entc = entc + 1
                if j['branch'] == "mechanical engineering":
                    mech = mech + 1
                if j['branch'] == "civil engineering":
                    civil = civil + 1
                if j['branch'] == "production engineering":
                    prod = prod + 1
                if j['branch'] == "instrumentation engineering":
                    instru = instru + 1
            total_row.append(comp + it + civil + mech + prod + instru + entc)
            comp_ls.append(comp)
            it_ls.append(it)
            civil_ls.append(civil)
            mech_ls.append(mech)
            prod_ls.append(prod)
            instru_ls.append(instru)
            entc_ls.append(entc)

            # absent data
            comp = comp_ls[1]-comp_ls[2]
            it = it_ls[1]-it_ls[2]
            civil = civil_ls[1]-civil_ls[2]
            mech = mech_ls[1]-mech_ls[2]
            prod = prod_ls[1]-prod_ls[2]
            instru = instru_ls[1]-instru_ls[2]
            entc = entc_ls[1]-entc_ls[2]

            comp_ls.append(comp)
            it_ls.append(it)
            civil_ls.append(civil)
            mech_ls.append(mech)
            prod_ls.append(prod)
            instru_ls.append(instru)
            entc_ls.append(entc)
            total_row.append(comp + it + civil + mech + prod + instru + entc)

            branc_wise_data = []
            if comp_ls[1] > 0:
                branc_wise_data.append(comp_ls)
            if it_ls[1] > 0:
                branc_wise_data.append(it_ls)
            if civil_ls[1] > 0:
                branc_wise_data.append(civil_ls)
            if mech_ls[1] > 0:
                branc_wise_data.append(mech_ls)
            if prod_ls[1] > 0:
                branc_wise_data.append(prod_ls)
            if instru_ls[1] > 0:
                branc_wise_data.append(instru_ls)
            if entc_ls[1] > 0:
                branc_wise_data.append(entc_ls)
            procedure = procedure[:-1]

            total_candidate = len(company["round1_student"])
            placed_candidate = len(company["placed_student"])



            data = {
                "today_date": today_date,
                "company_name": company_name,
                "date": drive_date,
                "year": year,
                "branches": branches,
                "criteria": criteria,
                "procedure": procedure,
                "total_candidate": total_candidate,
                "placed_candidate": placed_candidate,
                "branch_wise_data": branc_wise_data,
                "rounds": rounds,
                "total_row": total_row
            }

            print(data)
            pdf = render_to_pdf('drive/report_pdf.html', data)
            return HttpResponse(pdf,content_type='application/pdf')

        except Exception as e:
            print("exception", e)
            return HttpResponse("Error occurred")
    else:
        return render(request, 'drive/pdf_report_generate.html', {})