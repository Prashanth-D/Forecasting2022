import sqlite3
import pandas as pd
import unicodedata

def createTablesSpec():
    conn = sqlite3.connect('K_ghi.db')
    conn.execute(''' DROP TABLE IF EXISTS results_impact_map ''')
    conn.execute(''' DROP TABLE IF EXISTS results_impact_map2015 ''')
    conn.execute(''' CREATE TABLE results_impact_map2015 (Country text, Drug text, Disease text, Company text, Impact real) ''')
    conn.execute(''' DROP TABLE IF EXISTS results_impact_map2013 ''')
    conn.execute(''' CREATE TABLE results_impact_map2013 (Country text, Drug text, Disease text, Company text, Impact real) ''')
    conn.execute(''' DROP TABLE IF EXISTS results_impact_map2010 ''')
    conn.execute(''' CREATE TABLE results_impact_map2010 (Country text, Drug text, Disease text, Company text, Impact real) ''')
    conn.close()
    return

def findCompany(map, index):
    company = ""
    for i in range(len(map)):
        for j in range(len(map[0])):
            if (map[i][j] == index):
                company = map[i][0]
    return company

def uploadSpecData():
    conn = sqlite3.connect('K_ghi.db')
    disease_map2015 = conn.execute('select * from results_disease_drug_map2015').fetchall()
    disease_map2013 = conn.execute('select * from results_disease_drug_map2013').fetchall()
    disease_map2010 = conn.execute('select * from results_disease_drug_map2010').fetchall()
    country_drug_map2015 = conn.execute('select * from results_country_drug_totals2015').fetchall()
    country_drug_map2013 = conn.execute('select * from results_country_drug_totals2013').fetchall()
    country_drug_map2010 = conn.execute('select * from results_country_drug_totals2010').fetchall()
    company_map2015 = conn.execute('select * from results_company_drug_map2015').fetchall()
    company_map2013 = conn.execute('select * from results_company_drug_map2013').fetchall()
    company_map2010 = conn.execute('select * from results_company_drug_map2010').fetchall()
    try:
        createTablesSpec()
        tdata1 = []
        for i in range(len(country_drug_map2015)):
            country = country_drug_map2015[i][0]
            for j in range(len(disease_map2015)):
                drug = disease_map2015[j][0]
                for k in range(1, len(disease_map2015[0])):
                    index = disease_map2015[j][k]
                    if index != -1:
                        disease = ""
                        if k == 1: disease = "TB"
                        elif k == 2: disease = "Malaria"
                        elif k == 3: disease = "HIV"
                        elif k == 4: disease = "Roundworm"
                        elif k == 5: disease = "Hookworm"
                        elif k == 6: disease = "Whipworm"
                        elif k == 7: disease = "Schistomasis"
                        elif k == 8: disease = "Onchocerciasis"
                        elif k == 9: disease = "LF"
                        company = findCompany(company_map2015, index)
                        impact = country_drug_map2015[i][int(index)+1]
                        if(impact > 0):
                            trow = [country, drug, disease, company, impact]
                            tdata1.append(trow)
        for x in tdata1:
            conn.execute(''' INSERT INTO results_impact_map2015 VALUES (?,?,?,?,?)''', x)
        print("Database operation compelete")
        tdata2 = []
        for i in range(len(country_drug_map2013)):
            country = country_drug_map2013[i][0]
            for j in range(len(disease_map2013)):
                drug = disease_map2013[j][0]
                for k in range(1, len(disease_map2013[0])):
                    index = disease_map2013[j][k]
                    if index != -1:
                        disease = ""
                        if k == 1: disease = "TB"
                        elif k == 2: disease = "Malaria"
                        elif k == 3: disease = "HIV"
                        elif k == 4: disease = "Roundworm"
                        elif k == 5: disease = "Hookworm"
                        elif k == 6: disease = "Whipworm"
                        elif k == 7: disease = "Schistomasis"
                        elif k == 8: disease = "Onchocerciasis"
                        elif k == 9: disease = "LF"
                        company = findCompany(company_map2013, index)
                        impact = country_drug_map2013[i][int(index)+1]
                        if(impact > 0):
                            trow = [country, drug, disease, company, impact]
                            tdata2.append(trow)
        for x in tdata2:
            conn.execute(''' INSERT INTO results_impact_map2013 VALUES (?,?,?,?,?)''', x)
        print("Database operation compelete")
        tdata3 = []
        for i in range(len(country_drug_map2010)):
            country = country_drug_map2010[i][0]
            for j in range(len(disease_map2010)):
                drug = disease_map2010[j][0]
                for k in range(1, len(disease_map2010[0])):
                    index = disease_map2010[j][k]
                    if index != -1:
                        disease = ""
                        if k == 1: disease = "TB"
                        elif k == 2: disease = "Malaria"
                        elif k == 3: disease = "HIV"
                        elif k == 4: disease = "Roundworm"
                        elif k == 5: disease = "Hookworm"
                        elif k == 6: disease = "Whipworm"
                        elif k == 7: disease = "Schistomasis"
                        elif k == 8: disease = "Onchocerciasis"
                        elif k == 9: disease = "LF"
                        company = findCompany(company_map2010, index)
                        impact = country_drug_map2010[i][int(index)+1]
                        if(impact > 0):
                            trow = [country, drug, disease, company, impact]
                            tdata3.append(trow)
        for x in tdata3:
            print(x)
            conn.execute(''' INSERT INTO results_impact_map2010 VALUES (?,?,?,?,?)''', x)
        print("Database operation compelete")
        conn.commit()
        return 'success'
    except Exception as e:
        error = e
        conn.rollback()
        conn.close()
        return error
    return

uploadSpecData()