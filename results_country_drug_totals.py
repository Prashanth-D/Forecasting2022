import sqlite3
import pandas as pd
import unicodedata
import math

def createTablesSpec():
    conn = sqlite3.connect('K_ghi.db')
    # Regimen Distribution
    conn.execute(''' DROP TABLE IF EXISTS results_country_drug_totals ''')
    conn.execute(''' DROP TABLE IF EXISTS results_country_drug_totals2015 ''')
    conn.execute(''' CREATE TABLE results_country_drug_totals2015 (country text, drug0 real, drug1 real, drug2 real, drug3 real, drug4 real, drug5 real, drug6 real, drug7 real, drug8 real, drug9 real, drug10 real, drug11 real, drug12 real, drug13 real, drug14 real, drug15 real, drug16 real, drug17 real, drug18 real, drug19 real, drug20 real, drug21 real, drug22 real, drug23 real, drug24 real, drug25 real, drug26 real, drug27 real, drug28 real, drug29 real, drug30 real, drug31 real, drug32 real, drug33 real, drug34 real, drug35 real, drug36 real, drug37 real, drug38 real, drug39 real, drug40 real, drug41 real, drug42 real, drug43 real, drug44 real, drug45 real, drug46 real, drug47 real, drug48 real, drug49 real, drug50 real, drug51 real, TOTAL real) ''')
    conn.execute(''' DROP TABLE IF EXISTS results_country_drug_totals2013 ''')
    conn.execute(''' CREATE TABLE results_country_drug_totals2013 (country text, drug0 real, drug1 real, drug2 real, drug3 real, drug4 real, drug5 real, drug6 real, drug7 real, drug8 real, drug9 real, drug10 real, drug11 real, drug12 real, drug13 real, drug14 real, drug15 real, drug16 real, drug17 real, drug18 real, drug19 real, drug20 real, drug21 real, drug22 real, drug23 real, drug24 real, drug25 real, drug26 real, drug27 real, drug28 real, drug29 real, drug30 real, drug31 real, drug32 real, drug33 real, drug34 real, drug35 real, drug36 real, drug37 real, drug38 real, drug39 real, drug40 real, drug41 real, drug42 real, drug43 real, drug44 real, drug45 real, drug46 real, drug47 real, drug48 real, drug49 real, drug50 real, drug51 real, drug52 real, TOTAL real) ''')
    conn.execute(''' DROP TABLE IF EXISTS results_country_drug_totals2010 ''')
    conn.execute(''' CREATE TABLE results_country_drug_totals2010 (country text, drug0 real, drug1 real, drug2 real, drug3 real, drug4 real, drug5 real, drug6 real, drug7 real, drug8 real, drug9 real, drug10 real, drug11 real, drug12 real, drug13 real, drug14 real, drug15 real, drug16 real, drug17 real, drug18 real, drug19 real, drug20 real, drug21 real, drug22 real, drug23 real, drug24 real, drug25 real, drug26 real, drug27 real, drug28 real, drug29 real, drug30 real, drug31 real, drug32 real, drug33 real, drug34 real, drug35 real, drug36 real, drug37 real, drug38 real, drug39 real, drug40 real, drug41 real, drug42 real, drug43 real, drug44 real, drug45 real, drug46 real, drug47 real, drug48 real, drug49 real, drug50 real, TOTAL real) ''')
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
        createTablesSpec()
        is_df_true = df1.notnull()
        table_data1 = []
        for i in range(4, 221):
            row = []
            rtotal = 0
            country = df1.iloc[i, 0]
            row.append(country)
            for j in range(1, 53):
                drugj = df1.iloc[i,j]
                rtotal += float(drugj)
                row.append(drugj)
            row.append(rtotal)
            table_data1.append(row)
        for k in table_data1:
            conn.execute(''' INSERT INTO results_country_drug_totals2015 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', k)
        print("Database operation compelete")
        is_df_true = df2.notnull()
        table_data2 = []
        for i in range(2, 219):
            row = []
            rtotal = 0
            country = df2.iloc[i, 0]
            row.append(country)
            for j in range(1, 54):
                drugj = df2.iloc[i,j]
                if math.isnan(float(drugj)) == False:
                    rtotal += float(drugj)
                else:
                    drugj = 0
                row.append(drugj)
            row.append(rtotal)
            table_data2.append(row)
        for k in table_data2:
            conn.execute(''' INSERT INTO results_country_drug_totals2013 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', k)
        print("Database operation compelete")
        is_df_true = df3.notnull()
        table_data3 = []
        for i in range(2, 219):
            row = []
            rtotal = 0
            country = df3.iloc[i, 0]
            print(country)
            row.append(country)
            for j in range(1, 52):
                drugj = df3.iloc[i,j]
                if math.isnan(float(drugj)) == False:
                    rtotal += float(drugj)
                else:
                    drugj = 0
                row.append(drugj)
            row.append(rtotal)
            table_data3.append(row)
        for k in table_data3:
            print(k)
            conn.execute(''' INSERT INTO results_country_drug_totals2010 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', k)
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