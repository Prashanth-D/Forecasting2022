import sqlite3
import pandas as pd
import unicodedata

def createTablesSpec():
    conn = sqlite3.connect('K_ghi.db')
    # Regimen Distribution
    conn.execute(''' DROP TABLE IF EXISTS results_disease_drug_map ''')
    conn.execute(''' DROP TABLE IF EXISTS results_disease_drug_map2015 ''')
    conn.execute(''' CREATE TABLE results_disease_drug_map2015 (regimen text, TB real, Malaria real, HIV real, Roundworm real, Hookworm real, Whipworm real, Schistomasis real, Onchocerciasis real, LF real) ''')
    conn.execute(''' DROP TABLE IF EXISTS results_disease_drug_map2013 ''')
    conn.execute(''' CREATE TABLE results_disease_drug_map2013 (regimen text, TB real, Malaria real, HIV real, Roundworm real, Hookworm real, Whipworm real, Schistomasis real, Onchocerciasis real, LF real) ''')
    conn.execute(''' DROP TABLE IF EXISTS results_disease_drug_map2010 ''')
    conn.execute(''' CREATE TABLE results_disease_drug_map2010 (regimen text, TB real, Malaria real, HIV real, Roundworm real, Hookworm real, Whipworm real, Schistomasis real, Onchocerciasis real, LF real) ''')
    conn.close()
    return

# 0 - 13 = TB, 14 - 27 = Malaria, 28 - 38 = HIV, 39 - 41 = Roundworm, 42 - 43 = Hookworm, 44 - 46 = Whipworm, 47 = Schistomasis, 48 = Onchocerciasis, 49-51 = LF

def uploadSpecData():
    conn = sqlite3.connect('K_ghi.db')
    url1 = "1-1country_drug2015.csv"
    df1 = pd.read_csv(url1, skiprows=1)
    url2 = "1-1country_drug2013.csv"
    df2 = pd.read_csv(url2)
    url3 = "1-1country_drug2010.csv"
    df3 = pd.read_csv(url3)
    try:
        createTablesSpec()
        dict1 = {}
        is_df_true = df1.notnull()
        for i in range(1, 53):
            drug = df1.iloc[0, i]
            index = 0
            if i >= 1 and i <15:
                index = 1
            elif i >= 15 and i < 29:
                index = 2
            elif i >= 29 and i < 40:
                index = 3
            elif i >= 40 and i < 43:
                index = 4
            elif i == 43 or i == 44:
                index = 5
            elif i >= 45 and i < 48:
                index = 6
            elif i == 48:
                index = 7
            elif i == 49:
                index = 8
            elif i >= 50 and i < 53:
                index = 9
            if drug in dict1:
                dict1[drug][index] = i-1
            else:
                dict1[drug] = [drug, -1, -1, -1, -1, -1, -1, -1, -1, -1]
                dict1[drug][index] = i-1
            # print(dict1)
        for k in dict1.values():
            # print(k)
            conn.execute(''' INSERT INTO results_disease_drug_map2015 VALUES (?,?,?,?,?,?,?,?,?,?)''', k)
        print("Database operation compelete")
        dict2 = {}
        is_df_true = df2.notnull()
        for i in range(1, 54):
            # drug = df2.iloc[0, i]
            drug = df2.iloc[1, i]
            # print(drug)
            # print(df2.iloc[1, i])
            index = 0
            if i >= 1 and i <15:
                index = 1
            elif i >= 15 and i < 30:
                index = 2
            elif i >= 30 and i < 41:
                index = 3
            elif i >= 41 and i < 44:
                index = 4
            elif i == 44 or i == 45:
                index = 5
            elif i >= 46 and i < 49:
                index = 6
            elif i == 49:
                index = 7
            elif i == 50:
                index = 8
            elif i >= 51 and i < 54:
                index = 9
            if drug in dict2:
                dict2[drug][index] = i-1
            else:
                dict2[drug] = [drug, -1, -1, -1, -1, -1, -1, -1, -1, -1]
                dict2[drug][index] = i-1
        for k in dict2.values():

            conn.execute(''' INSERT INTO results_disease_drug_map2013 VALUES (?,?,?,?,?,?,?,?,?,?)''', k)
        print("Database operation compelete")
        dict3 = {}
        is_df_true = df3.notnull()
        for i in range(1, 52):
            drug = df3.iloc[1, i]
            # print(drug)
            index = 0
            if i >= 1 and i <15:
                index = 1
            elif i >= 15 and i < 27:
                index = 2
            elif i >= 27 and i < 39:
                index = 3
            elif i >= 39 and i < 42:
                index = 4
            elif i == 42 or i == 43:
                index = 5
            elif i >= 44 and i < 47:
                index = 6
            elif i == 47:
                index = 7
            elif i == 48:
                index = 8
            elif i >= 49 and i < 52:
                index = 9
            if drug in dict3:
                dict3[drug][index] = i-1
            else:
                dict3[drug] = [drug, -1, -1, -1, -1, -1, -1, -1, -1, -1]
                dict3[drug][index] = i-1
        for k in dict3.values():
            print(k)
            conn.execute(''' INSERT INTO results_disease_drug_map2010 VALUES (?,?,?,?,?,?,?,?,?,?)''', k)
        print("Database operation compelete")
        conn.commit()
        return 'success'
    except Exception as e:
        error = e
        conn.rollback()
        conn.close()
        return error
    return df

uploadSpecData()