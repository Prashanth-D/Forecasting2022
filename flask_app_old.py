# -*- coding: utf-8 -*-
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template, request
import xlrd, pandas, os, sqlite3, json
from collections import defaultdict
import numpy as np
from flask import request

app = Flask(__name__)
pandas.option_context('display.max_rows', None, 'display.max_columns', None)
DATABASE = 'K_ghi.db'
mapping = {2: "TB", 3: "Malaria", 4: "HIV", 5: "Roundworm", 6: "Hookworm", 7: "Whipworm", 8: "Schistomasis",
           9: "Onchoceriasis", 10: "if"}
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

@app.route('/country', methods=['GET', 'POST'])
def getAllCountries():
    conn = connect_db()
    countries_obj = conn.execute("select country from country2015").fetchall()
    list_of_countries = [i[0] for i in countries_obj]
    return json.dumps(list_of_countries)


@app.route('/get_disease', methods=['GET', 'POST'])
def getDiseaseFromCountry():
    country_select = request.get_json()["selected_country"]
    string_country_select = str(country_select)
    # print country_select
    conn = connect_db()
    disease = []
    # countries_obj = conn.execute("select * from country2015 where country = " + "' " + str(country_select) +"'").fetchall()
    countries_obj = conn.execute(
        "select * from country2015 where country = " + "\" " + str(country_select) + "\"").fetchall()
    # changes the query to add escape character in the middle like this  "\" "
    # Updated on :July 07,2020
    # Updated by : Kasturi Vartak
    if (len(countries_obj) > 0):
        for idx, val in enumerate(countries_obj[0][2:]):
            if (val > 0):
                disease.append(mapping[idx + 2])
        return json.dumps(disease)
    return "No data found"
    # return json.dumps("No diseases found")


@app.route('/get_drug', methods=['GET', 'POST'])
def getDrugByDisease():
    selected_disease = request.get_json()["selected_disease"]
    print(selected_disease)
    selected_country = request.get_json()["selected_country"]
    print(selected_country)
    drugsToSelect = []
    conn = connect_db()
    # Updated by: Nutan (Added condition to filter drugs by Country and Disease

    drug_obj_by_dis = conn.execute(
        "select drug from drug2015 where disease ='" + selected_disease + "' COLLATE NOCASE").fetchall()
    drug_obj_by_cntry = conn.execute(
        "select distinct drug from countryDrug2015 where country='" + selected_country + "' and score>0").fetchall()

    print(len(drug_obj_by_dis))
    print(len(drug_obj_by_cntry))

    if (len(drug_obj_by_cntry) > 0):
        for drgIdxByDis, drgByDis in enumerate(drug_obj_by_dis):
            for drgIdxByCnt, drgByCnt in enumerate(drug_obj_by_cntry):
                # print(drgByDis)
                # print(drgByCnt)
                if (drgByDis[0].lower() == drgByCnt[0].lower()):
                    drugsToSelect.append(drgByDis[0])
        return json.dumps(drugsToSelect)
    return "No data found"

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
    selected_country = request.get_json()["selected_country"]
    selected_disease = request.get_json()["selected_disease"]
    drug = request.get_json()["selected_drug"]
    conn = connect_db()
    # Nutan: Added distinct to eliminate duplicates
    company_obj = conn.execute("select distinct company from drug2015 where drug ='" + drug + "'").fetchall()
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


# print getDiseaseFromCountry(" Albania")
# print getDrugByDisease('TB')
# print getCompanyByDrug("Lamivudine (3TC)")

# drug->country->disease->Company
def getAllDrugs():
    conn = connect_db()
    obj = conn.execute("select drug from drug2015").fetchall()
    return obj


def getCountrybyDrug(drug):
    conn = connect_db()
    obj = conn.execute("select country from drugimpact2015 where drug > 0").fetchall()
    return obj


def getDiseaseByCountry(country):
    conn = connect_db()
    countries = []
    obj = conn.execute("select * from country2015 where country =" + country).fetchall()
    for idx, val in enumerate(obj[0][2:]):
        if (val > 0):
            countries.append(mapping[idx + 2])
    return countries


# can use the above company by disease for next function


# disease -> country -> drug-> company
def getAllDisease():
    conn = connect_db()
    obj = conn.execute("select disease from disease2015").fetchall()
    return obj


def getCompanybyDisease(disease):
    conn = connect_db()
    obj = conn.execute("select disease, company from manudis2015").fetchall()
    d = {}
    for key, value in obj:
        if key not in d:
            d[key] = []
        d[key].append(value)
    return d[disease]


def getCountrybyDrug(drug):
    conn = connect_db()
    obj = conn.execute("select country from drugimpact2015 where drug > 0").fetchall()
    return obj


def getCountrybyDisease(disease):
    conn = connect_db()
    obj = conn.execute("select country from countrybydis2010 where " + disease + "> 0").fetchall()
    return obj

# Changed by: Nutan (03/12/2021)
# Sequence 4
# company -> Country -> disease -> drug
#Commenting Old Default code and adding the API calls
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
@app.route('/company', methods = ['GET' , 'POST'])
def getAllCompanies():
    conn = connect_db()
    #companies_obj = conn.execute("select manufacturer from manufacturer").fetchall()
    companies_obj = conn.execute("select distinct company from drugr2015").fetchall()
    list_of_companies =  [i[0] for i in companies_obj]
    return json.dumps(list_of_companies)

#can use the getCountrybyDisease function from the first sequence

#Get company for the drug selected
@app.route('/get_country', methods = ['GET','POST'])
def getCountryByCompany():
    company_select = request.get_json()["selected_company"]
    print (company_select)
    conn = connect_db()
    #country_obj = conn.execute("select country from country2015").fetchall()
    # country_obj = conn.execute("select country from company_country_mapping where company='"+company_select+"'").fetchall()
    country_obj = conn.execute("select distinct country from countryDrug2015 where company='"+company_select+"' and score>0").fetchall()
    list_of_countries =  [i[0] for i in country_obj]
    return json.dumps(list_of_countries)

#Get disease from Country selected
@app.route('/get_disease', methods = ['GET','POST'])
def getDiseaseFromCountryCmpny():
    print ("In disease selection")
    country_select = request.get_json()["selected_country"]
    print ("selected country")
    print (country_select)
    #company_select = "Kyorin Pharmaceutical Co., Ltd."
    company_select = request.get_json()["selected_company"]
    print ("selected company")
    print (company_select)
    conn = connect_db()
    disease = []
    countries_obj = conn.execute("select * from country2015 where country = " + "' " + str(country_select) +"'").fetchall()
    company_obj = conn.execute("select distinct disease from drug2015 where company = '"+company_select+"'").fetchall()
    print (company_obj)
    print (countries_obj)

    #if((len(countries_obj) >0 ) and (len(company_obj) > 0)):
    if(len(countries_obj) >0 ):
        for idx, val in enumerate(countries_obj[0][2:]):
            if(val > 0):
                print(idx,val)
                for cmpnyIdx, cmpnyDisease in enumerate(company_obj):
                    print ("disease based on copny")
                    print (cmpnyIdx, cmpnyDisease[0])
                    if ((mapping[idx+2]).lower() == cmpnyDisease[0].lower()):
                        disease.append(mapping[idx+2])
        return json.dumps(disease)
    return "No data found"
    # return json.dumps("No diseases found")

#Get drug from disease selected
@app.route('/get_drug', methods = ['GET','POST'])
def getDrugByDiseaseCmpny():
    selected_disease = request.get_json()["selected_disease"]
    selected_company = request.get_json()["selected_company"]
    selected_country = request.get_json()["selected_country"]
    print (selected_company, selected_country, selected_disease)
    #company_select = "Kyorin Pharmaceutical Co., Ltd."

    conn = connect_db()
    drug_obj = conn.execute("select drug from drug2015 where disease ='"+selected_disease+"' COLLATE NOCASE and company ='"+selected_company+"' COLLATE NOCASE").fetchall()
    #drug_obj = conn.execute("select drug from drug2015 where disease ='"+selected_disease+"' COLLATE NOCASE").fetchall()
    drugs_obj = [i[0] for i in drug_obj]
    # getCompanyByDrug(drug_obj[0][0])
    return json.dumps(drugs_obj)
### Sequece 4 END

# specification start
# to display specifications in the dropdown
@app.route('/get_specification', methods=['GET', 'POST'])
def getSpecification():
    # selected_country = request.get_json()["selected_country"]
    selected_disease = request.get_json()["selected_disease"]
    selected_drug = request.get_json()["selected_drug"]
    print(selected_drug)
    # selected_company = request.get_json()["selected_company"]
    sd = selected_drug[selected_drug.find("(") + 1:selected_drug.find(")")]
    print(sd)
    spec = []
    conn = connect_db()
    spec_obj = conn.execute(
        "select tb_hiv_plus,tb_hiv_minus,tb_mdr,tb_xdr,malaria_PFalc, malaria_PVivax from spec_treatment_regimen where drug ='" + sd + "' COLLATE NOCASE").fetchall()
    # spec_test = conn.execute("select * from spec_treatment_regimen where drug ='" + sd + "' COLLATE NOCASE").fetchall()
    print(spec_obj)
    # print(spec_test)
    # spec.append(spec_obj)
    # for n in spec_obj:
    #     spec.append(n[0])
    if (len(spec_obj) > 0):
        if (selected_disease == 'TB'):
            spec.append('Prevalence')
            #spec.append('Treatment coverage:')
            if spec_obj[0][0] == 'True':
                spec.append('TB/HIV+ Coverage')
            if spec_obj[0][1] == 'True':
                spec.append('TB/HIV- Coverage')
            if spec_obj[0][2] == 'True':
                spec.append('MDR-TB Coverage')
            if spec_obj[0][3] == 'True':
                spec.append('XDR-TB Coverage')
            #spec.append('Efficacy:')
            if spec_obj[0][0] == 'True':
                spec.append('TB/HIV+ Efficacy')
            if spec_obj[0][1] == 'True':
                spec.append('TB/HIV- Efficacy')
            if spec_obj[0][2] == 'True':
                spec.append('MDR-TB Efficacy')
            if spec_obj[0][3] == 'True':
                spec.append('XDR-TB Efficacy')
            #spec.append('DALY:')
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

        else:
            spec.append("All specifications")
        return json.dumps(spec)
    return "No Data Found"


# calculate Index for tb
@app.route('/get_spec_tb', methods=['GET', 'POST'])
def getSpecTB():
    print("In Tb Specifications")
    conn = connect_db()
    selected_country = request.get_json()["selected_country"]
    selected_disease = request.get_json()["selected_disease"]
    selected_drug = request.get_json()["selected_drug"]
    selected_company = request.get_json()["selected_company"]
    selected_specification = request.get_json()["selected_specification"]
    # print("Specification Name ***************")
    # print(request.get_json()["SpecificationName"])
    print(selected_specification)
    # Nutan: updated query to fetch al the deatils in one place and based on the selection populate
    # the required details.
    spec_obj = conn.execute(
        "select * from spec_2015_TB where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

    d = {}
    I = 0
    for each_spec in selected_specification:
        print(each_spec)
        #Set the required values, which will be further used to calculate Impact Score
        #and further passed to specifications page.

        TB_pevalance = spec_obj[0][1]
        if each_spec == "Prevalence":
            #TB_pevalance = spec_obj[0][1]
            d["TB Prevalence"] = TB_pevalance

        #1. Set Treatment Coverage Values
        TB_plus_coverage = spec_obj[0][2] / 100
        if each_spec == "TB/HIV+ Coverage":
            #TB_plus_coverage = spec_obj[0][2] / 100
            d["TB/HIV+ Treatment Coverage"] = TB_plus_coverage * 100

        TB_minus_coverage = spec_obj[0][3] / 100
        if each_spec == "TB/HIV- Coverage":
            #TB_minus_coverage = spec_obj[0][3] / 100
            d["TB/HIV- Treatment Coverage"] = TB_minus_coverage * 100

        TB_mdr_coverage = spec_obj[0][4] / 100
        if each_spec == "MDR-TB Coverage":
            #TB_mdr_coverage = spec_obj[0][4] / 100
            d["MDR-TB Treatment Coverage"] = TB_mdr_coverage * 100

        TB_xdr_coverage = spec_obj[0][5] / 100
        if each_spec == "XDR-TB Coverage":
            #TB_xdr_coverage = spec_obj[0][5] / 100
            d["XDR-TB Treatment Coverage"] = TB_xdr_coverage * 100

        # 2. Set Efficacy Values
        TB_plus_Efficacy = 0.78  # predefined, check handbook
        if each_spec == "TB/HIV+ Efficacy":
            #TB_plus_Efficacy = 0.78  # predefined, check handbook
            d["TB/HIV+ Efficacy"] = TB_plus_Efficacy * 100

        TB_minus_Efficacy = 0.83  # predefined, check handbook
        if each_spec == "TB/HIV- Efficacy":
            #TB_minus_Efficacy = 0.83  # predefined, check handbook
            d["TB/HIV- Efficacy"] = TB_minus_Efficacy * 100

        TB_mdr_Efficacy = 0.54  # predefined, check handbook
        if each_spec == "MDR-TB Efficacy":
            #TB_mdr_Efficacy = 0.54  # predefined, check handbook
            d["MDR-TB Efficacy"] = TB_mdr_Efficacy * 100

        TB_xdr_Efficacy = 0.30  # predefined, check handbook
        if each_spec == "XDR-TB Efficacy":
            #TB_xdr_Efficacy = 0.30  # predefined, check handbook
            d["XDR-TB Efficacy"] = TB_xdr_Efficacy * 100

        # 2. Set DALY Values
        TB_plus_DALY = spec_obj[0][6]
        if each_spec == "TB/HIV+ DALY":
            #TB_plus_DALY = spec_obj[0][6]
            d["TB/HIV+ DALYs"] = TB_plus_DALY

        TB_minus_DALY = spec_obj[0][7]
        if each_spec == "TB/HIV- DALY":
            #TB_minus_DALY = spec_obj[0][7]
            d["TB/HIV- DALYs"] = TB_minus_DALY

        TB_mdr_DALY = spec_obj[0][8]
        if each_spec == "MDR-TB DALY":
            #TB_mdr_DALY = spec_obj[0][8]
            d["MDR-TB DALYs"] = TB_mdr_DALY

        TB_xdr_DALY = spec_obj[0][9]
        if each_spec == "XDR-TB DALY":
            #TB_xdr_DALY = spec_obj[0][9]
            d["XDR-TB DALYs"] = TB_xdr_DALY

        #Calculate Original Impact Score of TB/HIV+
        TB_HIV_plus_I = ((TB_plus_DALY * TB_plus_Efficacy * TB_plus_coverage) / (
           1 - (TB_plus_Efficacy * TB_plus_coverage)))
        #I = I + TB_HIV_plus_I

        # Calculate Original Impact Score of TB/HIV-
        TB_HIV_minus_I = ((TB_minus_DALY * TB_minus_Efficacy * TB_minus_coverage) / (
                    1 - (TB_minus_Efficacy * TB_minus_coverage)))
        #I = I + TB_HIV_minus_I

        # Calculate Original Impact Score of MDR-TB
        MDR_TB_I = ((TB_mdr_DALY * TB_mdr_Efficacy * TB_mdr_coverage) / (1 - (TB_mdr_Efficacy * TB_mdr_coverage)))
        #I = I + MDR_TB_I

        # Calculate Original Impact Score of XDR-TB
        XDR_TB_I = ((TB_xdr_DALY * TB_xdr_Efficacy * TB_xdr_coverage) / (1 - (TB_xdr_Efficacy * TB_xdr_coverage)))

        #Calculate Total Impact Score
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

    selected_drug = request.get_json()["selected_drug"]
    selected_drug = selected_drug[selected_drug.find("(") + 1:selected_drug.find(")")]
    selected_drug = selected_drug.replace(" + ", "_").replace("-", "_")

    selected_specification = request.get_json()["selected_specification"]
    print(selected_specification)
    # selected_specification = ['PFalc', 'PVivax']
    d = {}
    I = 0
    conn = connect_db()
    cursor = conn.execute("select * from spec_2015_Malaria")
    names = list(map(lambda x: x[0], cursor.description))
    drug_column1 = "Eff_PVivax_" + selected_drug
    drug_column2 = "Eff_PFalc_" + selected_drug
    if drug_column1 in names:
        spec_obj_eff1 = conn.execute(
            "select " + drug_column1 + " from spec_2015_Malaria where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

    if drug_column2 in names:
        spec_obj_eff2 = conn.execute(
            "select " + drug_column2 + " from spec_2015_Malaria where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

    # spec_obj = conn.execute(
    #     "select Coverage_Malaria_PFalc,DALY_Malaria," + drug_column + "  from spec_2015_Malaria where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

    spec_obj = conn.execute(
        "select * from spec_2015_Malaria where country ='" + selected_country + "' COLLATE NOCASE").fetchall()


    for each_spec in selected_specification:
        #Set the required values, which will be further used to calculate Impact Score
        #and further passed to specifications page.
        Malaria_pevalance = spec_obj[0][1]
        if each_spec == "Prevalence":
            d["Malaria Prevalence"] = Malaria_pevalance

        # 1. Set Treatment Coverage Values
        Malaria_PFalc_coverage = spec_obj[0][2] / 100
        if each_spec == "Malaria PFalc Coverage":
            d["Malaria PFalc Coverage"] = Malaria_PFalc_coverage * 100

        Malaria_PVivax_coverage = spec_obj[0][3] / 100
        if each_spec == "Malaria PVivax Coverage":
            d["Malaria PVivax Coverage"] = Malaria_PVivax_coverage * 100

        # 2. Set DALY Values
        Malaria_PFalc_DALY = spec_obj[0][4]
        Malaria_PVivax_DALY = spec_obj[0][5]
        if each_spec == "Malaria PFalc DALY":
            d["Malaria PFalc DALY"] = Malaria_PFalc_DALY

        if each_spec == "Malaria PVivax DALY":
            d["Malaria PVivax DALY"] = Malaria_PVivax_DALY

        # 2. Set Efficacy Values
        Malaria_PFalc_Efficacy = 0
        Malaria_PVivax_Efficacy = 0
        if (len(spec_obj_eff1) > 0):
            Malaria_PFalc_Efficacy = spec_obj_eff1[0][0] / 100  # predefined, check handbook

        if (len(spec_obj_eff2) > 0):
            Malaria_PVivax_Efficacy = spec_obj_eff2[0][0] / 100

        if each_spec == "Malaria PFalc Efficacy":
            d["Malaria PFalc Efficacy"] = Malaria_PFalc_Efficacy * 100

        if each_spec == "Malaria PVivax Efficacy":
            d["Malaria PVivax Efficacy"] = Malaria_PVivax_Efficacy * 100

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

# calculate Index for worms
@app.route('/get_spec_worms', methods=['GET', 'POST'])
def getSpecWorms():
    selected_country = request.get_json()["selected_country"]
    selected_disease = request.get_json()["selected_disease"]
    selected_drug = request.get_json()["selected_drug"]
    selected_company = request.get_json()["selected_company"]
    # selected_specification = request.get_json()["selected_specification"]
    selected_specification = ['Adult', 'Children']
    I = 0
    d = {}
    # roundworm
    if (selected_disease == 'roundworm'):
        for each_spec in selected_specification:
            if each_spec == "Children":
                conn = connect_db()
                if selected_drug == "Albendazole (ALB)":
                    spec_obj = conn.execute(
                        "select worm_preSac_coverage,roundworm_prevalance_child,roundworm_Efficacy_ALB,roundworm_DALY_child from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
                elif selected_drug == "Ivermectin (IVM)":
                    spec_obj = conn.execute(
                        "select worm_preSac_coverage,roundworm_prevalance_child,roundworm_Efficacy_Ivm_Alb,roundworm_DALY_child from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
                elif selected_drug == "Mebendazole (MBD)":
                    spec_obj = conn.execute(
                        "select worm_preSac_coverage,roundworm_prevalance_child,roundworm_Efficacy_Mbd,roundworm_DALY_child from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

            if each_spec == "Adult":
                conn = connect_db()
                if selected_drug == "Albendazole (ALB)":
                    spec_obj = conn.execute(
                        "select worm_Sac_coverage,roundworm_prevalance_adult,roundworm_Efficacy_ALB,roundworm_DALY_adult from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
                elif selected_drug == "Ivermectin (IVM)":
                    spec_obj = conn.execute(
                        "select worm_Sac_coverage,roundworm_prevalance_adult,roundworm_Efficacy_Ivm_Alb,roundworm_DALY_adult from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
                elif selected_drug == "Mebendazole (MBD)":
                    spec_obj = conn.execute(
                        "select worm_Sac_coverage,roundworm_prevalance_adult,roundworm_Efficacy_Mbd,roundworm_DALY_adult from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

            roundworm_coverage = spec_obj[0][0] / 100
            roundworm_prevalance = spec_obj[0][1] / 100
            roundworm_Efficacy = spec_obj[0][2] / 100
            roundworm_DALY = spec_obj[0][3]
            d["roundworm_coverage"] = roundworm_coverage
            d["roundworm_prevalance"] = roundworm_prevalance
            d["roundworm_Efficacy"] = roundworm_Efficacy
            d["roundworm_DALY"] = roundworm_DALY
            I = (((roundworm_DALY * roundworm_coverage * roundworm_Efficacy) / (
                        1 - (roundworm_coverage * roundworm_Efficacy))) * roundworm_prevalance)
            I = I + I
            conn.close()

    # hookworm
    if (selected_disease == 'hookworm'):
        for each_spec in selected_specification:
            if each_spec == "Children":
                conn = connect_db()
                if selected_drug == "Albendazole (ALB)":
                    spec_obj = conn.execute(
                        "select worm_preSac_coverage,hookworm_prevalance_child,hookworm_Efficacy_ALB,hookworm_DALY_child from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
                elif selected_drug == "Mebendazole (MBD)":
                    spec_obj = conn.execute(
                        "select worm_preSac_coverage,hookworm_prevalance_child,hookworm_Efficacy_Mbd,hookworm_DALY_child from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

            if each_spec == "Adult":
                conn = connect_db()
                if selected_drug == "Albendazole (ALB)":
                    spec_obj = conn.execute(
                        "select worm_Sac_coverage,hookworm_prevalance_adult,hookworm_Efficacy_ALB,hookworm_DALY_adult from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
                elif selected_drug == "Mebendazole (MBD)":
                    spec_obj = conn.execute(
                        "select worm_Sac_coverage,hookworm_prevalance_adult,hookworm_Efficacy_Mbd,hookworm_DALY_adult from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

            hookworm_coverage = spec_obj[0][0] / 100
            hookworm_prevalance = spec_obj[0][1] / 100
            hookworm_Efficacy = spec_obj[0][2] / 100
            hookworm_DALY = spec_obj[0][3]
            d["hookworm_coverage"] = roundworm_coverage
            d["hookworm_prevalance"] = roundworm_prevalance
            d["hookworm_Efficacy"] = roundworm_Efficacy
            d["hookworm_DALY"] = roundworm_DALY
            I = (((hookworm_DALY * hookworm_coverage * hookworm_Efficacy) / (
                        1 - (hookworm_coverage * hookworm_Efficacy))) * hookworm_prevalance)
            I = I + I

            conn.close()

    # whipworm
    if (selected_disease == 'whipworm'):
        for each_spec in selected_specification:
            if each_spec == "Children":
                conn = connect_db()
                if selected_drug == "Albendazole (ALB)":
                    spec_obj = conn.execute(
                        "select worm_preSac_coverage,whipworm_prevalance_child,whipworm_Efficacy_ALB,whipworm_DALY_child from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
                elif selected_drug == "Ivermectin (IVM)":
                    spec_obj = conn.execute(
                        "select worm_preSac_coverage,whipworm_prevalance_child,whipworm_Efficacy_Ivm_Alb,whipworm_DALY_child from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
                elif selected_drug == "Mebendazole (MBD)":
                    spec_obj = conn.execute(
                        "select worm_preSac_coverage,whipworm_prevalance_child,whipworm_Efficacy_Mbd,whipworm_DALY_child from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

            if each_spec == "Adult":
                conn = connect_db()
                if selected_drug == "Albendazole (ALB)":
                    spec_obj = conn.execute(
                        "select worm_Sac_coverage,whipworm_prevalance_adult,whipworm_Efficacy_ALB,whipworm_DALY_adult from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
                elif selected_drug == "Ivermectin (IVM)":
                    spec_obj = conn.execute(
                        "select worm_Sac_coverage,whipworm_prevalance_adult,whipworm_Efficacy_Ivm_Alb,whipworm_DALY_adult from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
                elif selected_drug == "Mebendazole (MBD)":
                    spec_obj = conn.execute(
                        "select worm_Sac_coverage,whipworm_prevalance_adult,whipworm_Efficacy_Mbd,whipworm_DALY_adult from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

            whipworm_coverage = spec_obj[0][0] / 100
            whipworm_prevalance = spec_obj[0][1] / 100
            whipworm_Efficacy = spec_obj[0][2] / 100
            whipworm_DALY = spec_obj[0][3]
            d["whipworm_coverage"] = whipworm_coverage
            d["whipworm_prevalance"] = whipworm_prevalance
            d["whipworm_Efficacy"] = whipworm_Efficacy
            d["whipworm_DALY"] = whipworm_DALY

            I = (((whipworm_DALY * whipworm_coverage * whipworm_Efficacy) / (
                        1 - (whipworm_coverage * whipworm_Efficacy))) * whipworm_prevalance)
            I = I + I
            conn.close()
    # need to pass this dictionsry
    d["I"] = I
    return json.dumps(I)


# calculate Index for other
@app.route('/get_spec_other', methods=['GET', 'POST'])
def getSpecOther():
    selected_country = request.get_json()["selected_country"]
    selected_disease = request.get_json()["selected_disease"]
    selected_drug = request.get_json()["selected_drug"]
    # selected_company = request.get_json()["selected_company"]
    # selected_specification = request.get_json()["selected_specification"]

    d = {}
    I = 0
    if (selected_disease == 'Schistomasis'):
        conn = connect_db()
        spec_obj = conn.execute(
            "select schi_prevalance,schi_coverage,schi_Efficacy,schi_DALY from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

        schi_prevalance = spec_obj[0][0] / 100
        schi_coverage = spec_obj[0][1] / 100
        schi_Efficacy = spec_obj[0][2] / 100
        schi_DALY = spec_obj[0][3]
        d["schi_prevalance"] = schi_prevalance
        d["schi_coverage"] = schi_coverage
        d["schi_Efficacy"] = schi_Efficacy
        d["schi_DALY"] = schi_DALY
        I = (schi_DALY * schi_coverage * schi_Efficacy / (1 - schi_coverage * schi_Efficacy)) * schi_prevalance

    if (selected_disease == 'onchoceriasis'):
        conn = connect_db()
        spec_obj = conn.execute(
            "select onch_prevalance,onch_coverage,onch_Efficacy,onch_DALY from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

        onch_prevalance = spec_obj[0][0] / 100
        onch_coverage = spec_obj[0][1] / 100
        onch_Efficacy = spec_obj[0][2] / 100
        onch_DALY = spec_obj[0][3]
        d["onch_prevalance"] = onch_prevalance
        d["onch_coverage"] = onch_coverage
        d["onch_Efficacy"] = onch_Efficacy
        d["onch_DALY"] = onch_DALY
        I = (onch_DALY * onch_coverage * onch_Efficacy / (1 - onch_coverage * onch_Efficacy)) * onch_prevalance

    if (selected_disease == 'if'):
        conn = connect_db()
        spec_obj = conn.execute(
            "select LF_prevalance,LF_coverage,LF_Efficacy_DEC,LF_Efficacy_DEC_ALB,LF_Efficacy_IVM_ALB,LF_DALY from spec_2015_NTD where country ='" + selected_country + "' COLLATE NOCASE").fetchall()

        LF_prevalance = spec_obj[0][0] / 100
        LF_coverage = spec_obj[0][1] / 100
        LF_DALY = spec_obj[0][5]
        if (selected_drug == 'Albendazole (ALB)'):
            LF_Efficacy = spec_obj[0][2] / 100
        elif (selected_drug == 'Diethylcarbamazine (DEC)'):
            LF_Efficacy = spec_obj[0][3] / 100
        elif (selected_drug == 'Ivermectin (IVM)'):
            LF_Efficacy = spec_obj[0][4] / 100

        d["LF_prevalance"] = LF_prevalance
        d["LF_coverage"] = LF_coverage
        d["LF_Efficacy"] = LF_Efficacy
        d["LF_DALY"] = LF_DALY
        I = (LF_DALY * LF_coverage * LF_Efficacy / (1 - LF_coverage * LF_Efficacy)) * LF_prevalance
    # need to pass this dictionsry
    d["I"] = I
    return json.dumps(I)


# specification end




@app.route('/get_result', methods=['GET', 'POST'])
def getResults():
    print("In Results")
    conn = connect_db()
    selected_country = "India"
    selected_disease = "TB"

    # selected_country = request.get_json()["selected_country"]
    # selected_disease = request.get_json()["selected_disease"]
    # selected_company = request.get_json()["selected_company"]
    # selected_drug = request.get_json()["selected_drug"]
    updated_spec = request.get_json()["updated_specification"]
    print(updated_spec)
    selected_country_test = updated_spec["state"]
    print("selected_country_test",selected_country_test)
    updated_specification = updated_spec["data"]
    print(updated_specification)

    if (selected_disease == "TB"):
        spec_obj = conn.execute(
            "select * from spec_2015_TB where country ='" + selected_country + "' COLLATE NOCASE").fetchall()
        d = {}
        I = 0
        for each_spec in updated_specification:
            print(each_spec)
            # Set the required values, which will be further used to calculate Impact Score
            # and further passed to specifications page.
            TB_pevalance = spec_obj[0][1]
            if each_spec == "TB Prevalence":
                TB_pevalance = updated_specification["TB Prevalence"]

            # 1. Set Treatment Coverage Values
            TB_plus_coverage = spec_obj[0][2] / 100
            if each_spec == "TB/HIV+ Treatment Coverage":
                TB_plus_coverage = updated_specification["TB/HIV+ Treatment Coverage"]

            TB_minus_coverage = spec_obj[0][3] / 100
            if each_spec == "TB/HIV- Treatment Coverage":
                TB_minus_coverage = updated_specification["TB/HIV- Treatment Coverage"]

            TB_mdr_coverage = spec_obj[0][4] / 100
            if each_spec == "MDR-TB Treatment Coverage":
                TB_mdr_coverage = updated_specification["MDR-TB Treatment Coverage"]

            TB_xdr_coverage = spec_obj[0][5] / 100
            if each_spec == "XDR-TB Treatment Coverage":
                updated_specification["XDR-TB Treatment Coverage"] = TB_xdr_coverage * 100

            # 2. Set Efficacy Values
            TB_plus_Efficacy = 0.78
            if each_spec == "TB/HIV+ Efficacy":
                TB_plus_Efficacy = updated_specification["TB/HIV+ Efficacy"]

            TB_minus_Efficacy = 0.83  # predefined, check handbook
            if each_spec == "TB/HIV- Efficacy":
                TB_minus_Efficacy = updated_specification["TB/HIV- Efficacy"]

            TB_mdr_Efficacy = 0.54  # predefined, check handbook
            if each_spec == "MDR-TB Efficacy":
                # TB_mdr_Efficacy = 0.54  # predefined, check handbook
                TB_mdr_Efficacy = updated_specification["MDR-TB Efficacy"]

            TB_xdr_Efficacy = 0.30  # predefined, check handbook
            if each_spec == "XDR-TB Efficacy":
                # TB_xdr_Efficacy = 0.30  # predefined, check handbook
                TB_xdr_Efficacy = updated_specification["XDR-TB Efficacy"]

            # 2. Set DALY Values
            TB_plus_DALY = spec_obj[0][6]
            if each_spec == "TB/HIV+ DALY":
                TB_plus_DALY = updated_specification["TB/HIV+ DALYs"]

            TB_minus_DALY = spec_obj[0][7]
            if each_spec == "TB/HIV- DALY":
                TB_minus_DALY = updated_specification["TB/HIV- DALYs"]

            TB_mdr_DALY = spec_obj[0][8]
            if each_spec == "MDR-TB DALY":
                TB_mdr_DALY = updated_specification["MDR-TB DALYs"]

            TB_xdr_DALY = spec_obj[0][9]
            if each_spec == "XDR-TB DALY":
                TB_xdr_DALY = updated_specification["XDR-TB DALYs"]

            # Calculate New Impact Score of TB/HIV+
            TB_HIV_plus_newI = ((TB_plus_DALY * TB_plus_Efficacy * TB_plus_coverage) / (
                    1 - (TB_plus_Efficacy * TB_plus_coverage)))
            # I = I + TB_HIV_plus_I

            # Calculate Original Impact Score of TB/HIV-
            TB_HIV_minus_newI = ((TB_minus_DALY * TB_minus_Efficacy * TB_minus_coverage) / (
                    1 - (TB_minus_Efficacy * TB_minus_coverage)))
            # I = I + TB_HIV_minus_I

            # Calculate Original Impact Score of MDR-TB
            MDR_TB_newI = ((TB_mdr_DALY * TB_mdr_Efficacy * TB_mdr_coverage) / (1 - (TB_mdr_Efficacy * TB_mdr_coverage)))
            # I = I + MDR_TB_I

            # Calculate Original Impact Score of XDR-TB
            XDR_TB_newI = ((TB_xdr_DALY * TB_xdr_Efficacy * TB_xdr_coverage) / (1 - (TB_xdr_Efficacy * TB_xdr_coverage)))

            # Calculate Total Impact Score
            newI = TB_HIV_plus_newI + TB_HIV_minus_newI + MDR_TB_newI + XDR_TB_newI

        d["New Impact Score"] = round(newI, 2)
        print("New Impact Score")
        print(newI)
        countries_obj = conn.execute("select country,total from country2015").fetchall()
        d["Other Countries"] = countries_obj
        # print(countries_obj)
        print(d)

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
