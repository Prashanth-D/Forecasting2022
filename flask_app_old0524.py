# -*- coding: utf-8 -*-
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template, request
import xlrd, pandas, os, sqlite3, json
from collections import defaultdict
import numpy as np
from flask import request
from decimal import Decimal

app = Flask(__name__)
pandas.option_context('display.max_rows', None, 'display.max_columns', None)
DATABASE = 'K_ghi.db'
mapping = {2: "TB", 3: "Malaria", 4: "HIV", 5: "Roundworm", 6: "Hookworm", 7: "Whipworm", 8: "Schistosomiasis",
           9: "Onchoceriasis", 10: "LF"}
# added 8:"Schistomasis" in map
# Updated on :July 01,2020
# Updated by : Kasturi Vartak
app.config.from_object(__name__)


def connect_db():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'K_ghi.db')
    connection = sqlite3.connect(filename)
    return connection


# print conn.execute("select region from country2015").fetchall()

@app.route('/get_regions')
def getRegions():
    conn = connect_db()
    countries_obj = conn.execute("select region from country2015").fetchall()
    countries_obj.append('All Countries')
    return (countries_obj)


@app.route('/get_years')
def getYears():
    years = [2010, 2013, 2015]
    return (years)


@app.route('/get_countries_by_region')
def get_countries_by_region():
    conn = connect_db()
    region = request.args.get("selected_region")
    if (region == 'All Countries'):
        return getAllCountries()
    else:
        return (conn.execute("select country from country2015 where region ='" + str(region) + "'").fetchall())


# SEQUENCE1
# country -> disease -> drug -> company
# @app.route('/country', methods=['GET', 'POST'])
# def getAllCountries():
#     conn = connect_db()
#     countries_obj = conn.execute("select country from country2015").fetchall()
#     list_of_countries = [i[0] for i in countries_obj]
#     return json.dumps(list_of_countries)
#
#
# @app.route('/get_disease', methods=['GET', 'POST'])
# def getDiseaseFromCountry():
#     country_select = request.get_json()["selected_country"]
#     string_country_select = str(country_select)
#     # print country_select
#     conn = connect_db()
#     disease = []
#     # countries_obj = conn.execute("select * from country2015 where country = " + "' " + str(country_select) +"'").fetchall()
#     countries_obj = conn.execute(
#         "select * from country2015 where country = " + "\" " + str(country_select) + "\"").fetchall()
#
#     if (len(countries_obj) > 0):
#         for idx, val in enumerate(countries_obj[0][2:]):
#             if (val > 0):
#                 disease.append(mapping[idx + 2])
#         return json.dumps(disease)
#     return "No data found"
#     # return json.dumps("No diseases found")
#
#
# @app.route('/get_drug', methods=['GET', 'POST'])
# def getDrugByDisease():
#     selected_disease = request.get_json()["selected_disease"]
#     print(selected_disease)
#     selected_country = request.get_json()["selected_country"]
#     print(selected_country)
#     drugsToSelect = []
#     conn = connect_db()
#
#     drug_obj_by_dis = conn.execute(
#         "select distinct drug from drug2015 where disease ='" + selected_disease + "' COLLATE NOCASE").fetchall()
#     drug_obj_by_cntry = conn.execute(
#         "select distinct drug from countryDrug2015 where country='" + selected_country + "' and score>0").fetchall()
#
#     print(len(drug_obj_by_dis))
#     print(len(drug_obj_by_cntry))
#
#     if (len(drug_obj_by_cntry) > 0):
#         for drgIdxByDis, drgByDis in enumerate(drug_obj_by_dis):
#             for drgIdxByCnt, drgByCnt in enumerate(drug_obj_by_cntry):
#                 # print(drgByDis)
#                 # print(drgByCnt)
#                 if (drgByDis[0].lower() == drgByCnt[0].lower()):
#                     drugsToSelect.append(drgByDis[0])
#         return json.dumps(drugsToSelect)
#     return "No data found"
#
#     # drugs_obj = [i[0] for i in drug_obj]
#     # drugs_obj=[]
#     # for j in drug_obj:
#     #     if(j not in drugs_obj):
#     #         drugs_obj.append(j)
#     # return json.dumps(selected_country)
#     # drugs_obj = [i[0] for i in drug_obj]
#     # return json.dumps(drugs_obj)
#
#
# @app.route('/get_company', methods=['GET', 'POST'])
# def getCompanyByDrug():
#     selected_country = request.get_json()["selected_country"]
#     selected_disease = request.get_json()["selected_disease"]
#     drug = request.get_json()["selected_drug"]
#     conn = connect_db()
#     # Nutan: Added distinct to eliminate duplicates
#     company_obj = conn.execute("select distinct company from drug2015 where drug ='" + drug + "'").fetchall()
#     # companies_obj = [i[0] for i in company_obj]
#     # companies_obj = []
#     # for j in company_obj:
#     #     if(j not in companies_obj):
#     #         companies_obj.append(j)
#     # return json.dumps(companies_obj)
#     companies_obj = [i[0] for i in company_obj]
#     return json.dumps(companies_obj)
#     # return json.dumps(selected_country)
#
#
# # print getDiseaseFromCountry(" Albania")
# # print getDrugByDisease('TB')
# # print getCompanyByDrug("Lamivudine (3TC)")

@app.route('/country', methods=['GET', 'POST'])
def getCountries():
    requestJSON = request.get_json()
    print (requestJSON)
    # SEQUENCE 3 - Daniel
    if (requestJSON is  None):
        return "Error - Empty Request"
    if "selected_disease" in requestJSON and "selected_year" in requestJSON:
            string_disease_select = str(requestJSON["selected_disease"])
            year = str(requestJSON["selected_year"])
            country_year = "country" + year
            conn = connect_db()
            obj = conn.execute("select country from " + country_year + " where " + string_disease_select + "> 0").fetchall()
            countries = [i[0] for i in obj]
            # countries = getCountrybyDisease(string_disease_select)
            # print(countries)
            return json.dumps(countries)
    # SEQUENCE 1
    else:
        year = str(requestJSON["selected_year"])
        #print (year)
        country_year = "country" + year
        print (country_year)

        conn = connect_db()
        countries_obj = conn.execute("select country from " + country_year).fetchall()
        list_of_countries = [i[0] for i in countries_obj]
        return json.dumps(list_of_countries)


@app.route('/get_disease', methods=['GET', 'POST'])
def getDiseaseFromCountry():
    conn = connect_db()
    disease = []
    requestJSON = request.get_json()
    print(requestJSON)
    # SEQUENCE 1 - Daniel Orbach - 3/13/21
    if (requestJSON is not None) and ("selected_country" in requestJSON) and "selected_year" in requestJSON:
        country_select = requestJSON["selected_country"]
        country_year = "country" + str(requestJSON["selected_year"])
        string_country_select = str(country_select)
        # print("Country Select" + country_select)
        # countries_obj = conn.execute("select * from country2015 where country = " + "' " + str(country_select) +"'").fetchall()
        countries_obj = conn.execute(
            "select * from " + country_year + " where ltrim(country) = " + "\"" + str(country_select) + "\"").fetchall()

        # changes the query to add escape character in the middle like this  "\" " # Updated on :July 07,2020     # Updated by : Kasturi Vartak
        if (len(countries_obj) > 0):
            for idx, val in enumerate(countries_obj[0][2:]):
                if (val > 0):
                    disease.append(mapping[idx + 2])
            return json.dumps(disease)
        return "No data found"
    # SEQUENCE 3
    else:
        for key in mapping:
            disease.append(
                mapping[key])  # As mapping is tied with the DB we return the values in mapping instead # Daniel, Orbach
        return json.dumps(disease)




@app.route('/get_drug', methods=['GET', 'POST'])
def getDrugByDisease():
    requestJSON = request.get_json()
    #print("In Get Drug")
    print("Request: ", requestJSON)

    # SEQUENCE 1 , #SEQUENCE 3
    if ((requestJSON is not None) and ("selected_disease" in requestJSON) and ("selected_country" in requestJSON) and (
            "selected_year" in requestJSON)):
        #print("In IF Get Drug")
        selected_disease = request.get_json()["selected_disease"]
        selected_country = request.get_json()["selected_country"]
        selected_year = str(requestJSON["selected_year"])

        drug_year = "drug" + str(selected_year)
        countryDrug_year = "countryDrug" + str(selected_year)
        drugsToSelect = []
        conn = connect_db()
        if selected_disease == 'Schistosomiasis':
            selected_disease = 'Schistomasis'
        elif selected_disease == 'Onchoceriasis':
            selected_disease = 'onchoceriasis'
        elif selected_disease == 'LF':
            selected_disease = 'if'
        # Updated by: Nutan (Added condition to filter drugs by Country and Disease
        drug_obj_by_dis = conn.execute(
            "select distinct drug from " + drug_year + " where disease ='" + selected_disease + "' COLLATE NOCASE").fetchall()
        if selected_country == "Lao People's Democratic Republic":
            drug_obj_by_cntry = conn.execute(
                "select distinct drug from " + countryDrug_year + " where country like 'Lao People%' and score>0").fetchall()
        else:
            drug_obj_by_cntry = conn.execute(
                "select distinct drug from " + countryDrug_year + " where ltrim(country)='" + selected_country + "' COLLATE rtrim and score>0").fetchall()
        # print(len(drug_obj_by_dis)) #print(len(drug_obj_by_cntry))
        #print(drug_obj_by_dis)
        #print(drug_obj_by_cntry)
        if (len(drug_obj_by_cntry) > 0):
            for drgIdxByDis, drgByDis in enumerate(drug_obj_by_dis):
                for drgIdxByCnt, drgByCnt in enumerate(drug_obj_by_cntry):
                    # print(drgByDis)
                    # print(drgByCnt)
                    if (drgByDis[0].lower() == drgByCnt[0].lower()):
                        drugsToSelect.append(drgByDis[0])
            #print(drugsToSelect)
            return json.dumps(drugsToSelect)
        return "No data found"
    # SEQUENCES 2 and 4
    else:
        pass

    # drugs_obj = [i[0] for i in drug_obj]
    # added a for loop to filter so that only 1 drug will populate
    # Updated on :July 07,2020
    # Updated by : Kasturi Vartak
    # drugs_obj=[]
    # for j in drug_obj:
    #     if(j not in drugs_obj):
    #         drugs_obj.append(j)
    # return json.dumps(selected_country)
    # drugs_obj = [i[0] for i in drug_obj]
    # return json.dumps(drugs_obj)


@app.route('/get_company', methods=['GET', 'POST'])
def getCompanyByDrug():
    requestJSON = request.get_json()
    print("Request:")
    print(requestJSON)
    KeysFirstThird = {"selected_country", "selected_disease", "selected_drug"}
    companies_obj = []
    # First and Third Sequences
    if ((requestJSON  is not None)):
        # and requestJSON.keys() >= KeysFirstThird  (condition from above if)
        selected_country = request.get_json()["selected_country"]
        selected_disease = request.get_json()["selected_disease"]
        drug = request.get_json()["selected_drug"]
        drug_year = "drug" + str(requestJSON["selected_year"])
        conn = connect_db()
        # Nutan: Added distinct to eliminate duplicates
        company_obj = conn.execute(
            "select distinct company from " + drug_year + " where drug ='" + drug + "'").fetchall()
        # companies_obj = [i[0] for i in company_obj]
        # added a for loop to filter so that only 1 company will populate
        # Updated on :July 07,2020
        # Updated by : Kasturi Vartak
        # companies_obj = []
        # for j in company_obj:
        #     if(j not in companies_obj):
        #         companies_obj.append(j)
        # return json.dumps(companies_obj)
        # Nutan
        companies_obj = [i[0] for i in company_obj]
    return json.dumps(companies_obj)
    # return json.dumps(selected_country)


# Sequence 2
# drug->country->disease->Company
# def getAllDrugs():
#     conn = connect_db()
#     obj = conn.execute("select drug from drug2015").fetchall()
#     return obj


# def getCountrybyDrug(drug):
#     conn = connect_db()
#     obj = conn.execute("select country from drugimpact2015 where drug > 0").fetchall()
#     return obj


# def getDiseaseByCountry(country):
#     conn = connect_db()
#     countries = []
#     obj = conn.execute("select * from country2015 where country =" + country).fetchall()
#     for idx, val in enumerate(obj[0][2:]):
#         if (val > 0):
#             countries.append(mapping[idx + 2])
#     return countries

@app.route('/drug', methods=['GET', 'POST'])
def getAllDrugs():
    conn = connect_db()
    drug_year = "drug" + str(request.get_json()["selected_year"])
    drugs_obj = conn.execute("select drug from " + drug_year).fetchall()
    drugs_list = [i[0] for i in drugs_obj]
    # remove duplicates
    drugs_list = list(set(drugs_list))
    # alphebatize
    drugs_list.sort()
    return json.dumps(drugs_list)


@app.route('/get_country_by_drug', methods=['GET', 'POST'])
def getCountrybyDrug():
    conn = connect_db()
    drug = request.get_json()["selected_drug"]
    countryDrug_year = "countryDrug" + request.get_json()["selected_year"]
    # had to use lower case because of mismatches in databases
    drug = drug.lower()
    countries_obj = conn.execute(
        "select country from " + countryDrug_year + " where LOWER(drug) ='" + drug + "' AND score > 0").fetchall()
    list_of_countries = [i[0] for i in countries_obj]
    # alphebatize
    list_of_countries.sort()
    return json.dumps(list_of_countries)


@app.route('/get_disease_by_drug', methods=['GET', 'POST'])
def getDiseaseFromCountryandDrug():
    country_select = request.get_json()["selected_country"]
    drug = request.get_json()["selected_drug"]
    country_year = "country" + str(request.get_json()["selected_year"])
    drug_year = "drug" + str(request.get_json()["selected_year"])
    drug = drug.lower()
    conn = connect_db()
    diseases = []
    countries_obj = conn.execute(
        "select * from " + country_year + " where country = " + "' " + str(country_select) + "'").fetchall()

    enumerate(countries_obj)

    if (len(countries_obj) > 0):
        for idx, val in enumerate(countries_obj[0][2:]):
            # print(idx)
            # print(diseases)
            if (val > 0):
                diseases.append(mapping[idx + 2])
        # disease now all diseases associated with country. We will now filter out all diseases not treated by selected_drug
        # print(diseases)
        diseases_final = []
        for disease in diseases:
            # print("checking", disease)
            if (conn.execute(
                    "select disease from " + drug_year + " where LOWER(drug) ='" + drug + "'AND  LOWER(disease) ='" + disease.lower() + "'").fetchall()):
                # print("adding: ", disease)
                diseases_final.append(disease)
        # remove duplicates
        diseases_final = list(set(diseases_final))
        # alphebatize
        diseases_final.sort()
        return json.dumps(diseases_final)
    return "No data found"


@app.route('/get_company_by_drug', methods=['GET', 'POST'])
def getCompanyByDiseaseAndCountryAndDrug():
    drug = request.get_json()["selected_drug"]
    country = request.get_json()["selected_country"]
    disease = request.get_json()["selected_disease"]
    countryDrug_year = "countryDrug" + str(request.get_json()["selected_year"])
    drug_year = "drug" + str(request.get_json()["selected_year"])

    conn = connect_db()

    # filter by drug and country
    company_obj = conn.execute(
        "select company from " + countryDrug_year + " where score > 0 AND LOWER(drug) ='" + drug.lower() + "' AND LOWER(country) ='" + country.lower() + "'").fetchall()
    companies_obj = [i[0] for i in company_obj]

    # if there are multiple unique companies, filter through diseases as well
    companies_obj_final = []
    companies_obj = list(set(companies_obj))
    companies_obj.append("Sanofi")
    if (len(companies_obj) > 1):
        compDisObj = conn.execute(
            "select company from " + drug_year + " where score > 0 AND LOWER(drug) ='" + drug.lower() + "' AND LOWER(disease) ='" + disease.lower() + "'").fetchall()
        compDisObj = [i[0] for i in compDisObj]
        # filter companies by drug, country, and disease
        companies_obj_final = list(set(set(compDisObj).intersection(set(companies_obj))))
    else:
        companies_obj_final = companies_obj

    # make sure things don't print out awkwardly if there is one unique answer
    if (len(companies_obj_final) == 1):
        retVal = [1]
        retVal[0] = companies_obj[0]
        return json.dumps(retVal)

    # alphebatize
    companies_obj_final.sort()
    return json.dumps(companies_obj_final)


# can use the above company by disease for next function


# # disease -> country -> drug-> company
# def getAllDisease():
#     conn = connect_db()
#     obj = conn.execute("select disease from disease2015").fetchall()
#     return obj
#
#
# def getCompanybyDisease(disease):
#     conn = connect_db()
#     obj = conn.execute("select disease, company from manudis2015").fetchall()
#     d = {}
#     for key, value in obj:
#         if key not in d:
#             d[key] = []
#         d[key].append(value)
#     return d[disease]
#
#
# def getCountrybyDrug(drug):
#     conn = connect_db()
#     obj = conn.execute("select country from drugimpact2015 where drug > 0").fetchall()
#     return obj
#
#
# def getCountrybyDisease(disease):
#     conn = connect_db()
#     obj = conn.execute("select country from countrybydis2010 where " + disease + "> 0").fetchall()
#     return obj

# Changed by: Nutan (03/12/2021)
# Sequence 4
# company -> Country -> disease -> drug
# Commenting Old Default code and adding the API calls
# def getAllCompanies():
#     conn = connect_db()
#     obj = conn.execute("select manufacturer from manufacturer").fetchall()
#     return obj
#
# # can use the getCountrybyDisease function from the first sequence
# def getCountryByCompany(selected_company):
#     conn = connect_db()
#     # get drug by company
#     drug_obj = conn.execute("select drug from drug2015 where company='" + selected_company + "'").fetchall()
#     # for each_drug in drug_obj:
#     #     #will need harshal's table here
#     # return obj
#     return drug_obj
#
# def getDrugByCountry(selected_country):
#     conn = connect_db()
#     obj = conn.execute("select distype from distypes where country = '" + selected_country + "'").fetchall()
#     return obj
#
# def getDrugbyCompany():
#     conn = connect_db()
@app.route('/company', methods=['GET', 'POST'])
def getAllCompanies():
    conn = connect_db()
    # companies_obj = conn.execute("select manufacturer from manufacturer").fetchall()
    drugr_year = "drugr" + str(request.get_json()["selected_year"])
    companies_obj = conn.execute("select distinct company from " + drugr_year).fetchall()
    list_of_companies = [i[0] for i in companies_obj]
    return json.dumps(list_of_companies)


# can use the getCountrybyDisease function from the first sequence

# Get company for the drug selected
@app.route('/get_country_by_cmpny', methods=['GET', 'POST'])
def getCountryByCompany():
    company_select = request.get_json()["selected_company"]
    countryDrug_year = "countryDrug" + str(request.get_json()["selected_year"])
    print(company_select)
    conn = connect_db()
    # country_obj = conn.execute("select country from country2015").fetchall()
    # country_obj = conn.execute("select country from company_country_mapping where company='"+company_select+"'").fetchall()
    country_obj = conn.execute(
        "select distinct country from " + countryDrug_year + " where company='" + company_select + "' and score>0").fetchall()
    list_of_countries = [i[0] for i in country_obj]
    return json.dumps(list_of_countries)


# Get disease from Company selected
@app.route('/get_disease_by_cmpny', methods=['GET', 'POST'])
def getDiseaseFromCountryCmpny():
    print("In disease selection")
    country_select = request.get_json()["selected_country"]
    print("selected country")
    print(country_select)
    # company_select = "Kyorin Pharmaceutical Co., Ltd."
    company_select = request.get_json()["selected_company"]
    country_year = "country" + str(request.get_json()["selected_year"])
    drug_year = "drug" + str(request.get_json()["selected_year"])
    print("selected company")
    print(company_select)
    conn = connect_db()
    disease = []
    countries_obj = conn.execute(
        "select * from " + country_year + " where country = " + "' " + str(country_select) + "'").fetchall()
    company_obj = conn.execute(
        "select distinct disease from " + drug_year + " where company = '" + company_select + "'").fetchall()
    print(company_obj)
    print(countries_obj)

    # if((len(countries_obj) >0 ) and (len(company_obj) > 0)):
    if (len(countries_obj) > 0):
        for idx, val in enumerate(countries_obj[0][2:]):
            if (val > 0):
                print(idx, val)
                for cmpnyIdx, cmpnyDisease in enumerate(company_obj):
                    print("disease based on copny")
                    print(cmpnyIdx, cmpnyDisease[0])
                    if ((mapping[idx + 2]).lower() == cmpnyDisease[0].lower()):
                        disease.append(mapping[idx + 2])
        return json.dumps(disease)
    return "No data found"
    # return json.dumps("No diseases found")


# Get drug from disease selected
################## Can use same API call as /get_drug - Can be removed ###################
@app.route('/get_drug_by_cmpny', methods=['GET', 'POST'])
def getDrugByDiseaseCmpny():
    selected_disease = request.get_json()["selected_disease"]
    selected_company = request.get_json()["selected_company"]
    selected_country = request.get_json()["selected_country"]
    countryDrug_year = "countryDrug" + str(request.get_json()["selected_year"])
    drug_year = "drug" + str(request.get_json()["selected_year"])
    print("Request: ")
    print(request.get_json()) 
    # company_select = "Kyorin Pharmaceutical Co., Ltd."

    if selected_disease == 'Schistosomiasis':
        selected_disease = 'Schistomasis'
    elif selected_disease == 'Onchoceriasis':
        selected_disease = 'onchoceriasis'
    elif selected_disease == 'LF':
        selected_disease = 'if'

    drugsToSelect = []
    conn = connect_db()
    drug_obj_by_dis = conn.execute(
        "select distinct drug from " + drug_year + " where disease ='" + selected_disease + "' COLLATE NOCASE and company ='" + selected_company + "' COLLATE NOCASE").fetchall()
    # drug_obj = conn.execute("select drug from drug2015 where disease ='"+selected_disease+"' COLLATE NOCASE").fetchall()

    if selected_country == "Lao People's Democratic Republic":
        drug_obj_by_cntry = conn.execute(
            "select distinct drug from " + countryDrug_year + " where country like 'Lao People%' and score>0").fetchall()
    else:
        drug_obj_by_cntry = conn.execute(
            "select distinct drug from " + countryDrug_year + " where ltrim(country)='" + selected_country + "' and score>0").fetchall()

    # print(len(drug_obj_by_dis)) #print(len(drug_obj_by_cntry))
    print(drug_obj_by_dis)
    print(drug_obj_by_cntry)
    if (len(drug_obj_by_cntry) > 0):
        for drgIdxByDis, drgByDis in enumerate(drug_obj_by_dis):
            for drgIdxByCnt, drgByCnt in enumerate(drug_obj_by_cntry):
                if (drgByDis[0].lower() == drgByCnt[0].lower()):
                    drugsToSelect.append(drgByDis[0])
        print(drugsToSelect)
        return json.dumps(drugsToSelect)
    return "No data found"
    # drugs_obj = [i[0] for i in drug_obj]
    # # getCompanyByDrug(drug_obj[0][0])
    # return json.dumps(drugs_obj)


### Sequece 4 END

# specification start
# to display specifications in the dropdown
@app.route('/get_specification', methods=['GET', 'POST'])
def getSpecification():
    print('Request:')
    print(request.get_json())
    selected_country = request.get_json()["selected_country"]
    selected_year = request.get_json()["selected_year"]
    selected_disease = request.get_json()["selected_disease"]
    selected_drug = request.get_json()["selected_drug"]
    selected_year = request.get_json()["selected_year"]
    #print(selected_drug)
    # selected_company = request.get_json()["selected_company"]
    sd = selected_drug[selected_drug.find("(") + 1:selected_drug.find(")")]
    #print(sd)
    spec = []
    conn = connect_db()
    spec_obj = ""
    if (selected_disease == 'TB' or selected_disease == 'Malaria'):
        spec_obj = conn.execute(
            "select tb_hiv_plus,tb_hiv_minus,tb_mdr,tb_xdr,malaria_PFalc, malaria_PVivax from spec_treatment_regimen where drug ='" + sd + "' COLLATE NOCASE").fetchall()
    elif (selected_disease == 'HIV'):
        spec_obj = conn.execute(
            "select Ndrug,Adult_prop,Children_prop,Adult_eff,Children_eff from spec_2015_HIV_Regimen where Regimens like '%" + sd + "%' COLLATE NOCASE").fetchall()
    spec_obj_NTDs = conn.execute(
        "select disease from drug2015 where drug ='" + selected_drug + "' COLLATE NOCASE").fetchall()
    #print(spec_obj_NTDs)
    worms = [i[0] for i in spec_obj_NTDs if 'worm' in i[0]]
    otherNTDs = [i[0] for i in spec_obj_NTDs if 'worm' not in i[0]]

    # spec_test = conn.execute("select * from spec_treatment_regimen where drug ='" + sd + "' COLLATE NOCASE").fetchall()
    #print(spec_obj)
    # print(spec_test)
    # spec.append(spec_obj)
    # for n in spec_obj:
    #     spec.append(n[0])
    if (len(spec_obj) > 0):
        if (selected_disease == 'TB'):
            spec.append('Prevalence')
            # spec.append('Treatment coverage:')
            if spec_obj[0][0] == 'True':
                spec.append('TB/HIV+ Coverage')
            if spec_obj[0][1] == 'True':
                spec.append('TB/HIV- Coverage')
            if spec_obj[0][2] == 'True':
                spec.append('MDR-TB Coverage')
            if spec_obj[0][3] == 'True':
                spec.append('XDR-TB Coverage')
            # spec.append('Efficacy:')
            if spec_obj[0][0] == 'True':
                spec.append('TB/HIV+ Efficacy')
            if spec_obj[0][1] == 'True':
                spec.append('TB/HIV- Efficacy')
            if spec_obj[0][2] == 'True':
                spec.append('MDR-TB Efficacy')
            if spec_obj[0][3] == 'True':
                spec.append('XDR-TB Efficacy')
            # spec.append('DALY:')
            if spec_obj[0][0] == 'True':
                spec.append('TB/HIV+ DALY')
            if spec_obj[0][1] == 'True':
                spec.append('TB/HIV- DALY')
            if spec_obj[0][2] == 'True':
                spec.append('MDR-TB DALY')
            if spec_obj[0][3] == 'True':
                spec.append('XDR-TB DALY')

        # use this code if they want specifications to be as PFalc and PVivax for Malaria
        elif (selected_disease == 'Malaria'):
            # spec_obj = conn.execute(
            #     "select malaria_PFalc,malaria_PVivax from spec_treatment_regimen where drug ='" + sd + "' COLLATE NOCASE").fetchall()
            spec.append('Prevalence')
            # spec.append('Treatment coverage:')
            if spec_obj[0][4] == 'True':
                spec.append('Malaria PFalc Coverage')
            if spec_obj[0][5] == 'True':
                spec.append('Malaria PVivax Coverage')

            # spec.append('Efficacy:')
            if spec_obj[0][4] == 'True':
                spec.append('Malaria PFalc Efficacy')
            if spec_obj[0][5] == 'True':
                spec.append('Malaria PVivax Efficacy')

            # spec.append('DALY:')
            if spec_obj[0][4] == 'True':
                spec.append('Malaria PFalc DALY')
            if spec_obj[0][5] == 'True':
                spec.append('Malaria PVivax DALY')
        elif (selected_disease == 'HIV'):
            if selected_year == '2015':
                spec.append("Treatment Coverage Adults")
                spec.append("Treatment Coverage Children")
                spec.append("Adult DALY")
                spec.append("Child DALY")
                spec.append("Overall Retention Rates")
                spec.append("Adult Retention Rates")
                spec.append("Child Retention Rates")
                spec.append("First-line Adult Distribution")
                spec.append("Second-line Adult Distribution")
                spec.append("First-line Child Distribution")
                spec.append("Second-line Child Distribution")
                spec.append("First-line Regimen Adult Proportion")
                spec.append("Second-line Regimen Adult Proportion")
                spec.append("First-line Regimen Child Proportion")
                spec.append("Second-line Regimen child Proportion")
                spec.append("First-line Regimen Adult Efficacy")
                spec.append("Second-line Regimen Adult Efficacy")
                spec.append("First-line Regimen Child Efficacy")
                spec.append("Second-line Regimen Child Efficacy")
            #HIV 2013 and 2010 use WHO groups for impact scores
            elif selected_year == '2013' or selected_year == '2010':
                spec_obj = conn.execute("select * from spec_"+ selected_year +"_HIV where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

                #No matter the group, these specifications are present
                spec.append("Treatment Coverage Adults")
                spec.append("Treatment Coverage Children")
                spec.append("Adult DALY")
                spec.append("Child DALY")
                spec.append("Overall Retention Rates")
                spec.append("Adult Retention Rates")
                spec.append("Child Retention Rates")
                #GROUP A Country
                print(spec_obj)
                if spec_obj[0][12] == 'A':
                    spec.append("Group A First-line Adult Distribution")
                    spec.append("Group A Second-line Adult Distribution")
                    spec.append("Group A First-line Child Distribution")
                    spec.append("Group A Second-line Child Distribution")
                    spec.append("Group A First-line Regimen Adult Proportion")
                    spec.append("Group A Second-line Regimen Adult Proportion")
                    spec.append("Group A First-line Regimen Child Proportion")
                    spec.append("Group A Second-line Regimen child Proportion")
                    spec.append("Group A First-line Regimen Adult Efficacy")
                    spec.append("Group A Second-line Regimen Adult Efficacy")
                    spec.append("Group A First-line Regimen Child Efficacy")
                    spec.append("Group A Second-line Regimen Child Efficacy")
                #GROUP B Country
                else:
                    spec.append("Group B First-line Adult Distribution")
                    spec.append("Group B Second-line Adult Distribution")
                    spec.append("Group B First-line Child Distribution")
                    spec.append("Group B Second-line Child Distribution")
                    spec.append("Group B First-line Regimen Adult Proportion")
                    spec.append("Group B Second-line Regimen Adult Proportion")
                    spec.append("Group B First-line Regimen Child Proportion")
                    spec.append("Group B Second-line Regimen child Proportion")
                    spec.append("Group B First-line Regimen Adult Efficacy")
                    spec.append("Group B Second-line Regimen Adult Efficacy")
                    spec.append("Group B First-line Regimen Child Efficacy")
                    spec.append("Group B Second-line Regimen Child Efficacy")
        else:
            spec.append("All specifications")
        # return json.dumps(spec)

    elif (len(spec_obj_NTDs) > 0):
        if (
                selected_disease == 'Roundworm'
                or selected_disease == 'Hookworm'
                or selected_disease == 'Whipworm'
        ):
            spec.append('Prevalence for 1-4 year olds')
            spec.append('Prevalence for 5-14 year olds')
            spec.append('Pre-Sac Treatment Coverage')
            spec.append('SAC Treatment Coverage')
            spec.append('Efficacy')
            spec.append('DALYs for 1-4 year olds')
            spec.append('DALYs for 5-14 year olds')

        elif (
                selected_disease == 'Onchoceriasis'
                or selected_disease == 'Schistosomiasis'
                or selected_disease == 'LF'
        ):
            spec.append('Prevalence')
            spec.append('Treatment Coverage')
            spec.append('Efficacy')
            spec.append('DALY')

        else:
            spec.append("All specifications")

    if (len(spec) > 0):
        return json.dumps(spec)

    return "No Data Found"


# calculate Index for tb
@app.route('/get_spec_tb', methods=['GET', 'POST'])
def getSpecTB():
    print("In Tb Specifications")
    conn = connect_db()

    if (request.get_json() is  None):
        return "Error - Empty Request"

    selected_country = request.get_json()["selected_country"]
    selected_disease = request.get_json()["selected_disease"]
    selected_drug = request.get_json()["selected_drug"]
    sd = selected_drug[selected_drug.find("(") + 1:selected_drug.find(")")]
    selected_company = request.get_json()["selected_company"]
    selected_specification = request.get_json()["selected_specification"]
    selected_year = request.get_json()["selected_year"]
    #print("SelectedYear: " + selected_year)
    # print("Specification Name ***************")
    # print(request.get_json()["SpecificationName"])
    # print(selected_specification)

    spec_year_TB = "spec_" + str(selected_year) + "_TB"
    spec_obj = conn.execute(
        "select * from " + spec_year_TB + " where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

    specdrug_obj = conn.execute(
        "select tb_hiv_plus,tb_hiv_minus,tb_mdr,tb_xdr from spec_treatment_regimen where drug ='" + sd + "' COLLATE NOCASE").fetchall()

    TB_pevalance = spec_obj[0][1]
    TB_plus_Efficacy = 0
    TB_plus_coverage = 0
    TB_plus_DALY = 0
    if ((len(specdrug_obj) > 0) and (specdrug_obj[0][0] == 'True')):
        TB_plus_Efficacy = 0.78
        TB_plus_coverage = spec_obj[0][2] / 100
        TB_plus_DALY = spec_obj[0][6]

    TB_minus_coverage = 0
    TB_minus_Efficacy = 0
    TB_minus_DALY = 0
    if ((len(specdrug_obj) > 0) and (specdrug_obj[0][1] == 'True')):
        TB_minus_coverage = spec_obj[0][3] / 100
        TB_minus_Efficacy = 0.83  # predefined, check handbook
        TB_minus_DALY = spec_obj[0][7]

    TB_mdr_coverage = 0
    TB_mdr_Efficacy = 0
    TB_mdr_DALY = 0
    if ((len(specdrug_obj) > 0) and (specdrug_obj[0][2] == 'True')):
        TB_mdr_coverage = spec_obj[0][4] / 100
        TB_mdr_Efficacy = 0.54  # predefined, check handbook
        TB_mdr_DALY = spec_obj[0][8]

    TB_xdr_coverage = 0
    TB_xdr_Efficacy = 0
    TB_xdr_DALY = 0
    if ((len(specdrug_obj) > 0) and (specdrug_obj[0][3] == 'True')):
        TB_xdr_coverage = spec_obj[0][5] / 100
        TB_xdr_Efficacy = 0.30  # predefined, check handbook
        TB_xdr_DALY = spec_obj[0][9]

    d = {}
    I = 0
    for each_spec in selected_specification:
        # print(each_spec)
        # Set the required values, which will be further used to calculate Impact Score
        # and further passed to specifications page.
        if each_spec == "Prevalence":
            d["TB Prevalence"] = TB_pevalance

        # 1. Set Treatment Coverage Values
        if each_spec == "TB/HIV+ Coverage":
            d["TB/HIV+ Treatment Coverage"] = float(Decimal(str(TB_plus_coverage)) * 100)

        if each_spec == "TB/HIV- Coverage":
            d["TB/HIV- Treatment Coverage"] = float(Decimal(str(TB_minus_coverage)) * 100)

        if each_spec == "MDR-TB Coverage":
            d["MDR-TB Treatment Coverage"] = float(Decimal(str(TB_mdr_coverage)) * 100)

        if each_spec == "XDR-TB Coverage":
            d["XDR-TB Treatment Coverage"] = float(Decimal(str(TB_xdr_coverage)) * 100)

        # 2. Set Efficacy Values
        if each_spec == "TB/HIV+ Efficacy":
            d["TB/HIV+ Efficacy"] = float(Decimal(str(TB_plus_Efficacy)) * 100)

        if each_spec == "TB/HIV- Efficacy":
            d["TB/HIV- Efficacy"] = float(Decimal(str(TB_minus_Efficacy)) * 100)

        if each_spec == "MDR-TB Efficacy":
            d["MDR-TB Efficacy"] = float(Decimal(str(TB_mdr_Efficacy)) * 100)

        if each_spec == "XDR-TB Efficacy":
            d["XDR-TB Efficacy"] = float(Decimal(str(TB_xdr_Efficacy)) * 100)

        # 2. Set DALY Values
        if each_spec == "TB/HIV+ DALY":
            d["TB/HIV+ DALYs"] = TB_plus_DALY

        if each_spec == "TB/HIV- DALY":
            d["TB/HIV- DALYs"] = TB_minus_DALY

        if each_spec == "MDR-TB DALY":
            d["MDR-TB DALYs"] = TB_mdr_DALY

        if each_spec == "XDR-TB DALY":
            d["XDR-TB DALYs"] = TB_xdr_DALY

    # Calculate Original Impact Score of TB/HIV+
    # print (TB_plus_DALY)
    # print(TB_plus_Efficacy)
    # print(TB_plus_coverage)
    TB_HIV_plus_I = ((TB_plus_DALY * TB_plus_Efficacy * TB_plus_coverage) / (
            1 - (TB_plus_Efficacy * TB_plus_coverage)))
    # print (TB_HIV_plus_I)
    # Calculate Original Impact Score of TB/HIV-
    TB_HIV_minus_I = ((TB_minus_DALY * TB_minus_Efficacy * TB_minus_coverage) / (
            1 - (TB_minus_Efficacy * TB_minus_coverage)))
    # print (TB_HIV_minus_I)
    # Calculate Original Impact Score of MDR-TB
    MDR_TB_I = ((TB_mdr_DALY * TB_mdr_Efficacy * TB_mdr_coverage) / (1 - (TB_mdr_Efficacy * TB_mdr_coverage)))
    # print(MDR_TB_I)
    # Calculate Original Impact Score of XDR-TB
    XDR_TB_I = ((TB_xdr_DALY * TB_xdr_Efficacy * TB_xdr_coverage) / (1 - (TB_xdr_Efficacy * TB_xdr_coverage)))
    # print (XDR_TB_I)
    # Calculate Total Impact Score
    I = TB_HIV_plus_I + TB_HIV_minus_I + MDR_TB_I + XDR_TB_I

    d["Original Impact Score"] = round(I, 2)
    print("Originial Impact Score")
    print(I)
    print(d)
    conn.close()
    # return json.dumps(I)
    return json.dumps(d)


# calculate Index for malaria
@app.route('/get_spec_malaria', methods=['GET', 'POST'])
def getSpecMalaria():
    selected_country = request.get_json()["selected_country"]
    selected_disease = request.get_json()["selected_disease"]
    selected_company = request.get_json()["selected_company"]
    selected_year = request.get_json()["selected_year"]
    print("SelectedYear: " + str(selected_year))
    spec_year_Malaria = "spec_" + str(selected_year) + "_Malaria"
    selected_drug = request.get_json()["selected_drug"]
    sd = selected_drug[selected_drug.find("(") + 1:selected_drug.find(")")]
    print("MALARIA", selected_drug)
    selected_drug = sd.replace(" + ", "_").replace("-", "_")
    print(selected_drug)

    selected_specification = request.get_json()["selected_specification"]
    print(selected_specification)
    # selected_specification = ['PFalc', 'PVivax']
    d = {}
    I = 0
    conn = connect_db()
    cursor = conn.execute("select * from " + spec_year_Malaria)
    names = list(map(lambda x: x[0], cursor.description))
    drug_column1 = "Eff_PFalc_" + selected_drug
    drug_column2 = "Eff_PVivax_" + selected_drug

    print("drug_column1: ", drug_column1)
    print("drug_column2: ", drug_column2)

    # spec_obj = conn.execute(
    #     "select Coverage_Malaria_PFalc,DALY_Malaria," + drug_column + "  from spec_2015_Malaria where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

    spec_obj = conn.execute(
        "select * from " +spec_year_Malaria + " where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

    specdrug_obj = conn.execute(
        "select malaria_PFalc, malaria_PVivax from spec_treatment_regimen where drug ='" + sd + "' COLLATE NOCASE").fetchall()

    Malaria_pevalance = spec_obj[0][1]
    Malaria_PFalc_coverage = 0
    Malaria_PFalc_DALY_prop = 0
    if ((len(specdrug_obj) > 0) and (specdrug_obj[0][0] == 'True')):
        Malaria_PFalc_coverage = spec_obj[0][2] / 100
        Malaria_PFalc_DALY_prop = spec_obj[0][4] / 100
        # print("Malaria_PFalc_DALY_Prop ", Malaria_PFalc_DALY_prop)

    Malaria_PVivax_coverage = 0
    Malaria_PVivax_DALY_prop = 0
    if ((len(specdrug_obj) > 0) and (specdrug_obj[0][1] == 'True')):
        Malaria_PVivax_coverage = spec_obj[0][3] / 100
        Malaria_PVivax_DALY_prop = spec_obj[0][5] / 100
        # print("Malaria_PVivax_DALY_Prop ", Malaria_PVivax_DALY_prop)

    Malaria_Total_DALY = spec_obj[0][6]
    # print("Malaria_Total_DALY ", Malaria_Total_DALY)
    Malaria_PFalc_DALY = round((Malaria_PFalc_DALY_prop * Malaria_Total_DALY), 2)
    Malaria_PVivax_DALY = round((Malaria_PVivax_DALY_prop * Malaria_Total_DALY), 2)
    # print ("Malaria_PFalc_DALY ",Malaria_PFalc_DALY)
    # print("Malaria_PVivax_DALY ", Malaria_PVivax_DALY)

    Malaria_PFalc_Efficacy = 0
    Malaria_PVivax_Efficacy = 0

    if drug_column1 in names:
        print("In drug_column1")
        spec_obj_eff1 = conn.execute(
            "select " + drug_column1 + " from " + spec_year_Malaria + " where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
        print("spec_obj_eff1: ", spec_obj_eff1)

        if (len(spec_obj_eff1) > 0):
            Malaria_PFalc_Efficacy = spec_obj_eff1[0][0] / 100  # predefined, check handbook

    if drug_column2 in names:
        print("In drug_column2")
        spec_obj_eff2 = conn.execute(
            "select " + drug_column2 + " from " + spec_year_Malaria + " where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
        print("spec_obj_eff2: ", spec_obj_eff2)
        if (len(spec_obj_eff2) > 0):
            Malaria_PVivax_Efficacy = spec_obj_eff2[0][0] / 100

    for each_spec in selected_specification:
        # Set the required values, which will be further used to calculate Impact Score
        # and further passed to specifications page.

        if each_spec == "Prevalence":
            d["Malaria Prevalence"] = Malaria_pevalance

        # 1. Set Treatment Coverage Values

        if each_spec == "Malaria PFalc Coverage":
            d["Malaria PFalc Coverage"] = float(Decimal(str(Malaria_PFalc_coverage)) * 100)

        if each_spec == "Malaria PVivax Coverage":
            d["Malaria PVivax Coverage"] = float(Decimal(str(Malaria_PVivax_coverage)) * 100)

        # 2. Set DALY Values

        if each_spec == "Malaria PFalc DALY":
            d["Malaria PFalc DALY"] = Malaria_PFalc_DALY

        if each_spec == "Malaria PVivax DALY":
            d["Malaria PVivax DALY"] = Malaria_PVivax_DALY

        # 2. Set Efficacy Values
        if each_spec == "Malaria PFalc Efficacy":
            d["Malaria PFalc Efficacy"] = float(Decimal(str(Malaria_PFalc_Efficacy)) * 100)

        if each_spec == "Malaria PVivax Efficacy":
            d["Malaria PVivax Efficacy"] = float(Decimal(str(Malaria_PVivax_Efficacy)) * 100)

    # Malaria_PFalc_I = 0
    Malaria_PFalc_I = ((Malaria_PFalc_DALY * Malaria_PFalc_coverage * Malaria_PFalc_Efficacy) / (
            1 - (Malaria_PFalc_coverage * Malaria_PFalc_Efficacy)))

    # Malaria_PVivax_I = 0
    Malaria_PVivax_I = ((Malaria_PVivax_DALY * Malaria_PVivax_coverage * Malaria_PVivax_Efficacy) / (
            1 - (Malaria_PVivax_coverage * Malaria_PVivax_Efficacy)))

    I = I + Malaria_PFalc_I + Malaria_PVivax_I
    # I = I / 2
    # need to pass this dictionsry
    d["Original Impact Score"] = round(I, 2)
    print("Originial Impact Score")
    print(I)
    print(d)
    conn.close()
    return json.dumps(d)

# calculate index for HIV:
@app.route('/get_spec_hiv', methods=['GET', 'POST'])
def getSpecHIV():
    selected_year = request.get_json()["selected_year"]
    selected_country = request.get_json()["selected_country"]
    selected_disease = request.get_json()["selected_disease"]
    selected_drug = request.get_json()["selected_drug"]
    sd = selected_drug[selected_drug.find("(") + 1:selected_drug.find(")")]
    selected_company = request.get_json()["selected_company"]
    selected_specification = request.get_json()["selected_specification"]
    selected_year = request.get_json()["selected_year"]
    print("SelectedYear: " + selected_year)
    print(selected_specification)
    conn = connect_db()
    d={}
    if selected_year == '2015':
        spec_obj = conn.execute("select * from spec_2015_HIV where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
        regimen1_obj = conn.execute("select * from spec_2015_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 COLLATE NOCASE").fetchall()
        regimen2_obj = conn.execute("select * from spec_2015_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 COLLATE NOCASE").fetchall()
        # Original specification values
        adult_coverage = spec_obj[0][1] / 100
        child_coverage = spec_obj[0][4] / 100
        adult_daly = spec_obj[0][7]
        child_daly = spec_obj[0][8]
        overall_rate = spec_obj[0][9] / 100
        adult_rate = spec_obj[0][10] / 100
        child_rate = spec_obj[0][11] / 100
        first_adult_distribution = 0.9084 #constant
        second_adult_distribution = 0.0917 #constant
        first_child_distribution = 0.8933 #constant
        second_child_distribution = 0.1068 #constant
        first_adult_prop = 0
        second_adult_prop = 0
        first_adult_eff = 0
        second_adult_eff = 0
        first_child_prop = 0
        second_child_prop = 0
        first_child_eff = 0
        second_child_eff = 0
        for k in regimen1_obj:
            first_adult_prop += k[2]/k[1]
            first_adult_eff += k[4]/k[1]
            first_child_prop += k[3]/k[1]
            first_child_eff += k[5]/k[1]
        for k in regimen2_obj:
            second_adult_prop += k[2]/k[1]
            second_adult_eff += k[4]/k[1]
            second_child_prop += k[3]/k[1]
            second_child_eff += k[5]/k[1]
        I_a1 = (adult_daly * adult_coverage * (first_adult_distribution * first_adult_prop * first_adult_eff))/(1 - adult_coverage *(first_adult_distribution * first_adult_prop * first_adult_eff))
        I_a2 = (adult_daly * adult_coverage * (second_adult_distribution * second_adult_prop * second_adult_eff))/(1 - adult_coverage *(second_adult_distribution * second_adult_prop * second_adult_eff))
        I_c1 = (child_daly * child_coverage * (first_child_distribution * first_child_prop * first_child_eff))/(1 - child_coverage*(first_child_distribution * first_child_prop * first_child_eff))
        I_c2 = (child_daly * child_coverage * (second_child_distribution * second_child_prop * second_child_eff))/(1 - child_coverage*(second_child_distribution * second_child_prop * second_child_eff))
        I = I_a1 + I_a2 + I_c1 + I_c2
        d = {}
        d["Original Impact Score"] = round(I, 2)
        for spec in selected_specification:
            if spec == "Treatment Coverage Adults":
                d["Adults Needing Treatment"] = spec_obj[0][2]
                d["Adults Receiving Treatment"] = spec_obj[0][3]
            if spec == "Treatment Coverage Children":
                d["Children Needing Treatment"] = spec_obj[0][5]
                d["Children Receiving Treatment"] = spec_obj[0][6]
            if spec == "Adult DALY":
                d["Adult DALY"] = adult_daly
            if spec == "Child DALY":
                d["Child DALY"] = child_daly
            if spec == "Overall Retention Rates":
                d["Overall Retention Rates"] = round((overall_rate * 100),2)
            if spec == "Adult Retention Rates":
                d["Adult Retention Rates"] = round((adult_rate * 100),2)
            if spec == "Child Retention Rates":
                d["Child Retention Rates"] = round((child_rate * 100),2)
            if spec == "First-line Adult Distribution":
                d["First-line Adult Distribution"] = round(first_adult_distribution*100,2)
            if spec == "Second-line Adult Distribution":
                d["Second-line Adult Distribution"] = round(second_adult_distribution*100,2)
            if spec == "First-line Child Distribution":
                d["First-line Child Distribution"] = round(first_child_distribution*100,2)
            if spec == "Second-line Child Distribution":
                d["Second-line Child Distribution"] = round(second_child_distribution*100,2)
            if spec == "First-line Regimen Adult Proportion":
                d["First-line Regimen Adult Proportion"] = first_adult_prop
            if spec == "Second-line Regimen Adult Proportion":
                d["Second-line Regimen Adult Proportion"] = second_adult_prop
            if spec == "First-line Regimen Child Proportion":
                d["First-line Regimen Child Proportion"] = first_child_prop
            if spec == "Second-line Regimen child Proportion":
                d["Second-line Regimen Child Proportion"] = second_child_prop
            if spec == "First-line Regimen Adult Efficacy":
                d["First-line Regimen Adult Efficacy"] = round(first_adult_eff*100)
            if spec == "Second-line Regimen Adult Efficacy":
                d["Second-line Regimen Adult Efficacy"] = round(second_adult_eff*100)
            if spec == "First-line Regimen Child Efficacy":
                d["First-line Regimen Child Efficacy"] = round(first_child_eff*100)
            if spec == "Second-line Regimen Child Efficacy":
                d["Second-line Regimen Child Efficacy"] = round(second_child_eff*100)
        print(d)
    elif selected_year == '2013':
            spec_obj = conn.execute("select * from spec_2013_HIV where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
            regimen1_obj_A = conn.execute("select * from spec_2013_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and grp = 'A' COLLATE NOCASE").fetchall()
            regimen2_obj_A = conn.execute("select * from spec_2013_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and grp = 'A' COLLATE NOCASE").fetchall()
            regimen1_obj_B = conn.execute("select * from spec_2013_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and grp = 'B' COLLATE NOCASE").fetchall()
            regimen2_obj_B = conn.execute("select * from spec_2013_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and grp = 'B' COLLATE NOCASE").fetchall()

            # Original specification values
            adult_coverage = spec_obj[0][1] / 100
            child_coverage = spec_obj[0][4] / 100
            adult_daly = spec_obj[0][7]
            child_daly = spec_obj[0][8]
            overall_rate = spec_obj[0][9] / 100
            adult_rate = spec_obj[0][10] / 100
            child_rate = spec_obj[0][11] / 100

            # Group A values
            first_adult_distribution_A = 0.9624 #constant
            second_adult_distribution_A = 0.0376 #constant
            first_child_distribution_A = 0.9655 #constant
            second_child_distribution_A = 0.0345 #constant
            first_adult_prop_A = 0
            second_adult_prop_A = 0
            first_adult_eff_A = 0
            second_adult_eff_A = 0
            first_child_prop_A = 0
            second_child_prop_A = 0
            first_child_eff_A = 0
            second_child_eff_A = 0
            for k in regimen1_obj_A:
                first_adult_prop_A += k[2]/k[1]
                first_adult_eff_A += k[4]/k[1]
                first_child_prop_A += k[3]/k[1]
                first_child_eff_A += k[5]/k[1]
            for k in regimen2_obj_A:
                second_adult_prop_A += k[2]/k[1]
                second_adult_eff_A += k[4]/k[1]
                second_child_prop_A += k[3]/k[1]
                second_child_eff_A += k[5]/k[1]
            I_a1_A = (adult_daly * adult_coverage * (first_adult_distribution_A * first_adult_prop_A * first_adult_eff_A))/(1 - adult_coverage *(first_adult_distribution_A * first_adult_prop_A * first_adult_eff_A))
            I_a2_A = (adult_daly * adult_coverage * (second_adult_distribution_A * second_adult_prop_A * second_adult_eff_A))/(1 - adult_coverage *(second_adult_distribution_A * second_adult_prop_A * second_adult_eff_A))
            I_c1_A = (child_daly * child_coverage * (first_child_distribution_A * first_child_prop_A * first_child_eff_A))/(1 - child_coverage*(first_child_distribution_A * first_child_prop_A * first_child_eff_A))
            I_c2_A = (child_daly * child_coverage * (second_child_distribution_A * second_child_prop_A * second_child_eff_A))/(1 - child_coverage*(second_child_distribution_A * second_child_prop_A * second_child_eff_A))

            # Group B values
            first_adult_distribution_B = 0.8543 #constant
            second_adult_distribution_B = 0.1457 #constant
            first_child_distribution_B = 0.8210 #constant
            second_child_distribution_B = 0.1790 #constant
            first_adult_prop_B = 0
            second_adult_prop_B = 0
            first_adult_eff_B = 0
            second_adult_eff_B = 0
            first_child_prop_B = 0
            second_child_prop_B = 0
            first_child_eff_B = 0
            second_child_eff_B = 0
            for k in regimen1_obj_B:
                first_adult_prop_B += k[2]/k[1]
                first_adult_eff_B += k[4]/k[1]
                first_child_prop_B += k[3]/k[1]
                first_child_eff_B += k[5]/k[1]
            for k in regimen2_obj_B:
                second_adult_prop_B += k[2]/k[1]
                second_adult_eff_B += k[4]/k[1]
                second_child_prop_B += k[3]/k[1]
                second_child_eff_B += k[5]/k[1]
            I_a1_B = (adult_daly * adult_coverage * (first_adult_distribution_B * first_adult_prop_B * first_adult_eff_B))/(1 - adult_coverage *(first_adult_distribution_B * first_adult_prop_B * first_adult_eff_B))
            I_a2_B = (adult_daly * adult_coverage * (second_adult_distribution_B * second_adult_prop_B * second_adult_eff_B))/(1 - adult_coverage *(second_adult_distribution_B * second_adult_prop_B * second_adult_eff_B))
            I_c1_B = (child_daly * child_coverage * (first_child_distribution_B * first_child_prop_B * first_child_eff_B))/(1 - child_coverage*(first_child_distribution_B * first_child_prop_B * first_child_eff_B))
            I_c2_B = (child_daly * child_coverage * (second_child_distribution_B * second_child_prop_B * second_child_eff_B))/(1 - child_coverage*(second_child_distribution_B * second_child_prop_B * second_child_eff_B))
            I = I_a1_A + I_a2_A + I_c1_A + I_c2_A + I_a1_B + I_a2_B + I_c1_B + I_c2_B
            d = {}
            d["Original Impact Score"] = round(I, 2)
            for spec in selected_specification:
                if spec == "Treatment Coverage Adults":
                    d["Adults Needing Treatment"] = spec_obj[0][2]
                    d["Adults Receiving Treatment"] = spec_obj[0][3]
                if spec == "Treatment Coverage Children":
                    d["Children Needing Treatment"] = spec_obj[0][5]
                    d["Children Receiving Treatment"] = spec_obj[0][6]
                if spec == "Adult DALY":
                    d["Adult DALY"] = adult_daly
                if spec == "Child DALY":
                    d["Child DALY"] = child_daly
                if spec == "Overall Retention Rates":
                    d["Overall Retention Rates"] = round((overall_rate * 100),2)
                if spec == "Adult Retention Rates":
                    d["Adult Retention Rates"] = round((adult_rate * 100),2)
                if spec == "Child Retention Rates":
                    d["Child Retention Rates"] = round((child_rate * 100),2)
                if spec == "Group A First-line Adult Distribution":
                    d["Group A First-line Adult Distribution"] = round(first_adult_distribution_A*100,2)
                if spec == "Group A Second-line Adult Distribution":
                    d["Group A Second-line Adult Distribution"] = round(second_adult_distribution_A*100,2)
                if spec == "Group A First-line Child Distribution":
                    d["Group A First-line Child Distribution"] = round(first_child_distribution_A*100,2)
                if spec == "Group A Second-line Child Distribution":
                    d["Group A Second-line Child Distribution"] = round(second_child_distribution_A*100,2)
                if spec == "Group A First-line Regimen Adult Proportion":
                    d["Group A First-line Regimen Adult Proportion"] = first_adult_prop_A
                if spec == "Group A Second-line Regimen Adult Proportion":
                    d["Group A Second-line Regimen Adult Proportion"] = second_adult_prop_A
                if spec == "Group A First-line Regimen Child Proportion":
                    d["Group A First-line Regimen Child Proportion"] = first_child_prop_A
                if spec == "Group A Second-line Regimen child Proportion":
                    d["Group A Second-line Regimen Child Proportion"] = second_child_prop_A
                if spec == "Group A First-line Regimen Adult Efficacy":
                    d["Group A First-line Regimen Adult Efficacy"] = round(first_adult_eff_A*100)
                if spec == "Group A Second-line Regimen Adult Efficacy":
                    d["Group A Second-line Regimen Adult Efficacy"] = round(second_adult_eff_A*100)
                if spec == "Group A First-line Regimen Child Efficacy":
                    d["Group A First-line Regimen Child Efficacy"] = round(first_child_eff_A*100)
                if spec == "Group A Second-line Regimen Child Efficacy":
                    d["Group A Second-line Regimen Child Efficacy"] = round(second_child_eff_A*100)
                if spec == "Group B First-line Adult Distribution":
                    d["Group B First-line Adult Distribution"] = round(first_adult_distribution_B*100,2)
                if spec == "Group B Second-line Adult Distribution":
                    d["Group B Second-line Adult Distribution"] = round(second_adult_distribution_B*100,2)
                if spec == "Group B First-line Child Distribution":
                    d["Group B First-line Child Distribution"] = round(first_child_distribution_B*100,2)
                if spec == "Group B Second-line Child Distribution":
                    d["Group B Second-line Child Distribution"] = round(second_child_distribution_B*100,2)
                if spec == "Group B First-line Regimen Adult Proportion":
                    d["Group B First-line Regimen Adult Proportion"] = first_adult_prop_B
                if spec == "Group B Second-line Regimen Adult Proportion":
                    d["Group B Second-line Regimen Adult Proportion"] = second_adult_prop_B
                if spec == "Group B First-line Regimen Child Proportion":
                    d["Group B First-line Regimen Child Proportion"] = first_child_prop_B
                if spec == "Group B Second-line Regimen child Proportion":
                    d["Group B Second-line Regimen Child Proportion"] = second_child_prop_B
                if spec == "Group B First-line Regimen Adult Efficacy":
                    d["Group B First-line Regimen Adult Efficacy"] = round(first_adult_eff_B*100)
                if spec == "Group B Second-line Regimen Adult Efficacy":
                    d["Group B Second-line Regimen Adult Efficacy"] = round(second_adult_eff_B*100)
                if spec == "Group B First-line Regimen Child Efficacy":
                    d["Group B First-line Regimen Child Efficacy"] = round(first_child_eff_B*100)
                if spec == "Group B Second-line Regimen Child Efficacy":
                    d["Group B Second-line Regimen Child Efficacy"] = round(second_child_eff_B*100)
    elif selected_year == '2010':
        spec_obj = conn.execute("select * from spec_2010_HIV where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
        regimen1_obj_A_adult = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and adult = 1 and grp = 'A' COLLATE NOCASE").fetchall()
        regimen1_obj_A_child = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and child = 1 and grp = 'A' COLLATE NOCASE").fetchall()
        regimen2_obj_A_adult = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and adult = 1 and grp = 'A' COLLATE NOCASE").fetchall()
        regimen2_obj_A_child = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and child = 1 and grp = 'A' COLLATE NOCASE").fetchall()
        regimen1_obj_B_adult = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and adult = 1 and grp = 'B' COLLATE NOCASE").fetchall()
        regimen1_obj_B_child = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and child = 1 and grp = 'B' COLLATE NOCASE").fetchall()
        regimen2_obj_B_adult = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and adult = 1 and grp = 'B' COLLATE NOCASE").fetchall()
        regimen2_obj_B_child = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and child = 1 and grp = 'B' COLLATE NOCASE").fetchall()

        # Original specification values
        adult_coverage = spec_obj[0][1] / 100
        child_coverage = spec_obj[0][4] / 100
        adult_daly = spec_obj[0][7]
        child_daly = spec_obj[0][8]
        overall_rate = spec_obj[0][9] / 100
        adult_rate = spec_obj[0][10] / 100
        child_rate = spec_obj[0][11] / 100

        # Group A values
        first_adult_distribution_A = 0.9710 #constant
        second_adult_distribution_A = 0.0290 #constant
        first_child_distribution_A = 0.9680 #constant
        second_child_distribution_A = 0.0320 #constant
        first_adult_prop_A = 0
        second_adult_prop_A = 0
        first_adult_eff_A = 0
        second_adult_eff_A = 0
        first_child_prop_A = 0
        second_child_prop_A = 0
        first_child_eff_A = 0
        second_child_eff_A = 0
        for k in regimen1_obj_A_adult:
            first_adult_prop_A += k[2]/k[1]
            first_adult_eff_A += k[3]/k[1]
        for k in regimen1_obj_A_child:
            first_child_prop_A += k[2]/k[1]
            first_child_eff_A += k[3]/k[1]
        for k in regimen2_obj_A_adult:
            second_adult_prop_A += k[2]/k[1]
            second_adult_eff_A += k[3]/k[1]
        for k in regimen2_obj_A_child:
            second_child_prop_A += k[2]/k[1]
            second_child_eff_A += k[3]/k[1]
        I_a1_A = (adult_daly * adult_coverage * (first_adult_distribution_A * first_adult_prop_A * first_adult_eff_A))/(1 - adult_coverage *(first_adult_distribution_A * first_adult_prop_A * first_adult_eff_A))
        I_a2_A = (adult_daly * adult_coverage * (second_adult_distribution_A * second_adult_prop_A * second_adult_eff_A))/(1 - adult_coverage *(second_adult_distribution_A * second_adult_prop_A * second_adult_eff_A))
        I_c1_A = (child_daly * child_coverage * (first_child_distribution_A * first_child_prop_A * first_child_eff_A))/(1 - child_coverage*(first_child_distribution_A * first_child_prop_A * first_child_eff_A))
        I_c2_A = (child_daly * child_coverage * (second_child_distribution_A * second_child_prop_A * second_child_eff_A))/(1 - child_coverage*(second_child_distribution_A * second_child_prop_A * second_child_eff_A))

        # Group B values
        first_adult_distribution_B = 0.6910 #constant
        second_adult_distribution_B = 0.2780 #constant
        first_child_distribution_B = 0.7210 #constant
        second_child_distribution_B = 0.2490 #constant
        first_adult_prop_B = 0
        second_adult_prop_B = 0
        first_adult_eff_B = 0
        second_adult_eff_B = 0
        first_child_prop_B = 0
        second_child_prop_B = 0
        first_child_eff_B = 0
        second_child_eff_B = 0
        for k in regimen1_obj_B_adult:
            first_adult_prop_B += k[2]/k[1]
            first_adult_eff_B += k[3]/k[1]
        for k in regimen1_obj_B_child:
            first_child_prop_B += k[2]/k[1]
            first_child_eff_B += k[3]/k[1]
        for k in regimen2_obj_B_adult:
            second_adult_prop_B += k[2]/k[1]
            second_adult_eff_B += k[3]/k[1]
        for k in regimen2_obj_B_child:
            second_child_prop_B += k[2]/k[1]
            second_child_eff_B += k[3]/k[1]
        I_a1_B = (adult_daly * adult_coverage * (first_adult_distribution_B * first_adult_prop_B * first_adult_eff_B))/(1 - adult_coverage *(first_adult_distribution_B * first_adult_prop_B * first_adult_eff_B))
        I_a2_B = (adult_daly * adult_coverage * (second_adult_distribution_B * second_adult_prop_B * second_adult_eff_B))/(1 - adult_coverage *(second_adult_distribution_B * second_adult_prop_B * second_adult_eff_B))
        I_c1_B = (child_daly * child_coverage * (first_child_distribution_B * first_child_prop_B * first_child_eff_B))/(1 - child_coverage*(first_child_distribution_B * first_child_prop_B * first_child_eff_B))
        I_c2_B = (child_daly * child_coverage * (second_child_distribution_B * second_child_prop_B * second_child_eff_B))/(1 - child_coverage*(second_child_distribution_B * second_child_prop_B * second_child_eff_B))
        I = I_a1_A + I_a2_A + I_c1_A + I_c2_A + I_a1_B + I_a2_B + I_c1_B + I_c2_B
        d["Original Impact Score"] = round(I, 2)
        for spec in selected_specification:
            if spec == "Treatment Coverage Adults":
                d["Adults Needing Treatment"] = spec_obj[0][2]
                d["Adults Receiving Treatment"] = spec_obj[0][3]
            if spec == "Treatment Coverage Children":
                d["Children Needing Treatment"] = spec_obj[0][5]
                d["Children Receiving Treatment"] = spec_obj[0][6]
            if spec == "Adult DALY":
                d["Adult DALY"] = adult_daly
            if spec == "Child DALY":
                d["Child DALY"] = child_daly
            if spec == "Overall Retention Rates":
                d["Overall Retention Rates"] = round((overall_rate * 100),2)
            if spec == "Adult Retention Rates":
                d["Adult Retention Rates"] = round((adult_rate * 100),2)
            if spec == "Child Retention Rates":
                d["Child Retention Rates"] = round((child_rate * 100),2)
            if spec == "Group A First-line Adult Distribution":
                d["Group A First-line Adult Distribution"] = round(first_adult_distribution_A*100,2)
            if spec == "Group A Second-line Adult Distribution":
                d["Group A Second-line Adult Distribution"] = round(second_adult_distribution_A*100,2)
            if spec == "Group A First-line Child Distribution":
                d["Group A First-line Child Distribution"] = round(first_child_distribution_A*100,2)
            if spec == "Group A Second-line Child Distribution":
                d["Group A Second-line Child Distribution"] = round(second_child_distribution_A*100,2)
            if spec == "Group A First-line Regimen Adult Proportion":
                d["Group A First-line Regimen Adult Proportion"] = first_adult_prop_A
            if spec == "Group A Second-line Regimen Adult Proportion":
                d["Group A Second-line Regimen Adult Proportion"] = second_adult_prop_A
            if spec == "Group A First-line Regimen Child Proportion":
                d["Group A First-line Regimen Child Proportion"] = first_child_prop_A
            if spec == "Group A Second-line Regimen child Proportion":
                d["Group A Second-line Regimen Child Proportion"] = second_child_prop_A
            if spec == "Group A First-line Regimen Adult Efficacy":
                d["Group A First-line Regimen Adult Efficacy"] = round(first_adult_eff_A*100)
            if spec == "Group A Second-line Regimen Adult Efficacy":
                d["Group A Second-line Regimen Adult Efficacy"] = round(second_adult_eff_A*100)
            if spec == "Group A First-line Regimen Child Efficacy":
                d["Group A First-line Regimen Child Efficacy"] = round(first_child_eff_A*100)
            if spec == "Group A Second-line Regimen Child Efficacy":
                d["Group A Second-line Regimen Child Efficacy"] = round(second_child_eff_A*100)
            if spec == "Group B First-line Adult Distribution":
                d["Group B First-line Adult Distribution"] = round(first_adult_distribution_B*100,2)
            if spec == "Group B Second-line Adult Distribution":
                d["Group B Second-line Adult Distribution"] = round(second_adult_distribution_B*100,2)
            if spec == "Group B First-line Child Distribution":
                d["Group B First-line Child Distribution"] = round(first_child_distribution_B*100,2)
            if spec == "Group B Second-line Child Distribution":
                d["Group B Second-line Child Distribution"] = round(second_child_distribution_B*100,2)
            if spec == "Group B First-line Regimen Adult Proportion":
                d["Group B First-line Regimen Adult Proportion"] = first_adult_prop_B
            if spec == "Group B Second-line Regimen Adult Proportion":
                d["Group B Second-line Regimen Adult Proportion"] = second_adult_prop_B
            if spec == "Group B First-line Regimen Child Proportion":
                d["Group B First-line Regimen Child Proportion"] = first_child_prop_B
            if spec == "Group B Second-line Regimen child Proportion":
                d["Group B Second-line Regimen Child Proportion"] = second_child_prop_B
            if spec == "Group B First-line Regimen Adult Efficacy":
                d["Group B First-line Regimen Adult Efficacy"] = round(first_adult_eff_B*100)
            if spec == "Group B Second-line Regimen Adult Efficacy":
                d["Group B Second-line Regimen Adult Efficacy"] = round(second_adult_eff_B*100)
            if spec == "Group B First-line Regimen Child Efficacy":
                d["Group B First-line Regimen Child Efficacy"] = round(first_child_eff_B*100)
            if spec == "Group B Second-line Regimen Child Efficacy":
                d["Group B Second-line Regimen Child Efficacy"] = round(second_child_eff_B*100)
    return d

# calculate Index for worms
@app.route('/get_spec_worms', methods=['GET', 'POST'])
def getSpecWorms():
    conn = connect_db()
    selected_country = request.get_json()["selected_country"]
    selected_disease = request.get_json()["selected_disease"]
    selected_drug = request.get_json()["selected_drug"]
    selected_company = request.get_json()["selected_company"]
    selected_specification = request.get_json()["selected_specification"]
    selected_year = request.get_json()["selected_year"]
    print("SelectedYear: " + selected_year)
    # selected_specification = ['Adult', 'Children']
    spec_obj = conn.execute(
        f"select worm_preSac_coverage, worm_Sac_coverage, roundworm_prevalance_child, roundworm_prevalance_adult, roundworm_Efficacy_ALB, roundworm_Efficacy_Mbd, roundworm_Efficacy_Ivm_Alb, roundworm_DALY_child, roundworm_DALY_adult, hookworm_prevalance_child, hookworm_prevalance_adult, hookworm_Efficacy_ALB, hookworm_Efficacy_Mbd, hookworm_DALY_child, hookworm_DALY_adult, whipworm_prevalance_child, whipworm_prevalance_adult, whipworm_Efficacy_ALB, whipworm_Efficacy_Mbd, whipworm_Efficacy_Ivm_Alb, whipworm_DALY_child, whipworm_DALY_adult from spec_{selected_year}_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

    print(spec_obj)

    worm_preSac_coverage = 0
    worm_Sac_coverage = 0
    prevalence_child = 0
    prevalence_adult = 0
    Efficacy = 0
    DALY_child = 0
    DALY_adult = 0

    if (len(spec_obj) > 0):
        # get treatment coverage data from db based on country selected
        worm_preSac_coverage = spec_obj[0][0] / 100
        worm_Sac_coverage = spec_obj[0][1] / 100

        if (selected_disease == 'Roundworm'):
            # get prevalence data from db based on country and disease selected
            prevalence_child = spec_obj[0][2] / 100
            prevalence_adult = spec_obj[0][3] / 100
            # get efficacy data from db based on country, disease, and drug selected
            if selected_drug == "Albendazole (ALB)":
                Efficacy = spec_obj[0][4] / 100
            elif selected_drug == "Mebendazole (MBD)":
                Efficacy = spec_obj[0][5] / 100
            elif selected_drug == "Ivermectin (IVM)":
                Efficacy = spec_obj[0][6] / 100
            # get DALY data from db based on country and disease selected
            DALY_child = spec_obj[0][7]
            DALY_adult = spec_obj[0][8]

        elif (selected_disease == 'Hookworm'):
            # get prevalence data from db based on country and disease selected
            prevalence_child = spec_obj[0][9] / 100
            prevalence_adult = spec_obj[0][10] / 100
            # get efficacy data from db based on country, disease, and drug selected
            if selected_drug == "Albendazole (ALB)":
                Efficacy = spec_obj[0][11] / 100
            elif selected_drug == "Mebendazole (MBD)":
                Efficacy = spec_obj[0][12] / 100
            # get DALY data from db based on country and disease selected
            DALY_child = spec_obj[0][13]
            DALY_adult = spec_obj[0][14]

        elif (selected_disease == 'Whipworm'):
            # get prevalence data from db based on country and disease selected
            prevalence_child = spec_obj[0][15] / 100
            prevalence_adult = spec_obj[0][16] / 100
            # get efficacy data from db based on country, disease, and drug selected
            if selected_drug == "Albendazole (ALB)":
                Efficacy = spec_obj[0][17] / 100
            elif selected_drug == "Mebendazole (MBD)":
                Efficacy = spec_obj[0][18] / 100
            elif selected_drug == "Ivermectin (IVM)":
                Efficacy = spec_obj[0][19] / 100
            # get DALY data from db based on country and disease selected
            DALY_child = spec_obj[0][20]
            DALY_adult = spec_obj[0][21]

    I = 0
    d = {}
    for each_spec in selected_specification:
        # Set prevalence values
        if each_spec == "Prevalence for 1-4 year olds":
            d["Prevalence for 1-4 year olds"] = float(Decimal(str(prevalence_child)) * 100)
        if each_spec == "Prevalence for 5-14 year olds":
            d["Prevalence for 5-14 year olds"] = float(Decimal(str(prevalence_adult)) * 100)

        # Set treatment coverage values
        if each_spec == "Pre-Sac Treatment Coverage":
            d["Pre-Sac Treatment Coverage"] = float(Decimal(str(worm_preSac_coverage)) * 100)
        if each_spec == "SAC Treatment Coverage":
            d["SAC Treatment Coverage"] = float(Decimal(str(worm_Sac_coverage)) * 100)

        # Set efficacy values
        if each_spec == "Efficacy":
            d["Efficacy"] = float(Decimal(str(Efficacy)) * 100)

        # Set DALY values
        if each_spec == "DALYs for 1-4 year olds":
            d["DALYs for 1-4 year olds"] = DALY_child
        if each_spec == "DALYs for 5-14 year olds":
            d["DALYs for 5-14 year olds"] = DALY_adult

    # Compute Impact Score
    worm_child_I = (((DALY_child * worm_preSac_coverage * Efficacy) / (
            1 - (worm_preSac_coverage * Efficacy))) * prevalence_child)

    worm_adult_I = (((DALY_adult * worm_Sac_coverage * Efficacy) / (
            1 - (worm_Sac_coverage * Efficacy))) * prevalence_adult)

    I = I + worm_child_I + worm_adult_I

    d["Original Impact Score"] = round(I, 2)
    print("Original Impact Score")
    print(I)
    print(d)
    conn.close()
    return json.dumps(d)


# calculate Index for other
@app.route('/get_spec_other', methods=['GET', 'POST'])
def getSpecOther():
    conn = connect_db()
    selected_country = request.get_json()["selected_country"]
    selected_disease = request.get_json()["selected_disease"]
    selected_drug = request.get_json()["selected_drug"]
    selected_year = request.get_json()["selected_year"]
    print("SelectedYear: " + selected_year)
    # selected_company = request.get_json()["selected_company"]
    selected_specification = request.get_json()["selected_specification"]

    spec_obj = conn.execute(
        f"select schi_prevalance, schi_coverage, schi_Efficacy, schi_DALY, onch_prevalance, onch_coverage, onch_Efficacy, onch_DALY, LF_prevalance, LF_coverage, LF_Efficacy_DEC, LF_Efficacy_DEC_ALB, LF_Efficacy_IVM_ALB, LF_DALY from spec_{selected_year}_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

    prevalence = 0
    treatment_coverage = 0
    Efficacy = 0
    DALY = 0

    if (len(spec_obj) > 0):
        if (selected_disease == 'Schistosomiasis'):
            # get prevalence data from db based on country and disease selected
            prevalence = spec_obj[0][0] / 100
            # get treatment coverage data from db based on country and disease selected
            treatment_coverage = spec_obj[0][1] / 100
            # get efficacy data from db based on country and disease selected
            Efficacy = spec_obj[0][2] / 100
            # get DALY data from db based on country and disease selected
            DALY = spec_obj[0][3]

        elif (selected_disease == 'Onchoceriasis'):
            # get prevalence data from db based on country and disease selected
            prevalence = spec_obj[0][4] / 100
            # get treatment coverage data from db based on country and disease selected
            treatment_coverage = spec_obj[0][5] / 100
            # get efficacy data from db based on country and disease selected
            Efficacy = spec_obj[0][6] / 100
            # get DALY data from db based on country and disease selected
            DALY = spec_obj[0][7]

        elif (selected_disease == 'LF'):
            # get prevalence data from db based on country and disease selected
            prevalence = spec_obj[0][8] / 100
            # get treatment coverage data from db based on country and disease selected
            treatment_coverage = spec_obj[0][9] / 100
            # get efficacy data from db based on country, disease, and drug selected
            if selected_drug == 'Diethylcarbamazine (DEC)':
                Efficacy = spec_obj[0][10] / 100
            elif selected_drug == "Albendazole (ALB)":
                Efficacy = spec_obj[0][11] / 100
            elif selected_drug == "Ivermectin (IVM)":
                Efficacy = spec_obj[0][12] / 100
            # get DALY data from db based on country and disease selected
            DALY = spec_obj[0][13]

    d = {}
    I = 0
    for each_spec in selected_specification:
        # Set prevalence value
        if each_spec == "Prevalence":
            d["Prevalence"] = float(Decimal(str(prevalence)) * 100)

        # Set treatment coverage value
        if each_spec == "Treatment Coverage":
            d["Treatment Coverage"] = float(Decimal(str(treatment_coverage)) * 100)

        # Set efficacy value
        if each_spec == "Efficacy":
            d["Efficacy"] = float(Decimal(str(Efficacy)) * 100)

        # Set DALY value
        if each_spec == "DALY":
            d["DALY"] = DALY

    # Compute Impact Score
    I = (((DALY * treatment_coverage * Efficacy) / (
            1 - (treatment_coverage * Efficacy))) * prevalence)

    d["Original Impact Score"] = round(I, 2)
    print("Original Impact Score")
    print(I)
    print(d)
    conn.close()
    return json.dumps(d)


# specification end

# Need to add new API for Results page
@app.route('/get_result', methods=['GET', 'POST'])
def getResults():
    print("In Results")
    conn = connect_db()
    # selected_country = request.get_json()["selected_country"]
    # selected_disease = request.get_json()["selected_disease"]
    # selected_company = request.get_json()["selected_company"]
    # selected_drug = request.get_json()["selected_drug"]
    updated_spec = request.get_json()["updated_specification"]
    print(request.get_json())
    # print("Updated Spec",updated_spec)
    options_obj = updated_spec["dict_dataa"]
    selected_country = options_obj["Country"]
    selected_company = options_obj["Company"]
    selected_disease = options_obj["Disease"]
    selected_year = options_obj["Year"]
    selected_drug = options_obj["Drug"]
    sd = selected_drug[selected_drug.find("(") + 1:selected_drug.find(")")]
    selected_state = options_obj["state"]
    # print("selected_country",selected_country)
    # print("selected_disease", selected_disease)
    updated_specification = updated_spec["dict_1"]
    print("SelectedYear: " + selected_year)
    if (selected_disease == "Whipworm"):
        d = {}
        spec_obj = conn.execute(
            f"select worm_preSac_coverage, worm_Sac_coverage, roundworm_prevalance_child, roundworm_prevalance_adult, roundworm_Efficacy_ALB, roundworm_Efficacy_Mbd, roundworm_Efficacy_Ivm_Alb, roundworm_DALY_child, roundworm_DALY_adult, hookworm_prevalance_child, hookworm_prevalance_adult, hookworm_Efficacy_ALB, hookworm_Efficacy_Mbd, hookworm_DALY_child, hookworm_DALY_adult, whipworm_prevalance_child, whipworm_prevalance_adult, whipworm_Efficacy_ALB, whipworm_Efficacy_Mbd, whipworm_Efficacy_Ivm_Alb, whipworm_DALY_child, whipworm_DALY_adult from spec_{selected_year}_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

        print(spec_obj)

        worm_preSac_coverage = 0
        worm_Sac_coverage = 0
        prevalence_child = 0
        prevalence_adult = 0
        Efficacy = 0
        DALY_child = 0
        DALY_adult = 0

        if (len(spec_obj) > 0):
            # get treatment coverage data from db based on country selected
            worm_preSac_coverage = spec_obj[0][0] / 100
            worm_Sac_coverage = spec_obj[0][1] / 100

            # if (selected_disease == 'Whipworm'):
            # get prevalence data from db based on country and disease selected
            prevalence_child = spec_obj[0][15] / 100
            prevalence_adult = spec_obj[0][16] / 100
            # get efficacy data from db based on country, disease, and drug selected
            if selected_drug == "Albendazole (ALB)":
                Efficacy = spec_obj[0][17] / 100
            elif selected_drug == "Mebendazole (MBD)":
                Efficacy = spec_obj[0][18] / 100
            elif selected_drug == "Ivermectin (IVM)":
                Efficacy = spec_obj[0][19] / 100
            # get DALY data from db based on country and disease selected
            DALY_child = spec_obj[0][20]
            DALY_adult = spec_obj[0][21]

        newI = 0
        for each_spec in updated_specification:
            print(each_spec)

            if each_spec == "Prevealence for 1-4 year olds":
                prevalence_child = updated_specification["Prevealence for 1-4 year olds"] / 100

            if each_spec == "Prevealence for 5-14 year olds":
                prevalence_adult = updated_specification["Prevealence for 5-14 year olds"] / 100

            if each_spec == "Pre-Sac Treatment Coverage":
                worm_preSac_coverage = updated_specification["Pre-Sac Treatment Coverage"] / 100

            if each_spec == "SAC Treatment Coverage":
                worm_Sac_coverage = updated_specification["SAC Treatment Coverage"] / 100

            if each_spec == "Efficacy":
                Efficacy = updated_specification["Efficacy"] / 100

            if each_spec == "DALYs for 1-4 year old":
                DALY_child = updated_specification["DALYs for 1-4 year old"]

            if each_spec == "DALYs for 5-14 year old":
                DALY_adult = updated_specification["DALYs for 5-14 year old"]

            if each_spec == "Original Impact Score":
                origI = updated_specification["Original Impact Score"]

        # calculate new impact score of whipworm

        worm_child_I_newI = (((DALY_child * worm_preSac_coverage * Efficacy) / (
                1 - (worm_preSac_coverage * Efficacy))) * prevalence_child)

        worm_adult_I_newI = (((DALY_adult * worm_Sac_coverage * Efficacy) / (
                1 - (worm_Sac_coverage * Efficacy))) * prevalence_adult)

        newI = newI + worm_child_I_newI + worm_adult_I_newI

        d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)
        print(d)

        d["Selected Country"] = selected_country
        d["Selected Company"] = selected_company
        d["Selected Disease"] = selected_disease
        d["Selected Drug"] = selected_drug
        d["Original Impact Score"] = origI
        # d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)

        # if (selected_state == 'Country'):
        #     countries_obj = conn.execute("select country,whipworm from country2015").fetchall()
        #     countries_dict= {}
        #     for countries in countries_obj:
        #         temp = countries[0].lstrip();
        #         if (temp != selected_country):
        #             countries_dict[temp] = countries[1];
        #     d["OTHER COUNTRIES"] = countries_dict
        # print(countries_obj)

        if (selected_state == 'Company'):
            company_obj = conn.execute(
                f"select company,whipworm from drugr{selected_year} where whipworm > 0").fetchall()
            # print(countries_obj[0])
            company_dict = {}
            for company in company_obj:
                temp = company[0].lstrip();
                if (temp != selected_company):
                    company_dict[temp] = company[1];
            del company_dict["Unmet Need"]
            d["OTHER COMPANIES"] = company_dict

        if (selected_state == 'Disease'):
            disease_obj = conn.execute(
                f"select tb , malaria, hiv, roundworm , hookworm , whipworm ,  schistosomiasis ,  onchoceriasis , lf from country{selected_year} where country = ' " + selected_country + "' ").fetchall()
            disease_dict = {"TB": 0, "Malaria": 0, "HIV": 0, "Roundworm": 0, "Hookworm": 0, "Whipworm": 0,
                            "Schistosomiasis": 0, "Onchoceriasis": 0, "LF": 0}
            disease_dict["TB"] = round(disease_obj[0][0], 2)
            disease_dict["Malaria"] = round(disease_obj[0][1], 2)
            disease_dict["HIV"] = round(disease_obj[0][2], 2)
            disease_dict["Roundworm"] = round(disease_obj[0][3], 2)
            disease_dict["Hookworm"] = round(disease_obj[0][4], 2)
            disease_dict["Whipworm"] = round(disease_obj[0][5], 2)
            disease_dict["Schistosomiasis"] = round(disease_obj[0][6], 2)
            disease_dict["Onchocerciasis"] = round(disease_obj[0][7], 2)
            disease_dict["LF"] = round(disease_obj[0][8], 2)

            del disease_dict[selected_disease]
            # print(disease_dict)
            d["OTHER DISEASES"] = disease_dict

        if (selected_state == 'Drug'):
            drug_obj = conn.execute(
                f"select drug,sum(score)from drug{selected_year} where disease='Whipworm' group by drug").fetchall()
            drug_dict = {}
            print(selected_drug)
            for drgobjs in drug_obj:
                # print (drgobjs)
                # print (drgobjs[0])
                # print (drgobjs[1])
                if (drgobjs[0] != selected_drug):
                    drug_dict[drgobjs[0]] = drgobjs[1];
            d["OTHER DRUGS"] = drug_dict
            # print(countries_obj)
        print(d)
        # conn.close()

    if (selected_disease == "Hookworm"):
        d = {}
        spec_obj = conn.execute(
            f"select worm_preSac_coverage, worm_Sac_coverage, roundworm_prevalance_child, roundworm_prevalance_adult, roundworm_Efficacy_ALB, roundworm_Efficacy_Mbd, roundworm_Efficacy_Ivm_Alb, roundworm_DALY_child, roundworm_DALY_adult, hookworm_prevalance_child, hookworm_prevalance_adult, hookworm_Efficacy_ALB, hookworm_Efficacy_Mbd, hookworm_DALY_child, hookworm_DALY_adult, whipworm_prevalance_child, whipworm_prevalance_adult, whipworm_Efficacy_ALB, whipworm_Efficacy_Mbd, whipworm_Efficacy_Ivm_Alb, whipworm_DALY_child, whipworm_DALY_adult from spec_{selected_year}_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

        print(spec_obj)

        worm_preSac_coverage = 0
        worm_Sac_coverage = 0
        prevalence_child = 0
        prevalence_adult = 0
        Efficacy = 0
        DALY_child = 0
        DALY_adult = 0

        if (len(spec_obj) > 0):
            # get treatment coverage data from db based on country selected
            worm_preSac_coverage = spec_obj[0][0] / 100
            worm_Sac_coverage = spec_obj[0][1] / 100

            # if (selected_disease == 'Hookworm'):
            # get prevalence data from db based on country and disease selected
            prevalence_child = spec_obj[0][9] / 100
            prevalence_adult = spec_obj[0][10] / 100
            # get efficacy data from db based on country, disease, and drug selected
            if selected_drug == "Albendazole (ALB)":
                Efficacy = spec_obj[0][11] / 100
            elif selected_drug == "Mebendazole (MBD)":
                Efficacy = spec_obj[0][12] / 100
            # get DALY data from db based on country and disease selected
            DALY_child = spec_obj[0][13]
            DALY_adult = spec_obj[0][14]

        newI = 0
        for each_spec in updated_specification:
            print(each_spec)

            if each_spec == "Prevealence for 1-4 year olds":
                prevalence_child = updated_specification["Prevealence for 1-4 year olds"] / 100

            if each_spec == "Prevealence for 5-14 year olds":
                prevalence_adult = updated_specification["Prevealence for 5-14 year olds"] / 100

            if each_spec == "Pre-Sac Treatment Coverage":
                worm_preSac_coverage = updated_specification["Pre-Sac Treatment Coverage"] / 100

            if each_spec == "SAC Treatment Coverage":
                worm_Sac_coverage = updated_specification["SAC Treatment Coverage"] / 100

            if each_spec == "Efficacy":
                Efficacy = updated_specification["Efficacy"] / 100

            if each_spec == "DALYs for 1-4 year old":
                DALY_child = updated_specification["DALYs for 1-4 year old"]

            if each_spec == "DALYs for 5-14 year old":
                DALY_adult = updated_specification["DALYs for 5-14 year old"]

            if each_spec == "Original Impact Score":
                origI = updated_specification["Original Impact Score"]

        # calculate new impact score for Hookworm

        # calculate new impact score of whipworm

        worm_child_I_newI = (((DALY_child * worm_preSac_coverage * Efficacy) / (
                1 - (worm_preSac_coverage * Efficacy))) * prevalence_child)

        worm_adult_I_newI = (((DALY_adult * worm_Sac_coverage * Efficacy) / (
                1 - (worm_Sac_coverage * Efficacy))) * prevalence_adult)

        newI = newI + worm_child_I_newI + worm_adult_I_newI

        d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)
        print(d)

        d["Selected Country"] = selected_country
        d["Selected Company"] = selected_company
        d["Selected Disease"] = selected_disease
        d["Selected Drug"] = selected_drug
        d["Original Impact Score"] = origI
        # d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)

        # if (selected_state == 'Country'):
        #     countries_obj = conn.execute("select country,hookworm from country2015").fetchall()
        #     countries_dict= {}
        #     for countries in countries_obj:
        #         temp = countries[0].lstrip();
        #         if (temp != selected_country):
        #             countries_dict[temp] = countries[1];
        #     d["OTHER COUNTRIES"] = countries_dict
        # print(countries_obj)

        if (selected_state == 'Company'):
            company_obj = conn.execute(f"select company,hookworm from drugr{selected_year} where hookworm > 0").fetchall()
            # print(countries_obj[0])
            company_dict = {}
            for company in company_obj:
                temp = company[0].lstrip();
                if (temp != selected_company):
                    company_dict[temp] = company[1];
            del company_dict["Unmet Need"]
            d["OTHER COMPANIES"] = company_dict

        if (selected_state == 'Disease'):
            disease_obj = conn.execute(
                f"select tb , malaria, hiv, roundworm , hookworm , whipworm ,  schistosomiasis ,  onchoceriasis , lf from country{selected_year} where country = ' " + selected_country + "' ").fetchall()
            disease_dict = {"TB": 0, "Malaria": 0, "HIV": 0, "Roundworm": 0, "Hookworm": 0, "Whipworm": 0,
                            "Schistosomiasis": 0, "Onchoceriasis": 0, "LF": 0}
            disease_dict["TB"] = round(disease_obj[0][0], 2)
            disease_dict["Malaria"] = round(disease_obj[0][1], 2)
            disease_dict["HIV"] = round(disease_obj[0][2], 2)
            disease_dict["Roundworm"] = round(disease_obj[0][3], 2)
            disease_dict["Hookworm"] = round(disease_obj[0][4], 2)
            disease_dict["Whipworm"] = round(disease_obj[0][5], 2)
            disease_dict["Schistosomiasis"] = round(disease_obj[0][6], 2)
            disease_dict["Onchocerciasis"] = round(disease_obj[0][7], 2)
            disease_dict["LF"] = round(disease_obj[0][8], 2)

            del disease_dict[selected_disease]
            # print(disease_dict)
            d["OTHER DISEASES"] = disease_dict

        if (selected_state == 'Drug'):
            drug_obj = conn.execute(
                f"select drug,sum(score)from drug{selected_year} where disease='Hookworm' group by drug").fetchall()
            drug_dict = {}
            print(selected_drug)
            for drgobjs in drug_obj:
                # print (drgobjs)
                # print (drgobjs[0])
                # print (drgobjs[1])
                if (drgobjs[0] != selected_drug):
                    drug_dict[drgobjs[0]] = drgobjs[1];
            d["OTHER DRUGS"] = drug_dict
            # print(countries_obj)
        print(d)

    if (selected_disease == "Roundworm"):
        d = {}
        spec_obj = conn.execute(
            f"select worm_preSac_coverage, worm_Sac_coverage, roundworm_prevalance_child, roundworm_prevalance_adult, roundworm_Efficacy_ALB, roundworm_Efficacy_Mbd, roundworm_Efficacy_Ivm_Alb, roundworm_DALY_child, roundworm_DALY_adult, hookworm_prevalance_child, hookworm_prevalance_adult, hookworm_Efficacy_ALB, hookworm_Efficacy_Mbd, hookworm_DALY_child, hookworm_DALY_adult, whipworm_prevalance_child, whipworm_prevalance_adult, whipworm_Efficacy_ALB, whipworm_Efficacy_Mbd, whipworm_Efficacy_Ivm_Alb, whipworm_DALY_child, whipworm_DALY_adult from spec_{selected_year}_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

        print(spec_obj)

        worm_preSac_coverage = 0
        worm_Sac_coverage = 0
        prevalence_child = 0
        prevalence_adult = 0
        Efficacy = 0
        DALY_child = 0
        DALY_adult = 0

        if (len(spec_obj) > 0):
            # get treatment coverage data from db based on country selected
            worm_preSac_coverage = spec_obj[0][0] / 100
            worm_Sac_coverage = spec_obj[0][1] / 100

            # if (selected_disease == 'Roundworm'):
            # get prevalence data from db based on country and disease selected
            prevalence_child = spec_obj[0][2] / 100
            prevalence_adult = spec_obj[0][3] / 100
            # get efficacy data from db based on country, disease, and drug selected
            if selected_drug == "Albendazole (ALB)":
                Efficacy = spec_obj[0][4] / 100
            elif selected_drug == "Mebendazole (MBD)":
                Efficacy = spec_obj[0][5] / 100
            elif selected_drug == "Ivermectin (IVM)":
                Efficacy = spec_obj[0][6] / 100
            # get DALY data from db based on country and disease selected
            DALY_child = spec_obj[0][7]
            DALY_adult = spec_obj[0][8]

        newI = 0
        for each_spec in updated_specification:
            print(each_spec)

            if each_spec == "Prevealence for 1-4 year olds":
                prevalence_child = updated_specification["Prevealence for 1-4 year olds"] / 100

            if each_spec == "Prevealence for 5-14 year olds":
                prevalence_adult = updated_specification["Prevealence for 5-14 year olds"] / 100

            if each_spec == "Pre-Sac Treatment Coverage":
                worm_preSac_coverage = updated_specification["Pre-Sac Treatment Coverage"] / 100

            if each_spec == "SAC Treatment Coverage":
                worm_Sac_coverage = updated_specification["SAC Treatment Coverage"] / 100

            if each_spec == "Efficacy":
                Efficacy = updated_specification["Efficacy"] / 100

            if each_spec == "DALYs for 1-4 year old":
                DALY_child = updated_specification["DALYs for 1-4 year old"]

            if each_spec == "DALYs for 5-14 year old":
                DALY_adult = updated_specification["DALYs for 5-14 year old"]

            if each_spec == "Original Impact Score":
                origI = updated_specification["Original Impact Score"]

        # calculate new impact score for Roundworm

        worm_child_I_newI = (((DALY_child * worm_preSac_coverage * Efficacy) / (
                1 - (worm_preSac_coverage * Efficacy))) * prevalence_child)

        worm_adult_I_newI = (((DALY_adult * worm_Sac_coverage * Efficacy) / (
                1 - (worm_Sac_coverage * Efficacy))) * prevalence_adult)

        newI = newI + worm_child_I_newI + worm_adult_I_newI

        d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)
        print(d)

        d["Selected Country"] = selected_country
        d["Selected Company"] = selected_company
        d["Selected Disease"] = selected_disease
        d["Selected Drug"] = selected_drug
        d["Original Impact Score"] = origI
        # d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)

        # if (selected_state == 'Country'):
        #     countries_obj = conn.execute("select country,roundworm from country2015").fetchall()
        #     countries_dict= {}
        #     for countries in countries_obj:
        #         temp = countries[0].lstrip();
        #         if (temp != selected_country):
        #             countries_dict[temp] = countries[1];
        #     d["OTHER COUNTRIES"] = countries_dict
        # print(countries_obj)

        if (selected_state == 'Company'):
            company_obj = conn.execute(f"select company,roundworm from drugr{selected_year} where roundworm > 0").fetchall()
            # print(countries_obj[0])
            company_dict = {}
            for company in company_obj:
                temp = company[0].lstrip();
                if (temp != selected_company):
                    company_dict[temp] = company[1];

            del company_dict["Unmet Need"]
            d["OTHER COMPANIES"] = company_dict

        if (selected_state == 'Disease'):
            disease_obj = conn.execute(
                f"select tb , malaria, hiv, roundworm , hookworm , whipworm ,  schistosomiasis ,  onchoceriasis , lf from country{selected_year} where country = ' " + selected_country + "' ").fetchall()
            disease_dict = {"TB": 0, "Malaria": 0, "HIV": 0, "Roundworm": 0, "Hookworm": 0, "Whipworm": 0,
                            "Schistosomiasis": 0, "Onchoceriasis": 0, "LF": 0}
            disease_dict["TB"] = round(disease_obj[0][0], 2)
            disease_dict["Malaria"] = round(disease_obj[0][1], 2)
            disease_dict["HIV"] = round(disease_obj[0][2], 2)
            disease_dict["Roundworm"] = round(disease_obj[0][3], 2)
            disease_dict["Hookworm"] = round(disease_obj[0][4], 2)
            disease_dict["Whipworm"] = round(disease_obj[0][5], 2)
            disease_dict["Schistosomiasis"] = round(disease_obj[0][6], 2)
            disease_dict["Onchocerciasis"] = round(disease_obj[0][7], 2)
            disease_dict["LF"] = round(disease_obj[0][8], 2)

            del disease_dict[selected_disease]
            # print(disease_dict)
            d["OTHER DISEASES"] = disease_dict

        if (selected_state == 'Drug'):
            drug_obj = conn.execute(
                f"select drug,sum(score)from drug{selected_year} where disease='Roundworm' group by drug").fetchall()
            drug_dict = {}
            print(selected_drug)
            for drgobjs in drug_obj:
                # print (drgobjs)
                # print (drgobjs[0])
                # print (drgobjs[1])
                if (drgobjs[0] != selected_drug):
                    drug_dict[drgobjs[0]] = drgobjs[1];
            d["OTHER DRUGS"] = drug_dict
            # print(countries_obj)
        print(d)

    if (selected_disease == "Schistosomiasis"):
        d = {}
        spec_obj = conn.execute(
            f"select schi_prevalance, schi_coverage, schi_Efficacy, schi_DALY from spec_{selected_year}_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

        prevalence = 0
        treatment_coverage = 0
        Efficacy = 0
        DALY = 0

        if (len(spec_obj) > 0):
            if (selected_disease == 'Schistosomiasis'):
                prevalence = spec_obj[0][0] / 100
                treatment_coverage = spec_obj[0][1] / 100
                Efficacy = spec_obj[0][2] / 100
                DALY = spec_obj[0][3]

        newI = 0
        for each_spec in updated_specification:
            if each_spec == "Prevalence":
                prevalence = updated_specification["Prevalence"] / 100
            if each_spec == "Treatment Coverage":
                treatment_coverage = updated_specification["Treatment Coverage"] / 100
            if each_spec == "Efficacy":
                updated_specification["Efficacy"] / 100
            if each_spec == "DALY":
                DALY = updated_specification["DALY"]
            if each_spec == "Original Impact Score":
                origI = updated_specification["Original Impact Score"]

        # Compute New Impact Score
        newI = (((DALY * treatment_coverage * Efficacy) / (
                1 - (treatment_coverage * Efficacy))) * prevalence)

        d["Selected Country"] = selected_country
        d["Selected Company"] = selected_company
        d["Selected Disease"] = selected_disease
        d["Selected Drug"] = selected_drug
        d["Original Impact Score"] = origI
        d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)
        print(d)

        # if (selected_state == 'Country'):
        #     countries_obj = conn.execute("select country,schistosomiasis from country2015").fetchall()
        #     countries_dict= {}
        #     for countries in countries_obj:
        #         temp = countries[0].lstrip();
        #         if (temp != selected_country):
        #             countries_dict[temp] = countries[1];
        #     d["OTHER COUNTRIES"] = countries_dict
        # print(countries_obj)

        if (selected_state == 'Company'):
            company_obj = conn.execute(
                f"select company,schistosomiasis from drugr{selected_year} where schistosomiasis > 0").fetchall()
            # print(countries_obj[0])
            company_dict = {}
            for company in company_obj:
                temp = company[0].lstrip();
                if (temp != selected_company):
                    company_dict[temp] = company[1];

            del company_dict["Unmet Need"]
            d["OTHER COMPANIES"] = company_dict

        if (selected_state == 'Disease'):
            disease_obj = conn.execute(
                f"select sum(tb),sum(malaria),sum(hiv),sum(roundworm),sum(hookworm),sum(whipworm), sum(schistosomiasis), sum(onchoceriasis), sum(lf) from country{selected_year}").fetchall()
            disease_dict = {"TB": 0, "Malaria": 0, "HIV": 0, "Roundworm": 0, "Hookworm": 0, "Whipworm": 0,
                            "Schistosomiasis": 0, "Onchoceriasis": 0, "LF": 0}
            disease_dict["TB"] = round(disease_obj[0][0], 2)
            disease_dict["Malaria"] = round(disease_obj[0][1], 2)
            disease_dict["HIV"] = round(disease_obj[0][2], 2)
            disease_dict["Roundworm"] = round(disease_obj[0][3], 2)
            disease_dict["Hookworm"] = round(disease_obj[0][4], 2)
            disease_dict["Whipworm"] = round(disease_obj[0][5], 2)
            disease_dict["Schistosomiasis"] = round(disease_obj[0][6], 2)
            disease_dict["Onchocerciasis"] = round(disease_obj[0][7], 2)
            disease_dict["LF"] = round(disease_obj[0][8], 2)

            del disease_dict[selected_disease]
            # print(disease_dict)
            d["OTHER DISEASES"] = disease_dict

        if (selected_state == 'Drug'):
            drug_obj = conn.execute(
                f"select drug,sum(score)from drug{selected_year} where disease='Schistosomiasis' group by drug").fetchall()
            drug_dict = {}
            print(selected_drug)
            for drgobjs in drug_obj:
                # print (drgobjs)
                # print (drgobjs[0])
                # print (drgobjs[1])
                if (drgobjs[0] != selected_drug):
                    drug_dict[drgobjs[0]] = drgobjs[1];
            d["OTHER DRUGS"] = drug_dict
            # print(countries_obj)
        print(d)

    if (selected_disease == "Onchoceriasis"):
        d = {}
        spec_obj = conn.execute(
            f"select onch_prevalance, onch_coverage, onch_Efficacy, onch_DALY from spec_{selected_year}_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

        prevalence = 0
        treatment_coverage = 0
        Efficacy = 0
        DALY = 0

        if (len(spec_obj) > 0):
            if (selected_disease == 'Onchoceriasis'):
                prevalence = spec_obj[0][0] / 100
                treatment_coverage = spec_obj[0][1] / 100
                Efficacy = spec_obj[0][2] / 100
                DALY = spec_obj[0][3]

        newI = 0
        for each_spec in updated_specification:
            if each_spec == "Prevalence":
                prevalence = updated_specification["Prevalence"] / 100
            if each_spec == "Treatment Coverage":
                treatment_coverage = updated_specification["Treatment Coverage"] / 100
            if each_spec == "Efficacy":
                updated_specification["Efficacy"] / 100
            if each_spec == "DALY":
                DALY = updated_specification["DALY"]
            if each_spec == "Original Impact Score":
                origI = updated_specification["Original Impact Score"]

        # Compute New Impact Score
        newI = (((DALY * treatment_coverage * Efficacy) / (
                1 - (treatment_coverage * Efficacy))) * prevalence)

        d["Selected Country"] = selected_country
        d["Selected Company"] = selected_company
        d["Selected Disease"] = selected_disease
        d["Selected Drug"] = selected_drug
        d["Original Impact Score"] = origI
        d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)
        print(d)

        # if (selected_state == 'Country'):
        #     countries_obj = conn.execute("select country,onchoceriasis from country2015").fetchall()
        #     countries_dict= {}
        #     for countries in countries_obj:
        #         temp = countries[0].lstrip();
        #         if (temp != selected_country):
        #             countries_dict[temp] = countries[1];
        #     d["OTHER COUNTRIES"] = countries_dict
        # print(countries_obj)

        if (selected_state == 'Company'):
            company_obj = conn.execute(f"select company,onchoceriasis from drugr{selected_year} where onchoceriasis > 0").fetchall()
            # print(countries_obj[0])
            company_dict = {}
            for company in company_obj:
                temp = company[0].lstrip();
                if (temp != selected_company):
                    company_dict[temp] = company[1];

            del company_dict["Unmet Need"]
            d["OTHER COMPANIES"] = company_dict

        if (selected_state == 'Disease'):
            disease_obj = conn.execute(
                f"select sum(tb),sum(malaria),sum(hiv),sum(roundworm),sum(hookworm),sum(whipworm), sum(schistosomiasis), sum(onchoceriasis), sum(lf) from country{selected_year}").fetchall()
            disease_dict = {"TB": 0, "Malaria": 0, "HIV": 0, "Roundworm": 0, "Hookworm": 0, "Whipworm": 0,
                            "Schistosomiasis": 0, "Onchoceriasis": 0, "LF": 0}
            disease_dict["TB"] = round(disease_obj[0][0], 2)
            disease_dict["Malaria"] = round(disease_obj[0][1], 2)
            disease_dict["HIV"] = round(disease_obj[0][2], 2)
            disease_dict["Roundworm"] = round(disease_obj[0][3], 2)
            disease_dict["Hookworm"] = round(disease_obj[0][4], 2)
            disease_dict["Whipworm"] = round(disease_obj[0][5], 2)
            disease_dict["Schistosomiasis"] = round(disease_obj[0][6], 2)
            disease_dict["Onchocerciasis"] = round(disease_obj[0][7], 2)
            disease_dict["LF"] = round(disease_obj[0][8], 2)

            del disease_dict[selected_disease]
            # print(disease_dict)
            d["OTHER DISEASES"] = disease_dict

        if (selected_state == 'Drug'):
            drug_obj = conn.execute(
                f"select drug,sum(score)from drug{selected_year} where disease='onchoceriasis' group by drug").fetchall()
            drug_dict = {}
            print(selected_drug)
            for drgobjs in drug_obj:
                # print (drgobjs)
                # print (drgobjs[0])
                # print (drgobjs[1])
                if (drgobjs[0] != selected_drug):
                    drug_dict[drgobjs[0]] = drgobjs[1];
            d["OTHER DRUGS"] = drug_dict
            # print(countries_obj)
        print(d)

    if (selected_disease == "LF"):
        d = {}
        spec_obj = conn.execute(
            f"select LF_prevalance, LF_coverage, LF_Efficacy_DEC, LF_Efficacy_DEC_ALB, LF_Efficacy_IVM_ALB, LF_DALY from spec_{selected_year}_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

        prevalence = 0
        treatment_coverage = 0
        Efficacy = 0
        DALY = 0

        if (len(spec_obj) > 0):
            if (selected_disease == 'LF'):
                prevalence = spec_obj[0][0] / 100
                treatment_coverage = spec_obj[0][1] / 100
                if selected_drug == 'Diethylcarbamazine (DEC)':
                    Efficacy = spec_obj[0][2] / 100
                elif selected_drug == "Albendazole (ALB)":
                    Efficacy = spec_obj[0][3] / 100
                elif selected_drug == "Ivermectin (IVM)":
                    Efficacy = spec_obj[0][4] / 100
                DALY = spec_obj[0][5]

        newI = 0
        for each_spec in updated_specification:
            if each_spec == "Prevalence":
                prevalence = updated_specification["Prevalence"] / 100
            if each_spec == "Treatment Coverage":
                treatment_coverage = updated_specification["Treatment Coverage"] / 100
            if each_spec == "Efficacy":
                updated_specification["Efficacy"] / 100
            if each_spec == "DALY":
                DALY = updated_specification["DALY"]
            if each_spec == "Original Impact Score":
                origI = updated_specification["Original Impact Score"]

        # Compute New Impact Score
        newI = (((DALY * treatment_coverage * Efficacy) / (
                1 - (treatment_coverage * Efficacy))) * prevalence)

        d["Selected Country"] = selected_country
        d["Selected Company"] = selected_company
        d["Selected Disease"] = selected_disease
        d["Selected Drug"] = selected_drug
        d["Original Impact Score"] = origI
        d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)
        print(d)

        # if (selected_state == 'Country'):
        #     countries_obj = conn.execute("select country,lf from country2015").fetchall()
        #     countries_dict= {}
        #     for countries in countries_obj:
        #         temp = countries[0].lstrip();
        #         if (temp != selected_country):
        #             countries_dict[temp] = countries[1];
        #     d["OTHER COUNTRIES"] = countries_dict
        # print(countries_obj)

        if (selected_state == 'Company'):
            company_obj = conn.execute(f"select company,lf from drugr{selected_year} where lf > 0").fetchall()
            # print(countries_obj[0])
            company_dict = {}
            for company in company_obj:
                temp = company[0].lstrip();
                if (temp != selected_company):
                    company_dict[temp] = company[1];

            del company_dict["Unmet Need"]
            d["OTHER COMPANIES"] = company_dict

        if (selected_state == 'Disease'):
            disease_obj = conn.execute(
                f"select sum(tb),sum(malaria),sum(hiv),sum(roundworm),sum(hookworm),sum(whipworm), sum(schistosomiasis), sum(onchoceriasis), sum(lf) from country{selected_year}").fetchall()
            disease_dict = {"TB": 0, "Malaria": 0, "HIV": 0, "Roundworm": 0, "Hookworm": 0, "Whipworm": 0,
                            "Schistosomiasis": 0, "Onchoceriasis": 0, "LF": 0}
            disease_dict["TB"] = round(disease_obj[0][0], 2)
            disease_dict["Malaria"] = round(disease_obj[0][1], 2)
            disease_dict["HIV"] = round(disease_obj[0][2], 2)
            disease_dict["Roundworm"] = round(disease_obj[0][3], 2)
            disease_dict["Hookworm"] = round(disease_obj[0][4], 2)
            disease_dict["Whipworm"] = round(disease_obj[0][5], 2)
            disease_dict["Schistosomiasis"] = round(disease_obj[0][6], 2)
            disease_dict["Onchocerciasis"] = round(disease_obj[0][7], 2)
            disease_dict["LF"] = round(disease_obj[0][8], 2)

            del disease_dict[selected_disease]
            # print(disease_dict)
            d["OTHER DISEASES"] = disease_dict

        if (selected_state == 'Drug'):
            drug_obj = conn.execute(f"select drug,sum(score)from drug{selected_year} where disease='if' group by drug").fetchall()
            drug_dict = {}
            print(selected_drug)
            for drgobjs in drug_obj:
                # print (drgobjs)
                # print (drgobjs[0])
                # print (drgobjs[1])
                if (drgobjs[0] != selected_drug):
                    drug_dict[drgobjs[0]] = drgobjs[1];
            d["OTHER DRUGS"] = drug_dict
            # print(countries_obj)
        print(d)

    if (selected_disease == "TB"):
        spec_obj = conn.execute(
            "select * from spec_2015_TB where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
        TB_pevalance = spec_obj[0][1]
        # TB_plus_coverage = spec_obj[0][2] / 100
        # TB_minus_coverage = spec_obj[0][3] / 100
        # TB_mdr_coverage = spec_obj[0][4] / 100
        # TB_xdr_coverage = spec_obj[0][5] / 100
        # TB_plus_Efficacy = 0.78
        # TB_minus_Efficacy = 0.83  # predefined, check handbook
        # TB_mdr_Efficacy = 0.54  # predefined, check handbook
        # TB_xdr_Efficacy = 0.30  # predefined, check handbook
        # TB_plus_DALY = spec_obj[0][6]
        # TB_minus_DALY = spec_obj[0][7]
        # TB_mdr_DALY = spec_obj[0][8]
        # TB_xdr_DALY = spec_obj[0][9]
        specdrug_obj = conn.execute(
            "select tb_hiv_plus,tb_hiv_minus,tb_mdr,tb_xdr from spec_treatment_regimen where drug ='" + sd + "' COLLATE NOCASE").fetchall()

        TB_pevalance = spec_obj[0][1]
        TB_plus_Efficacy = 0
        TB_plus_coverage = 0
        TB_plus_DALY = 0
        if ((len(specdrug_obj) > 0) and (specdrug_obj[0][0] == 'True')):
            TB_plus_Efficacy = 0.78
            TB_plus_coverage = spec_obj[0][2] / 100
            TB_plus_DALY = spec_obj[0][6]

        TB_minus_coverage = 0
        TB_minus_Efficacy = 0
        TB_minus_DALY = 0
        if ((len(specdrug_obj) > 0) and (specdrug_obj[0][1] == 'True')):
            TB_minus_coverage = spec_obj[0][3] / 100
            TB_minus_Efficacy = 0.83  # predefined, check handbook
            TB_minus_DALY = spec_obj[0][7]

        TB_mdr_coverage = 0
        TB_mdr_Efficacy = 0
        TB_mdr_DALY = 0
        if ((len(specdrug_obj) > 0) and (specdrug_obj[0][2] == 'True')):
            TB_mdr_coverage = spec_obj[0][4] / 100
            TB_mdr_Efficacy = 0.54  # predefined, check handbook
            TB_mdr_DALY = spec_obj[0][8]

        TB_xdr_coverage = 0
        TB_xdr_Efficacy = 0
        TB_xdr_DALY = 0
        if ((len(specdrug_obj) > 0) and (specdrug_obj[0][3] == 'True')):
            TB_xdr_coverage = spec_obj[0][5] / 100
            TB_xdr_Efficacy = 0.30  # predefined, check handbook
            TB_xdr_DALY = spec_obj[0][9]

        d = {}
        I = 0
        for each_spec in updated_specification:
            print(each_spec)
            # Set the required values, which will be further used to calculate Impact Score
            # and further passed to specifications page.

            if each_spec == "TB Prevalence":
                TB_pevalance = updated_specification["TB Prevalence"]

            # 1. Set Treatment Coverage Values
            if each_spec == "TB/HIV+ Treatment Coverage":
                TB_plus_coverage = updated_specification["TB/HIV+ Treatment Coverage"] / 100

            if each_spec == "TB/HIV- Treatment Coverage":
                TB_minus_coverage = updated_specification["TB/HIV- Treatment Coverage"] / 100

            if each_spec == "MDR-TB Treatment Coverage":
                TB_mdr_coverage = updated_specification["MDR-TB Treatment Coverage"] / 100

            if each_spec == "XDR-TB Treatment Coverage":
                TB_xdr_coverage = updated_specification["XDR-TB Treatment Coverage"] / 100

            # 2. Set Efficacy Values
            if each_spec == "TB/HIV+ Efficacy":
                TB_plus_Efficacy = updated_specification["TB/HIV+ Efficacy"] / 100

            if each_spec == "TB/HIV- Efficacy":
                TB_minus_Efficacy = updated_specification["TB/HIV- Efficacy"] / 100

            if each_spec == "MDR-TB Efficacy":
                # TB_mdr_Efficacy = 0.54  # predefined, check handbook
                TB_mdr_Efficacy = updated_specification["MDR-TB Efficacy"] / 100

            if each_spec == "XDR-TB Efficacy":
                # TB_xdr_Efficacy = 0.30  # predefined, check handbook
                TB_xdr_Efficacy = updated_specification["XDR-TB Efficacy"] / 100

            # 2. Set DALY Values
            if each_spec == "TB/HIV+ DALY":
                TB_plus_DALY = updated_specification["TB/HIV+ DALYs"]

            if each_spec == "TB/HIV- DALY":
                TB_minus_DALY = updated_specification["TB/HIV- DALYs"]

            if each_spec == "MDR-TB DALY":
                TB_mdr_DALY = updated_specification["MDR-TB DALYs"]

            if each_spec == "XDR-TB DALY":
                TB_xdr_DALY = updated_specification["XDR-TB DALYs"]

            if each_spec == "Original Impact Score":
                origI = updated_specification["Original Impact Score"]

        # Calculate New Impact Score of TB/HIV+
        TB_HIV_plus_newI = ((TB_plus_DALY * TB_plus_Efficacy * TB_plus_coverage) / (
                1 - (TB_plus_Efficacy * TB_plus_coverage)))

        # Calculate Original Impact Score of TB/HIV-
        TB_HIV_minus_newI = ((TB_minus_DALY * TB_minus_Efficacy * TB_minus_coverage) / (
                1 - (TB_minus_Efficacy * TB_minus_coverage)))

        # Calculate Original Impact Score of MDR-TB
        MDR_TB_newI = ((TB_mdr_DALY * TB_mdr_Efficacy * TB_mdr_coverage) / (1 - (TB_mdr_Efficacy * TB_mdr_coverage)))

        # Calculate Original Impact Score of XDR-TB
        XDR_TB_newI = ((TB_xdr_DALY * TB_xdr_Efficacy * TB_xdr_coverage) / (1 - (TB_xdr_Efficacy * TB_xdr_coverage)))

        # Calculate Total Impact Score
        newI = TB_HIV_plus_newI + TB_HIV_minus_newI + MDR_TB_newI + XDR_TB_newI

        # d["Selected Disease"] = selected_disease
        d["Selected Country"] = selected_country
        d["Selected Company"] = selected_company
        d["Selected Disease"] = selected_disease
        d["Selected Drug"] = selected_drug
        d["Original Impact Score"] = origI
        d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)

        # if (selected_state == 'Country'):
        #     countries_obj = conn.execute("select country,tb from country2015").fetchall()
        #     countries_dict= {}
        #     for countries in countries_obj:
        #         temp = countries[0].lstrip();
        #         if (temp != selected_country):
        #             countries_dict[temp] = countries[1];
        #     d["OTHER COUNTRIES"] = countries_dict
        # print(countries_obj)

        if (selected_state == 'Company'):
            company_obj = conn.execute("select company,tb from drugr2015 where tb > 0").fetchall()
            # print(countries_obj[0])
            company_dict = {}
            for company in company_obj:
                temp = company[0].lstrip();
                if (temp != selected_company):
                    company_dict[temp] = company[1];

            del company_dict["Unmet Need"]
            d["OTHER COMPANIES"] = company_dict

        if (selected_state == 'Disease'):
            disease_obj = conn.execute(
                "select tb , malaria, hiv, roundworm , hookworm , whipworm ,  schistosomiasis ,  onchoceriasis , lf from country2015 where country = ' " + selected_country + "' ").fetchall()
            disease_dict = {"TB": 0, "Malaria": 0, "HIV": 0, "Roundworm": 0, "Hookworm": 0, "Whipworm": 0,
                            "Schistosomiasis": 0, "Onchoceriasis": 0, "LF": 0}
            disease_dict["TB"] = round(disease_obj[0][0], 2)
            disease_dict["Malaria"] = round(disease_obj[0][1], 2)
            disease_dict["HIV"] = round(disease_obj[0][2], 2)
            disease_dict["Roundworm"] = round(disease_obj[0][3], 2)
            disease_dict["Hookworm"] = round(disease_obj[0][4], 2)
            disease_dict["Whipworm"] = round(disease_obj[0][5], 2)
            disease_dict["Schistosomiasis"] = round(disease_obj[0][6], 2)
            disease_dict["Onchocerciasis"] = round(disease_obj[0][7], 2)
            disease_dict["LF"] = round(disease_obj[0][8], 2)

            del disease_dict[selected_disease]
            # print(disease_dict)
            d["OTHER DISEASES"] = disease_dict

        if (selected_state == 'Drug'):
            drug_obj = conn.execute("select drug,sum(score)from drug2015 where disease='TB' group by drug").fetchall()
            drug_dict = {}
            print(selected_drug)
            for drgobjs in drug_obj:
                # print (drgobjs)
                # print (drgobjs[0])
                # print (drgobjs[1])
                if (drgobjs[0] != selected_drug):
                    drug_dict[drgobjs[0]] = drgobjs[1];
            d["OTHER DRUGS"] = drug_dict
            # print(countries_obj)
        print(d)

    if (selected_disease == "Malaria"):
        print("Malaria Selected Drug", sd)
        selected_drug2 = sd.replace(" + ", "_").replace("-", "_")
        conn = connect_db()
        cursor = conn.execute("select * from spec_2015_Malaria")
        names = list(map(lambda x: x[0], cursor.description))
        drug_column1 = "Eff_PFalc_" + selected_drug2
        drug_column2 = "Eff_PVivax_" + selected_drug2

        spec_obj = conn.execute(
            "select * from spec_2015_Malaria where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
        specdrug_obj = conn.execute(
            "select malaria_PFalc, malaria_PVivax from spec_treatment_regimen where drug ='" + sd + "' COLLATE NOCASE").fetchall()

        Malaria_pevalance = spec_obj[0][1]
        # Malaria_PFalc_coverage = spec_obj[0][2] / 100
        # Malaria_PVivax_coverage = spec_obj[0][3] / 100
        # Malaria_PFalc_DALY_prop = spec_obj[0][4] / 100
        # Malaria_PVivax_DALY_prop = spec_obj[0][5] / 100
        # Malaria_Total_DALY = spec_obj[0][6]

        Malaria_PFalc_coverage = 0
        Malaria_PFalc_DALY_prop = 0
        if ((len(specdrug_obj) > 0) and (specdrug_obj[0][0] == 'True')):
            Malaria_PFalc_coverage = spec_obj[0][2] / 100
            Malaria_PFalc_DALY_prop = spec_obj[0][4] / 100
            # print("Malaria_PFalc_DALY_Prop ", Malaria_PFalc_DALY_prop)

        Malaria_PVivax_coverage = 0
        Malaria_PVivax_DALY_prop = 0
        if ((len(specdrug_obj) > 0) and (specdrug_obj[0][1] == 'True')):
            Malaria_PVivax_coverage = spec_obj[0][3] / 100
            Malaria_PVivax_DALY_prop = spec_obj[0][5] / 100
            # print("Malaria_PVivax_DALY_Prop ", Malaria_PVivax_DALY_prop)

        Malaria_Total_DALY = spec_obj[0][6]
        # print("Malaria_Total_DALY ", Malaria_Total_DALY)
        Malaria_PFalc_DALY = round((Malaria_PFalc_DALY_prop * Malaria_Total_DALY), 2)
        Malaria_PVivax_DALY = round((Malaria_PVivax_DALY_prop * Malaria_Total_DALY), 2)
        # print ("Malaria_PFalc_DALY ",Malaria_PFalc_DALY)
        # print("Malaria_PVivax_DALY ", Malaria_PVivax_DALY)
        # Malaria_PFalc_DALY = Malaria_PFalc_DALY_prop * Malaria_Total_DALY
        # Malaria_PVivax_DALY = Malaria_PVivax_DALY_prop * Malaria_Total_DALY

        Malaria_PFalc_Efficacy = 0
        Malaria_PVivax_Efficacy = 0

        if drug_column1 in names:
            spec_obj_eff1 = conn.execute(
                "select " + drug_column1 + " from spec_2015_Malaria where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
            # print("spec_obj_eff1: ", spec_obj_eff1)

            if (len(spec_obj_eff1) > 0):
                Malaria_PFalc_Efficacy = spec_obj_eff1[0][0] / 100  # predefined, check handbook

        if drug_column2 in names:
            spec_obj_eff2 = conn.execute(
                "select " + drug_column2 + " from spec_2015_Malaria where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
            # print("spec_obj_eff2: ", spec_obj_eff2)
            if (len(spec_obj_eff2) > 0):
                Malaria_PVivax_Efficacy = spec_obj_eff2[0][0] / 100

        d = {}
        I = 0
        for each_spec in updated_specification:
            print(each_spec)
            # Set the required values, which will be further used to calculate Impact Score
            # and further passed to specifications page.

            if each_spec == "Malaria Prevalence":
                Malaria_pevalance = updated_specification["Malaria Prevalence"]

            # 1. Set Treatment Coverage Values
            if each_spec == "Malaria PFalc Coverage":
                Malaria_PFalc_coverage = updated_specification["Malaria PFalc Coverage"] / 100

            if each_spec == "Malaria PVivax Coverage":
                Malaria_PVivax_coverage = updated_specification["Malaria PVivax Coverage"] / 100

            # 2. Set DALY Values

            if each_spec == "Malaria PFalc DALY":
                Malaria_PFalc_DALY = updated_specification["Malaria PFalc DALY"]
                d["Changed_Property"] = "Updated Malaria Pfalc Daly"

            if each_spec == "Malaria PVivax DALY":
                Malaria_PVivax_DALY = updated_specification["Malaria PVivax DALY"]

            # 2. Set Efficacy Values
            if each_spec == "Malaria PFalc Efficacy":
                Malaria_PFalc_Efficacy = updated_specification["Malaria PFalc Efficacy"] / 100

            if each_spec == "Malaria PVivax Efficacy":
                Malaria_PVivax_Efficacy = updated_specification["Malaria PVivax Efficacy"] / 100

            if each_spec == "Original Impact Score":
                origI = updated_specification["Original Impact Score"]

        # Malaria_PFalc_I = 0
        Malaria_PFalc_newI = ((Malaria_PFalc_DALY * Malaria_PFalc_coverage * Malaria_PFalc_Efficacy) / (
                1 - (Malaria_PFalc_coverage * Malaria_PFalc_Efficacy)))

        # Malaria_PVivax_I = 0
        Malaria_PVivax_newI = ((Malaria_PVivax_DALY * Malaria_PVivax_coverage * Malaria_PVivax_Efficacy) / (
                1 - (Malaria_PVivax_coverage * Malaria_PVivax_Efficacy)))

        # Calculate Total Impact Score
        newI = Malaria_PFalc_newI + Malaria_PVivax_newI

        d["Selected Company"] = selected_company
        d["Selected Country"] = selected_country
        d["Selected Disease"] = selected_disease
        d["Selected Drug"] = selected_drug
        d["Original Impact Score"] = origI
        d["New Impact Score"] = round(newI, 2)
        # print("New Impact Score")
        # print(newI)
        # if (selected_state == 'Country'):
        #     countries_obj = conn.execute("select country,malaria from country2015").fetchall()
        #     # print(countries_obj[0])
        #     countries_dict = {}
        #     for countries in countries_obj:
        #         temp = countries[0].lstrip();
        #         if (temp != selected_country):
        #             countries_dict[temp] = countries[1];
        #     # print(countries_dict)
        #     # print(countries_obj[" India"])
        #     d["OTHER COUNTRIES"] = countries_dict
        # print(countries_obj)

        if (selected_state == 'Company'):
            company_obj = conn.execute("select company,malaria from drugr2015 where malaria > 0").fetchall()
            # print(countries_obj[0])
            company_dict = {}
            for company in company_obj:
                temp = company[0].lstrip();
                if (temp != selected_company):
                    company_dict[temp] = company[1];
            del company_dict["Unmet Need"]

            # print(countries_dict)
            # print(countries_obj[" India"])
            d["OTHER COMPANIES"] = company_dict
            # print(countries_obj)

        if (selected_state == 'Disease'):
            disease_obj = conn.execute(
                "select tb , malaria, hiv, roundworm , hookworm , whipworm , schistosomiasis , onchoceriasis , lf from country2015 WHERE country =  ' " + selected_country + "' ").fetchall()  # Fetch data only for specific country
            disease_dict = {"TB": 0, "Malaria": 0, "HIV": 0, "Roundworm": 0, "Hookworm": 0, "Whipworm": 0,
                            "Schistosomiasis": 0, "Onchoceriasis": 0, "LF": 0}
            print(disease_obj)
            disease_dict["TB"] = round(disease_obj[0][0], 2)
            disease_dict["Malaria"] = round(disease_obj[0][1], 2)
            disease_dict["HIV"] = round(disease_obj[0][2], 2)
            disease_dict["Roundworm"] = round(disease_obj[0][3], 2)
            disease_dict["Hookworm"] = round(disease_obj[0][4], 2)
            disease_dict["Whipworm"] = round(disease_obj[0][5], 2)
            disease_dict["Schistosomiasis"] = round(disease_obj[0][6], 2)
            disease_dict["Onchocerciasis"] = round(disease_obj[0][7], 2)
            disease_dict["LF"] = round(disease_obj[0][8], 2)

            del disease_dict[selected_disease]
            # print(disease_dict)
            d["OTHER DISEASES"] = disease_dict

        if (selected_state == 'Drug'):
            drug_obj = conn.execute(
                "select drug,sum(score)from drug2015 where disease='Malaria' group by drug").fetchall()
            drug_dict = {}
            print(selected_drug)
            for drgobjs in drug_obj:
                # print (drgobjs)
                # print (drgobjs[0])
                # print (drgobjs[1])
                if (drgobjs[0] != selected_drug):
                    drug_dict[drgobjs[0]] = drgobjs[1];
            d["OTHER DRUGS"] = drug_dict

        print(d)
    if(selected_disease == "HIV"):
        d = {}
        if(selected_year == '2015'):
            spec_obj = conn.execute("select * from spec_2015_HIV where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
            regimen1_obj = conn.execute("select * from spec_2015_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 COLLATE NOCASE").fetchall()
            regimen2_obj = conn.execute("select * from spec_2015_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 COLLATE NOCASE").fetchall()
            # Original specification values
            adult_coverage = spec_obj[0][1] / 100
            child_coverage = spec_obj[0][4] / 100
            adult_daly = spec_obj[0][7]
            child_daly = spec_obj[0][8]
            overall_rate = spec_obj[0][9] / 100
            adult_rate = spec_obj[0][10] / 100
            child_rate = spec_obj[0][11] / 100
            first_adult_distribution = 0.9084 #constant
            second_adult_distribution = 0.0917 #constant
            first_child_distribution = 0.8933 #constant
            second_child_distribution = 0.1068 #constant
            first_adult_prop = 0
            second_adult_prop = 0
            first_adult_eff = 0
            second_adult_eff = 0
            first_child_prop = 0
            second_child_prop = 0
            first_child_eff = 0
            second_child_eff = 0
            origI = 0
            for k in regimen1_obj:
                first_adult_prop += k[2]/k[1]
                first_adult_eff += k[4]/k[1]
                first_child_prop += k[3]/k[1]
                first_child_eff += k[5]/k[1]
            for k in regimen2_obj:
                second_adult_prop += k[2]/k[1]
                second_adult_eff += k[4]/k[1]
                second_child_prop += k[3]/k[1]
                second_child_eff += k[5]/k[1]
            for spec in updated_specification:
                if spec == "Treatment Coverage Adults":
                    adults_need = updated_specification["Adults Needing Treatment"]
                    adults_receive = updated_spec["Adults Receiving Treatment"]
                    adult_coverage = adults_receive/adults_need
                if spec == "Treatment Coverage Children":
                    child_need = updated_specification["Adults Needing Treatment"]
                    child_receive = updated_specification["Adults Receiving Treatment"]
                    child_coverage = child_receive/child_need
                if spec == "Adult DALY":
                    adult_daly = updated_specification["Adult DALY"]
                if spec == "Child DALY":
                    child_daly = updated_specification["Child DALY"]
                if spec == "Overall Retention Rates":
                    overall_rate = updated_specification["Overall Retention Rates"]/100
                if spec == "Adult Retention Rates":
                    adult_rate = updated_specification["Adult Retention Rates"]/100
                if spec == "Child Retention Rates":
                    child_rate = updated_specification["Child Retention Rates"]/100
                if spec == "First-line Adult Distribution":
                    first_adult_distribution = updated_specification["First-line Adult Distribution"]/100
                if spec == "Second-line Adult Distribution":
                    second_adult_distribution = updated_specification["Second-line Adult Distribution"]/100
                if spec == "First-line Child Distribution":
                    first_child_distribution = updated_specification["First-line Child Distribution"]/100
                if spec == "Second-line Child Distribution":
                    second_child_distribution = updated_specification["Second-line Child Distribution"]/100
                if spec == "First-line Regimen Adult Proportion":
                    first_adult_prop = updated_specification["First-line Regimen Adult Proportion"]
                if spec == "Second-line Regimen Adult Proportion":
                    second_adult_prop = updated_specification["Second-line Regimen Adult Proportion"]
                if spec == "First-line Regimen Child Proportion":
                    first_child_prop  = updated_specification["First-line Regimen Child Proportion"]
                if spec == "Second-line Regimen child Proportion":
                    second_child_prop  = updated_specification["Second-line Regimen child Proportion"]
                if spec == "First-line Regimen Adult Efficacy":
                    first_adult_eff = updated_specification["First-line Regimen Adult Efficacy"]/100
                if spec == "Second-line Regimen Adult Efficacy":
                    second_adult_eff = updated_specification["Second-line Regimen Adult Efficacy"]/100
                if spec == "First-line Regimen Child Efficacy":
                    first_child_eff = updated_specification["First-line Regimen Child Efficacy"]/100
                if spec == "Second-line Regimen Child Efficacy":
                    second_child_eff = updated_specification["Second-line Regimen Child Efficacy"]/100
                if spec == "Original Impact Score":
                    origI = updated_specification["Original Impact Score"]

            newI_a1 = (adult_daly * adult_coverage * (first_adult_distribution * first_adult_prop * first_adult_eff))/(1 - adult_coverage *(first_adult_distribution * first_adult_prop * first_adult_eff))
            newI_a2 = (adult_daly * adult_coverage * (second_adult_distribution * second_adult_prop * second_adult_eff))/(1 - adult_coverage *(second_adult_distribution * second_adult_prop * second_adult_eff))
            newI_c1 = (child_daly * child_coverage * (first_child_distribution * first_child_prop * first_child_eff))/(1 - child_coverage*(first_child_distribution * first_child_prop * first_child_eff))
            newI_c2 = (child_daly * child_coverage * (second_child_distribution * second_child_prop * second_child_eff))/(1 - child_coverage*(second_child_distribution * second_child_prop * second_child_eff))
            newI = newI_a1 + newI_a2 + newI_c1 + newI_c2
            # d["Selected Disease"] = selected_disease
            d["Selected Country"] = selected_country
            d["Selected Company"] = selected_company
            d["Selected Disease"] = selected_disease
            d["Selected Drug"] = selected_drug
            d["Original Impact Score"] = origI
            d["New Impact Score"] = round(newI, 2)
            print("New Impact Score")
            print(newI)
        if (selected_year == '2013'):
            spec_obj = conn.execute("select * from spec_2013_HIV where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
            regimen1_obj_A = conn.execute("select * from spec_2013_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and grp = 'A' COLLATE NOCASE").fetchall()
            regimen2_obj_A = conn.execute("select * from spec_2013_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and grp = 'A' COLLATE NOCASE").fetchall()
            regimen1_obj_B = conn.execute("select * from spec_2013_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and grp = 'B' COLLATE NOCASE").fetchall()
            regimen2_obj_B = conn.execute("select * from spec_2013_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and grp = 'B' COLLATE NOCASE").fetchall()

            # Original specification values
            adult_coverage = spec_obj[0][1] / 100
            child_coverage = spec_obj[0][4] / 100
            adult_daly = spec_obj[0][7]
            child_daly = spec_obj[0][8]
            overall_rate = spec_obj[0][9] / 100
            adult_rate = spec_obj[0][10] / 100
            child_rate = spec_obj[0][11] / 100

            # Group A values
            first_adult_distribution_A = 0.9624 #constant
            second_adult_distribution_A = 0.0376 #constant
            first_child_distribution_A = 0.9655 #constant
            second_child_distribution_A = 0.0345 #constant
            first_adult_prop_A = 0
            second_adult_prop_A = 0
            first_adult_eff_A = 0
            second_adult_eff_A = 0
            first_child_prop_A = 0
            second_child_prop_A = 0
            first_child_eff_A = 0
            second_child_eff_A = 0
            for k in regimen1_obj_A:
                first_adult_prop_A += k[2]/k[1]
                first_adult_eff_A += k[4]/k[1]
                first_child_prop_A += k[3]/k[1]
                first_child_eff_A += k[5]/k[1]
            for k in regimen2_obj_A:
                second_adult_prop_A += k[2]/k[1]
                second_adult_eff_A += k[4]/k[1]
                second_child_prop_A += k[3]/k[1]
                second_child_eff_A += k[5]/k[1]

            # Group B values
            first_adult_distribution_B = 0.8543 #constant
            second_adult_distribution_B = 0.1457 #constant
            first_child_distribution_B = 0.8210 #constant
            second_child_distribution_B = 0.1790 #constant
            first_adult_prop_B = 0
            second_adult_prop_B = 0
            first_adult_eff_B = 0
            second_adult_eff_B = 0
            first_child_prop_B = 0
            second_child_prop_B = 0
            first_child_eff_B = 0
            second_child_eff_B = 0
            for k in regimen1_obj_B:
                first_adult_prop_B += k[2]/k[1]
                first_adult_eff_B += k[4]/k[1]
                first_child_prop_B += k[3]/k[1]
                first_child_eff_B += k[5]/k[1]
            for k in regimen2_obj_B:
                second_adult_prop_B += k[2]/k[1]
                second_adult_eff_B += k[4]/k[1]
                second_child_prop_B += k[3]/k[1]
                second_child_eff_B += k[5]/k[1]

            origI = 0
            for spec in updated_specification:
                if spec == "Treatment Coverage Adults":
                    adults_need = updated_specification["Adults Needing Treatment"]
                    adults_receive = updated_spec["Adults Receiving Treatment"]
                    adult_coverage = adults_receive/adults_need
                if spec == "Treatment Coverage Children":
                    child_need = updated_specification["Adults Needing Treatment"]
                    child_receive = updated_specification["Adults Receiving Treatment"]
                    child_coverage = child_receive/child_need
                if spec == "Adult DALY":
                    adult_daly = updated_specification["Adult DALY"]
                if spec == "Child DALY":
                    child_daly = updated_specification["Child DALY"]
                if spec == "Overall Retention Rates":
                    overall_rate = updated_specification["Overall Retention Rates"]/100
                if spec == "Adult Retention Rates":
                    adult_rate = updated_specification["Adult Retention Rates"]/100
                if spec == "Child Retention Rates":
                    child_rate = updated_specification["Child Retention Rates"]/100
                if spec == "Group A First-line Adult Distribution":
                    first_adult_distribution_A = updated_specification["Group A First-line Adult Distribution"]/100
                if spec == "Group B First-line Adult Distribution":
                    first_adult_distribution_B = updated_specification["Group B First-line Adult Distribution"]/100
                if spec == "Group A Second-line Adult Distribution":
                    second_adult_distribution_A = updated_specification["Group A Second-line Adult Distribution"]/100
                if spec == "Group B Second-line Adult Distribution":
                    second_adult_distribution_B = updated_specification["Group B Second-line Adult Distribution"]/100
                if spec == "Group A First-line Child Distribution":
                    first_child_distribution_A = updated_specification["Group A First-line Child Distribution"]/100
                if spec == "Group B First-line Child Distribution":
                    first_child_distribution_B = updated_specification["Group B First-line Child Distribution"]/100
                if spec == "Group A Second-line Child Distribution":
                    second_child_distribution_A = updated_specification["Group A Second-line Child Distribution"]/100
                if spec == "Group B Second-line Child Distribution":
                    second_child_distribution_B = updated_specification["Group B Second-line Child Distribution"]/100
                if spec == "Group A First-line Regimen Adult Proportion":
                    first_adult_prop_A = updated_specification["Group A First-line Regimen Adult Proportion"]
                if spec == "Group B First-line Regimen Adult Proportion":
                    first_adult_prop_B = updated_specification["Group B First-line Regimen Adult Proportion"]
                if spec == "Group A Second-line Regimen Adult Proportion":
                    second_adult_prop_A = updated_specification["Group A Second-line Regimen Adult Proportion"]
                if spec == "Group B Second-line Regimen Adult Proportion":
                    second_adult_prop_B = updated_specification["Group B Second-line Regimen Adult Proportion"]
                if spec == "Group A First-line Regimen Child Proportion":
                    first_child_prop_A = updated_specification["Group A First-line Regimen Child Proportion"]
                if spec == "Group B First-line Regimen Child Proportion":
                    first_child_prop_B = updated_specification["Group B First-line Regimen Child Proportion"]
                if spec == "Group A Second-line Regimen child Proportion":
                    second_child_prop_A  = updated_specification["Group A Second-line Regimen child Proportion"]
                if spec == "Group B Second-line Regimen child Proportion":
                    second_child_prop_B  = updated_specification["Group B Second-line Regimen child Proportion"]
                if spec == "Group A First-line Regimen Adult Efficacy":
                    first_adult_eff_A = updated_specification["Group A First-line Regimen Adult Efficacy"]/100
                if spec == "Group B First-line Regimen Adult Efficacy":
                    first_adult_eff_B = updated_specification["Group B First-line Regimen Adult Efficacy"]/100
                if spec == "Group A Second-line Regimen Adult Efficacy":
                    second_adult_eff_A = updated_specification["Group A Second-line Regimen Adult Efficacy"]/100
                if spec == "Group B Second-line Regimen Adult Efficacy":
                    second_adult_eff_B = updated_specification["Group B Second-line Regimen Adult Efficacy"]/100
                if spec == "Group A First-line Regimen Child Efficacy":
                    first_child_eff_A = updated_specification["Group A First-line Regimen Child Efficacy"]/100
                if spec == "Group B First-line Regimen Child Efficacy":
                    first_child_eff_B = updated_specification["Group B First-line Regimen Child Efficacy"]/100
                if spec == "Group A Second-line Regimen Child Efficacy":
                    second_child_eff_A = updated_specification["Group A Second-line Regimen Child Efficacy"]/100
                if spec == "Group B Second-line Regimen Child Efficacy":
                    second_child_eff_B = updated_specification["Group B Second-line Regimen Child Efficacy"]/100
                if spec == "Original Impact Score":
                    origI = updated_specification["Original Impact Score"]

            I_a1_A = (adult_daly * adult_coverage * (first_adult_distribution_A * first_adult_prop_A * first_adult_eff_A))/(1 - adult_coverage *(first_adult_distribution_A * first_adult_prop_A * first_adult_eff_A))
            I_a2_A = (adult_daly * adult_coverage * (second_adult_distribution_A * second_adult_prop_A * second_adult_eff_A))/(1 - adult_coverage *(second_adult_distribution_A * second_adult_prop_A * second_adult_eff_A))
            I_c1_A = (child_daly * child_coverage * (first_child_distribution_A * first_child_prop_A * first_child_eff_A))/(1 - child_coverage*(first_child_distribution_A * first_child_prop_A * first_child_eff_A))
            I_c2_A = (child_daly * child_coverage * (second_child_distribution_A * second_child_prop_A * second_child_eff_A))/(1 - child_coverage*(second_child_distribution_A * second_child_prop_A * second_child_eff_A))
            I_a1_B = (adult_daly * adult_coverage * (first_adult_distribution_B * first_adult_prop_B * first_adult_eff_B))/(1 - adult_coverage *(first_adult_distribution_B * first_adult_prop_B * first_adult_eff_B))
            I_a2_B = (adult_daly * adult_coverage * (second_adult_distribution_B * second_adult_prop_B * second_adult_eff_B))/(1 - adult_coverage *(second_adult_distribution_B * second_adult_prop_B * second_adult_eff_B))
            I_c1_B = (child_daly * child_coverage * (first_child_distribution_B * first_child_prop_B * first_child_eff_B))/(1 - child_coverage*(first_child_distribution_B * first_child_prop_B * first_child_eff_B))
            I_c2_B = (child_daly * child_coverage * (second_child_distribution_B * second_child_prop_B * second_child_eff_B))/(1 - child_coverage*(second_child_distribution_B * second_child_prop_B * second_child_eff_B))
            newI = I_a1_A + I_a2_A + I_c1_A + I_c2_A + I_a1_B + I_a2_B + I_c1_B + I_c2_B

            # d["Selected Disease"] = selected_disease
            d["Selected Country"] = selected_country
            d["Selected Company"] = selected_company
            d["Selected Disease"] = selected_disease
            d["Selected Drug"] = selected_drug
            d["Original Impact Score"] = origI
            d["New Impact Score"] = round(newI, 2)
            print("New Impact Score")
            print(newI)

        if (selected_year == '2010'):
            spec_obj = conn.execute("select * from spec_2010_HIV where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
            regimen1_obj_A_adult = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and adult = 1 and grp = 'A' COLLATE NOCASE").fetchall()
            regimen1_obj_A_child = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and child = 1 and grp = 'A' COLLATE NOCASE").fetchall()
            regimen2_obj_A_adult = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and adult = 1 and grp = 'A' COLLATE NOCASE").fetchall()
            regimen2_obj_A_child = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and child = 1 and grp = 'A' COLLATE NOCASE").fetchall()
            regimen1_obj_B_adult = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and adult = 1 and grp = 'B' COLLATE NOCASE").fetchall()
            regimen1_obj_B_child = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and First_line = 1 and child = 1 and grp = 'B' COLLATE NOCASE").fetchall()
            regimen2_obj_B_adult = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and adult = 1 and grp = 'B' COLLATE NOCASE").fetchall()
            regimen2_obj_B_child = conn.execute("select * from spec_2010_HIV_Regimen where Regimens like '%" + sd + "%' and Second_line = 1 and child = 1 and grp = 'B' COLLATE NOCASE").fetchall()

            # Original specification values
            adult_coverage = spec_obj[0][1] / 100
            child_coverage = spec_obj[0][4] / 100
            adult_daly = spec_obj[0][7]
            child_daly = spec_obj[0][8]
            overall_rate = spec_obj[0][9] / 100
            adult_rate = spec_obj[0][10] / 100
            child_rate = spec_obj[0][11] / 100

            # Group A values
            first_adult_distribution_A = 0.9710 #constant
            second_adult_distribution_A = 0.0290 #constant
            first_child_distribution_A = 0.9680 #constant
            second_child_distribution_A = 0.0320 #constant
            first_adult_prop_A = 0
            second_adult_prop_A = 0
            first_adult_eff_A = 0
            second_adult_eff_A = 0
            first_child_prop_A = 0
            second_child_prop_A = 0
            first_child_eff_A = 0
            second_child_eff_A = 0
            for k in regimen1_obj_A_adult:
                first_adult_prop_A += k[2]/k[1]
                first_adult_eff_A += k[3]/k[1]
            for k in regimen1_obj_A_child:
                first_child_prop_A += k[2]/k[1]
                first_child_eff_A += k[3]/k[1]
            for k in regimen2_obj_A_adult:
                second_adult_prop_A += k[2]/k[1]
                second_adult_eff_A += k[3]/k[1]
            for k in regimen2_obj_A_child:
                second_child_prop_A += k[2]/k[1]
                second_child_eff_A += k[3]/k[1]

            # Group B values
            first_adult_distribution_B = 0.6910 #constant
            second_adult_distribution_B = 0.2780 #constant
            first_child_distribution_B = 0.7210 #constant
            second_child_distribution_B = 0.2490 #constant
            first_adult_prop_B = 0
            second_adult_prop_B = 0
            first_adult_eff_B = 0
            second_adult_eff_B = 0
            first_child_prop_B = 0
            second_child_prop_B = 0
            first_child_eff_B = 0
            second_child_eff_B = 0
            for k in regimen1_obj_B_adult:
                first_adult_prop_B += k[2]/k[1]
                first_adult_eff_B += k[3]/k[1]
            for k in regimen1_obj_B_child:
                first_child_prop_B += k[2]/k[1]
                first_child_eff_B += k[3]/k[1]
            for k in regimen2_obj_B_adult:
                second_adult_prop_B += k[2]/k[1]
                second_adult_eff_B += k[3]/k[1]
            for k in regimen2_obj_B_child:  
                second_child_prop_B += k[2]/k[1]
                second_child_eff_B += k[3]/k[1]
            origI = 0
            for spec in updated_specification:
                if spec == "Treatment Coverage Adults":
                    adults_need = updated_specification["Adults Needing Treatment"]
                    adults_receive = updated_spec["Adults Receiving Treatment"]
                    adult_coverage = adults_receive/adults_need
                if spec == "Treatment Coverage Children":
                    child_need = updated_specification["Adults Needing Treatment"]
                    child_receive = updated_specification["Adults Receiving Treatment"]
                    child_coverage = child_receive/child_need
                if spec == "Adult DALY":
                    adult_daly = updated_specification["Adult DALY"]
                if spec == "Child DALY":
                    child_daly = updated_specification["Child DALY"]
                if spec == "Overall Retention Rates":
                    overall_rate = updated_specification["Overall Retention Rates"]/100
                if spec == "Adult Retention Rates":
                    adult_rate = updated_specification["Adult Retention Rates"]/100
                if spec == "Child Retention Rates":
                    child_rate = updated_specification["Child Retention Rates"]/100
                if spec == "Group A First-line Adult Distribution":
                    first_adult_distribution_A = updated_specification["Group A First-line Adult Distribution"]/100
                if spec == "Group B First-line Adult Distribution":
                    first_adult_distribution_B = updated_specification["Group B First-line Adult Distribution"]/100
                if spec == "Group A Second-line Adult Distribution":
                    second_adult_distribution_A = updated_specification["Group A Second-line Adult Distribution"]/100
                if spec == "Group B Second-line Adult Distribution":
                    second_adult_distribution_B = updated_specification["Group B Second-line Adult Distribution"]/100
                if spec == "Group A First-line Child Distribution":
                    first_child_distribution_A = updated_specification["Group A First-line Child Distribution"]/100
                if spec == "Group B First-line Child Distribution":
                    first_child_distribution_B = updated_specification["Group B First-line Child Distribution"]/100
                if spec == "Group A Second-line Child Distribution":
                    second_child_distribution_A = updated_specification["Group A Second-line Child Distribution"]/100
                if spec == "Group B Second-line Child Distribution":
                    second_child_distribution_B = updated_specification["Group B Second-line Child Distribution"]/100
                if spec == "Group A First-line Regimen Adult Proportion":
                    first_adult_prop_A = updated_specification["Group A First-line Regimen Adult Proportion"]
                if spec == "Group B First-line Regimen Adult Proportion":
                    first_adult_prop_B = updated_specification["Group B First-line Regimen Adult Proportion"]
                if spec == "Group A Second-line Regimen Adult Proportion":
                    second_adult_prop_A = updated_specification["Group A Second-line Regimen Adult Proportion"]
                if spec == "Group B Second-line Regimen Adult Proportion":
                    second_adult_prop_B = updated_specification["Group B Second-line Regimen Adult Proportion"]
                if spec == "Group A First-line Regimen Child Proportion":
                    first_child_prop_A = updated_specification["Group A First-line Regimen Child Proportion"]
                if spec == "Group B First-line Regimen Child Proportion":
                    first_child_prop_B = updated_specification["Group B First-line Regimen Child Proportion"]
                if spec == "Group A Second-line Regimen child Proportion":
                    second_child_prop_A  = updated_specification["Group A Second-line Regimen child Proportion"]
                if spec == "Group B Second-line Regimen child Proportion":
                    second_child_prop_B  = updated_specification["Group B Second-line Regimen child Proportion"]
                if spec == "Group A First-line Regimen Adult Efficacy":
                    first_adult_eff_A = updated_specification["Group A First-line Regimen Adult Efficacy"]/100
                if spec == "Group B First-line Regimen Adult Efficacy":
                    first_adult_eff_B = updated_specification["Group B First-line Regimen Adult Efficacy"]/100
                if spec == "Group A Second-line Regimen Adult Efficacy":
                    second_adult_eff_A = updated_specification["Group A Second-line Regimen Adult Efficacy"]/100
                if spec == "Group B Second-line Regimen Adult Efficacy":
                    second_adult_eff_B = updated_specification["Group B Second-line Regimen Adult Efficacy"]/100
                if spec == "Group A First-line Regimen Child Efficacy":
                    first_child_eff_A = updated_specification["Group A First-line Regimen Child Efficacy"]/100
                if spec == "Group B First-line Regimen Child Efficacy":
                    first_child_eff_B = updated_specification["Group B First-line Regimen Child Efficacy"]/100
                if spec == "Group A Second-line Regimen Child Efficacy":
                    second_child_eff_A = updated_specification["Group A Second-line Regimen Child Efficacy"]/100
                if spec == "Group B Second-line Regimen Child Efficacy":
                    second_child_eff_B = updated_specification["Group B Second-line Regimen Child Efficacy"]/100
                if spec == "Original Impact Score":
                    origI = updated_specification["Original Impact Score"]

            I_a1_A = (adult_daly * adult_coverage * (first_adult_distribution_A * first_adult_prop_A * first_adult_eff_A))/(1 - adult_coverage *(first_adult_distribution_A * first_adult_prop_A * first_adult_eff_A))
            I_a2_A = (adult_daly * adult_coverage * (second_adult_distribution_A * second_adult_prop_A * second_adult_eff_A))/(1 - adult_coverage *(second_adult_distribution_A * second_adult_prop_A * second_adult_eff_A))
            I_c1_A = (child_daly * child_coverage * (first_child_distribution_A * first_child_prop_A * first_child_eff_A))/(1 - child_coverage*(first_child_distribution_A * first_child_prop_A * first_child_eff_A))
            I_c2_A = (child_daly * child_coverage * (second_child_distribution_A * second_child_prop_A * second_child_eff_A))/(1 - child_coverage*(second_child_distribution_A * second_child_prop_A * second_child_eff_A))
            I_a1_B = (adult_daly * adult_coverage * (first_adult_distribution_B * first_adult_prop_B * first_adult_eff_B))/(1 - adult_coverage *(first_adult_distribution_B * first_adult_prop_B * first_adult_eff_B))
            I_a2_B = (adult_daly * adult_coverage * (second_adult_distribution_B * second_adult_prop_B * second_adult_eff_B))/(1 - adult_coverage *(second_adult_distribution_B * second_adult_prop_B * second_adult_eff_B))
            I_c1_B = (child_daly * child_coverage * (first_child_distribution_B * first_child_prop_B * first_child_eff_B))/(1 - child_coverage*(first_child_distribution_B * first_child_prop_B * first_child_eff_B))
            I_c2_B = (child_daly * child_coverage * (second_child_distribution_B * second_child_prop_B * second_child_eff_B))/(1 - child_coverage*(second_child_distribution_B * second_child_prop_B * second_child_eff_B))
            newI = I_a1_A + I_a2_A + I_c1_A + I_c2_A + I_a1_B + I_a2_B + I_c1_B + I_c2_B
            # d["Selected Disease"] = selected_disease
            d["Selected Country"] = selected_country
            d["Selected Company"] = selected_company
            d["Selected Disease"] = selected_disease
            d["Selected Drug"] = selected_drug
            d["Original Impact Score"] = origI
            d["New Impact Score"] = round(newI, 2)
            print("New Impact Score")
            print(newI)

        # if (selected_state == 'Country'):
        #     countries_obj = conn.execute("select country,hiv from country2015").fetchall()
        #     countries_dict= {}
        #     for countries in countries_obj:
        #         temp = countries[0].lstrip();
        #         if (temp != selected_country):
        #             countries_dict[temp] = countries[1];
        #     d["OTHER COUNTRIES"] = countries_dict
            # print(countries_obj)

        if (selected_state == 'Company'):
            company_obj = conn.execute("select company,hiv from drugr2015").fetchall()
            # print(countries_obj[0])
            company_dict = {}
            for company in company_obj:
                temp = company[0].lstrip();
                if (temp != selected_company):
                    company_dict[temp] = company[1];

            del company_dict["Unmet Need"]
            d["OTHER COMPANIES"] = company_dict

        if (selected_state == 'Disease'):
            # disease_obj = conn.execute("select sum(tb),sum(malaria),sum(hiv),sum(roundworm),sum(hookworm),sum(whipworm), sum(schistosomiasis), sum(onchoceriasis), sum(lf) from country2015").fetchall()
            disease_obj = conn.execute(
                "select tb , malaria, hiv, roundworm , hookworm , whipworm , schistosomiasis , onchoceriasis , lf from country2015 WHERE country =  ' " + selected_country + "' ").fetchall()  # Fetch data only for specific country
            disease_dict = {"TB": 0, "Malaria": 0, "HIV": 0, "Roundworm": 0, "Hookworm": 0, "Whipworm": 0,
                            "Schistosomiasis": 0, "Onchoceriasis": 0, "LF": 0}
            disease_dict["TB"] = round(disease_obj[0][0], 2)
            disease_dict["Malaria"] = round(disease_obj[0][1], 2)
            disease_dict["HIV"] = round(disease_obj[0][2], 2)
            disease_dict["Roundworm"] = round(disease_obj[0][3], 2)
            disease_dict["Hookworm"] = round(disease_obj[0][4], 2)
            disease_dict["Whipworm"] = round(disease_obj[0][5], 2)
            disease_dict["Schistosomiasis"] = round(disease_obj[0][6], 2)
            disease_dict["Onchocerciasis"] = round(disease_obj[0][7], 2)
            disease_dict["LF"] = round(disease_obj[0][8], 2)

            del disease_dict[selected_disease]
            # print(disease_dict)
            d["OTHER DISEASES"] = disease_dict

        if (selected_state == 'Drug'):
            drug_obj = conn.execute("select drug,sum(score)from drug2015 where disease='HIV' group by drug").fetchall()
            drug_dict = {}
            print(selected_drug)
            for drgobjs in drug_obj:
                # print (drgobjs)
                # print (drgobjs[0])
                # print (drgobjs[1])
                if (drgobjs[0] != selected_drug):
                    drug_dict[drgobjs[0]] = drgobjs[1];
            d["OTHER DRUGS"] = drug_dict
            # print(countries_obj)
        print(d)
        # return d;

    if (selected_state == 'Country'):
        # countries_obj = conn.execute("select country,whipworm from country2015").fetchall()
        countries_obj = conn.execute(f"select country,score from countryDrug{selected_year} where drug='" + selected_drug + "' and score > 0.0").fetchall()
        countries_dict = {}
        for countries in countries_obj:
            temp = countries[0].lstrip();
            if (temp != selected_country):
                countries_dict[temp] = countries[1];
        d["OTHER COUNTRIES"] = countries_dict

    ### 04/06:  Waiting on Confirmation from Modelling Team:
    # if (selected_state == 'Company'):
    #     # company_obj = conn.execute("select company,hiv from drugr2015").fetchall()
    #     drug_obj_by_dis = conn.execute(
    #         "select distinct drug from drug2015 where disease ='" + selected_disease + "' COLLATE NOCASE").fetchall()
    #     drug_obj_by_cntry = conn.execute(
    #         "select drug, company,score from countryDrug2015 where country='" + selected_country + "' and score>0 ").fetchall()
    #     print("***********************************")
    #     print(drug_obj_by_dis)
    #     print("***********************************")
    #     print (drug_obj_by_cntry)
    #     company_dict = {}
    #     for drgIdxByDis, drgByDis in enumerate(drug_obj_by_dis):
    #         for drgIdxByCnt, drgByCnt in enumerate(drug_obj_by_cntry):
    #             if (drgByDis[0].lower() == drgByCnt[0].lower()):
    #                 print (drgByCnt[0])
    #                 print (drgByCnt[1])
    #                 company_dict[drgByCnt[1]] = drgByCnt[2]
    #     print("***********************************")
    #     print (company_dict)
    # print(countries_obj[0])
    # company_dict= {}
    # for company in company_obj:
    #     temp = company[0].lstrip();
    #     if (temp != selected_company):
    #         company_dict[temp] = company[1];

    # del company_dict["Unmet Need"]
    # d["OTHER COMPANIES"] = company_dict

    conn.close()
    # return json.dumps(I)
    return json.dumps(d)


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)

# @app.errorhandler(500)
# def internal_error_500(e):
#     return render_template('error500.html',showindex=1, navsub=1), 500

if __name__ == '__main__':
    app.run(debug=True)
