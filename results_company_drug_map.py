import sqlite3
import pandas as pd
import unicodedata
import math

def createTablesSpec():
    conn = sqlite3.connect('K_ghi.db')
    # Regimen Distribution
    conn.execute(''' DROP TABLE IF EXISTS results_company_drug_map ''')
    conn.execute(''' DROP TABLE IF EXISTS results_company_drug_map2015 ''')
    conn.execute(''' CREATE TABLE results_company_drug_map2015 (Company text, index0 real, index1 real, index2 real, index3 real, index4 real, index5 real, index6 real) ''')
    conn.execute(''' DROP TABLE IF EXISTS results_company_drug_map2013 ''')
    conn.execute(''' CREATE TABLE results_company_drug_map2013 (Company text, index0 real, index1 real, index2 real, index3 real, index4 real, index5 real, index6 real) ''')
    conn.execute(''' DROP TABLE IF EXISTS results_company_drug_map2010 ''')
    conn.execute(''' CREATE TABLE results_company_drug_map2010 (Company text, index0 real, index1 real, index2 real, index3 real, index4 real, index5 real, index6 real) ''')
    conn.close()
    return

def uploadSpecData():
    conn = sqlite3.connect('K_ghi.db')
    url1 = "1-1country_drug2015.csv"
    df1 = pd.read_csv(url1)
    url2 = "1-1country_drug2013.csv"
    df2 = pd.read_csv(url2)
    url3 = "1-1country_drug2010.csv"
    df3 = pd.read_csv(url3)
    try:
        dict1 = {}
        createTablesSpec()
        is_df_true = df1.notnull()
        for i in range(1, 53):
            company = df1.iloc[0, i]
            if company in dict1:
                for j in range(1, 8):
                    if dict1[company][j] == -1:
                        dict1[company][j] = i-1
                        break
            else:
                dict1[company] = [company, -1, -1, -1, -1, -1, -1, -1]
                dict1[company][1] = i-1
        for k in dict1.values():
            conn.execute(''' INSERT INTO results_company_drug_map2015 VALUES (?,?,?,?,?,?,?,?)''', k)
        print("Database operation compelete 2015")
        dict2 = {}
        is_df_true = df2.notnull()
        for i in range(1, 54):
            company = df2.iloc[0, i]
            if company in dict2:
                for j in range(1, 8):
                    if dict2[company][j] == -1:
                        dict2[company][j] = i-1
                        break
            else:
                dict2[company] = [company, -1, -1, -1, -1, -1, -1, -1]
                dict2[company][1] = i-1
        for k in dict2.values():
            conn.execute(''' INSERT INTO results_company_drug_map2013 VALUES (?,?,?,?,?,?,?,?)''', k)
        print("Database operation compelete 2013")
        dict3 = {}
        is_df_true = df3.notnull()
        for i in range(1, 52):
            company = df3.iloc[0, i]
            print(company)
            if company in dict3:
                for j in range(1, 8):
                    if dict3[company][j] == -1:
                        dict3[company][j] = i-1
                        break
            else:
                dict3[company] = [company, -1, -1, -1, -1, -1, -1, -1]
                dict3[company][1] = i-1
        for k in dict3.values():
            conn.execute(''' INSERT INTO results_company_drug_map2010 VALUES (?,?,?,?,?,?,?,?)''', k)
        print("Database operation compelete 2010")
        conn.commit()
        return 'success'
    except Exception as e:
        error = e
        conn.rollback()
        conn.close()
        return error
    return [df1,df2,df3]

uploadSpecData()