import sqlite3
import pandas as pd
import unicodedata
import math

def createTablesCountry():
    print ("In create Table")
    #conn = sqlite3.connect('/home/globalhealth/mysite/ghi.db')
    # conn = sqlite3.connect('C:/Users/Nutan/Desktop/Masters/GHI Internship/Forecasting tool/MyChanges/ghi.db') 
    conn = sqlite3.connect('K_ghi.db')
    conn.execute(''' DROP TABLE IF EXISTS countryDrug2015 ''')
    conn.execute(''' CREATE TABLE countryDrug2015 (country text, drug text, company text, score real) ''')
    # conn.execute(''' CREATE TABLE countryDrug2015 (country text, drug text, score real) ''')
    conn.close()
    print ("Table Created")
    return

def countrydbUpdate():
    print ("In countrydbUpdate")
    # conn = sqlite3.connect('C:/Users/Nutan/Desktop/Masters/GHI Internship/Forecasting tool/MyChanges/ghi.db')
    conn = sqlite3.connect('K_ghi.db')
    url = "countrydrug2015.csv"
    df = pd.read_csv(url, skiprows=2)
    
    try:
        createTablesCountry()   

        is_df_true = df.notnull()
        def clean(value):
            try:
                strVal = str(value)
                if '-' in strVal:
                    resVal = strVal.replace('-', '0')
                elif ',' in strVal:
                    resVal = strVal.replace(',', '')
                else:
                    resVal = strVal
                resVal = float(resVal)
                return resVal
            except:
                return 0
        
        #Countries - at location row = 1 onwards and column=0 (1,0  2,0  3,0 ...)
        # Drugs (output row) - Row = 0 and column = 1 onwards ((0,0) will give "Output" ) (0,1  0,2 ..)
        #Impact socre starts : Row = 1 Onwards and column = 1 Onwards  
        print ("Processing started")       
        countryDrugData = {}
        impactScore=0

        for j in range (1,65):
            if ((pd.isnull(df.iloc[0,j])) or ((df.iloc[0,j]) == " ")):
                # print ("Drug column Empty 2")
                continue
            
            for i in range(0, 218):
                if (i==0):
                    # drug = df.iloc[i,1]  
                    drug = df.iloc[i,j]
                    # print ("drug: ", drug)
                    companyDrug = drug.split(", ")
                else:
                    country = df.iloc[i,0]
                    if not (country in countryDrugData):
                        countryDrugData.update ({country: {}}) 
                    
                    if ((pd.isnull(df.iloc[i,j])) or ((df.iloc[i,j]) == " ") or ((df.iloc[i,j]) == "0")
                        or ((df.iloc[i,j]) == "-")):
                        impactScore = 0.0
                    else: 
                        impactScore = df.iloc[i,j]
                        # print(impactScore)   
                        if (impactScore.isnumeric()):
                            # print("isNumeric")
                            impactScore = float(impactScore)
                        else: 
                            if ("," in impactScore):
                                # print("replace comma ")                         
                                impactScore = impactScore.replace(',' , '')
                                impactScore = float(impactScore)
                            else:
                                # print("Default")
                                impactScore = float(impactScore)        
 
                    for drugs in companyDrug:
                        drugs = drugs.strip()
                        totImpactScore = impactScore
                        # if (country in countryDrugData):
                        # print("key Exists"  + country)
                        for drugKey in countryDrugData[country]:
                            if (drugKey.lower() == drugs.lower()):
                                # print ("key Exist, new drugs value")
                                drugs = drugKey
                                break
    
                        if (drugs in countryDrugData[country]):
                            oldImpactScore = countryDrugData[country][drugs]                         
                            totImpactScore = oldImpactScore + impactScore
                            totImpactScore = round(totImpactScore,2)
                       
                        # else:   
                        countryDrugData[country].update({drugs: totImpactScore})
                        # else:
                        #     print ("New Country")
                        #     countryDrugData.update ({country: {drugs: impactScore}})                

        # print ("*** Printing Second method *****")
        # print (countryDrugData)    

        countryDrugDataFinal = []
        cmpny=""
        # for country in countryDrugData:
        #     for drugs in (countryDrugData[country]):
        #         drugToMatch = drugs.split(" (")
        #         # print(drugToMatch)
        #         company = conn.execute("select distinct drug,company from drugr2015 where drug like'%"+drugToMatch[0]+"%'COLLATE NOCASE").fetchall()
        #         cmpny=""
        #         if(len(company) >0 ):
        #             cmpny = company[0][1]
        #
        #         row = [country,drugs,cmpny,countryDrugData[country][drugs]]
        #         countryDrugDataFinal.append(row)


        for country in countryDrugData:
            for drugs in (countryDrugData[country]):
                drugToMatch = drugs.split(" (")
                print(drugs)
                # company = conn.execute("select distinct Drug,Company from results_impact_map2015 where Drug like'"+drugToMatch[0]+"%'COLLATE NOCASE").fetchall()
                company = conn.execute(
                    "select distinct Drug,Company from results_impact_map2015 where Drug=trim('" + drugs + "') COLLATE NOCASE").fetchall()
                    # "Drug = '" + drugToMatch[0] + "'COLLATE NOCASE").fetchall()
                cmpny=""
                drug_from_result = ""
                if(len(company) >0 ):
                    cmpny = company[0][1]
                    drug_from_result = company[0][0]
                    score_to_upd = countryDrugData[country][drugs]
                    # row = [country,drugs,cmpny,countryDrugData[country][drugs]]
                    country = country.strip()
                    if (score_to_upd > 0):
                        row = [country, drug_from_result, cmpny, score_to_upd]
                        countryDrugDataFinal.append(row)

        for k in countryDrugDataFinal:
            conn.execute(''' INSERT INTO countryDrug2015 VALUES (?,?,?,?) ''', k)
        conn.commit()
        conn.close()
        print("Database operation compelete")
        return 'success'

    except Exception as e:
        error = e
        print ("ERROR:" + error)
        conn.rollback()
        conn.close()
        return error
    return df

countrydbUpdate()
