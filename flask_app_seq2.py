# -*- coding: utf-8 -*-
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template, request
import xlrd, pandas,os,sqlite3,json
from collections import defaultdict
import numpy as np
from flask import request


app = Flask(__name__)
pandas.option_context('display.max_rows', None, 'display.max_columns', None)
DATABASE = 'ghi.db'
mapping = {2:"tb", 3:"malaria", 4:"hiv", 5:"roundworm", 6:"hookworm", 7:"whipworm", 8: "chistomiaisis",  9:"onchoceriasis", 9: "chistomiaisis", 10:"if"}

app.config.from_object(__name__)
def connect_db():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'ghi.db')
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
    years = [2010,2013,2015]
    return (years)

@app.route('/get_countries_by_region')
def get_countries_by_region():
    conn = connect_db()
    region = request.args.get("selected_region")
    if(region == 'All Countries'):
        return getAllCountries()
    else:
        return (conn.execute("select country from country2015 where region ='"+str(region)+"'").fetchall())


# drug->country->disease->Company

@app.route('/drug', methods = ['GET','POST'])
def getAllDrugs():
    conn = connect_db()
    drugs_obj = conn.execute("select drug from drug2015").fetchall()
    drugs_list = [i[0] for i in drugs_obj]
    #remove duplicates
    drugs_list = list(set(drugs_list))
    #alphebatize
    drugs_list.sort()
    return json.dumps(drugs_list)

@app.route('/get_country_by_drug', methods = ['GET' , 'POST'])
def getCountrybyDrug():
    conn = connect_db()
    drug = request.get_json()["selected_drug"]
    #had to use lower case because of mismatches in databases
    drug = drug.lower()
    countries_obj = conn.execute("select country from countryDrug2015 where LOWER(drug) ='" + drug +"' AND score > 0").fetchall()
    list_of_countries = [i[0] for i in countries_obj]
    #alphebatize
    list_of_countries.sort()
    return json.dumps(list_of_countries)


@app.route('/get_disease_by_drug', methods = ['GET','POST'])
def getDiseaseFromCountryandDrug():
    country_select = request.get_json()["selected_country"]
    drug = request.get_json()["selected_drug"]
    drug = drug.lower()
    conn = connect_db()
    diseases = []
    countries_obj = conn.execute("select * from country2015 where country = " + "' " + str(country_select) +"'").fetchall()

    enumerate(countries_obj)

    if(len(countries_obj) > 0 ):
        for idx, val in enumerate(countries_obj[0][2:]):
            #print(idx)
            #print(diseases)
            if(val > 0):
                diseases.append(mapping[idx+2])
        #disease now all diseases associated with country. We will now filter out all diseases not treated by selected_drug
        print(diseases)
        diseases_final = []
        for disease in diseases:
            print("checking", disease)
            if(conn.execute("select disease from drug2015 where LOWER(drug) ='"+ drug +"'AND  LOWER(disease) ='" + disease.lower() +"'").fetchall()):
                print("adding: ", disease)
                diseases_final.append(disease)
        #remove duplicates
        diseases_final = list(set(diseases_final))
        #alphebatize
        diseases_final.sort()
        return json.dumps(diseases_final)
    return "No data found"

@app.route('/get_company_by_drug', methods = ['GET','POST'])
def getCompanyByDiseaseAndCountryAndDrug():
    drug = request.get_json()["selected_drug"]
    country = request.get_json()["selected_country"]
    disease = request.get_json()["selected_disease"]

    conn = connect_db()

    #filter by drug and country
    company_obj = conn.execute("select company from countryDrug2015 where score > 0 AND LOWER(drug) ='"+drug.lower()+"' AND LOWER(country) ='" +country.lower()+"'").fetchall()
    companies_obj = [i[0] for i in company_obj]

    #if there are multiple unique companies, filter through diseases as well
    companies_obj_final = []
    companies_obj = list(set(companies_obj))
    companies_obj.append("Sanofi")
    if(len(companies_obj) > 1):
        compDisObj = conn.execute("select company from drug2015 where score > 0 AND LOWER(drug) ='" + drug.lower() + "' AND LOWER(disease) ='" +disease.lower()+"'").fetchall()
        compDisObj = [i[0] for i in compDisObj]
        #filter companies by drug, country, and disease
        companies_obj_final = list(set(set(compDisObj).intersection(set(companies_obj))))
    else:
        companies_obj_final = companies_obj

    #make sure things don't print out awkwardly if there is one unique answer
    if(len(companies_obj_final) == 1):
        retVal = [1]
        retVal[0] = companies_obj[0]
        return json.dumps(retVal)

    #alphebatize
    companies_obj_final.sort()
    return json.dumps(companies_obj_final)




# print getDiseaseFromCountry(" Albania")
# print getDrugByDisease('TB')
# print getCompanyByDrug("Lamivudine (3TC)")


# drug->country->disease->Company
'''
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
    obj = conn.execute("select * from country2015 where country ="+country).fetchall()
    for idx, val in enumerate(obj[0][2:]):
        if(val > 0):
            countries.append(mapping[idx+2])
    return countries
#can use the above company by disease for next function


#disease -> country -> drug-> company
def getAllDisease():
    obj = conn.execute("select disease from disease2015").fetchall()
    return obj

def getCompanybyDisease(disease):
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
    obj = conn.execute("select country from countrybydis2010 where "+ disease +"> 0").fetchall()
    return obj




# company -> Country -> disease -> drug
def getAllCompanies():
    conn = connect_db()
    obj = conn.execute("select manufacturer from manufacturer").fetchall()
    return obj

#can use the getCountrybyDisease function from the first sequence

def getCountryByCompany(selected_company):
    conn = connect_db()
    #get drug by company
    drug_obj =  conn.execute("select drug from drug2015 where company='"+selected_company+"'").fetchall()
    # for each_drug in drug_obj:
    #     #will need harshal's table here
    # return obj
    return drug_obj

def getDrugByCountry(selected_country):
    conn = connect_db()
    obj = conn.execute("select distype from distypes where country = '"+selected_country+"'").fetchall()
    return obj

def getDrugbyCompany():
    conn = connect_db()
'''
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)

# @app.errorhandler(500)
# def internal_error_500(e):
#     return render_template('error500.html',showindex=1, navsub=1), 500

if __name__ == '__main__':
    app.run(debug=False)
