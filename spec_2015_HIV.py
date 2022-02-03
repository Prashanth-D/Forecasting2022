import sqlite3
import pandas as pd
import unicodedata

def createTablesSpec():
    conn = sqlite3.connect('K_ghi.db')
    conn.execute(''' DROP TABLE IF EXISTS spec_2015_HIV ''')
    conn.execute(''' CREATE TABLE spec_2015_HIV (country text, Coverage_HIV_adult real, Coverage_HIV_adult_need real, Coverage_HIV_adult_received real, Coverage_HIV_children real, Coverage_HIV_children_need real, Coverage_HIV_children_received real,DALY_HIV_adult real, DALY_HIV_children real, rate_HIV real, rate_HIV_adult real, rate_HIV_children real) ''')
    conn.close()
    return

def createTablesSpecRegimen():
    conn = sqlite3.connect('K_ghi.db')
    # Regimen Distribution
    conn.execute(''' DROP TABLE IF EXISTS spec_2015_HIV_Regimen ''')
    conn.execute(''' CREATE TABLE spec_2015_HIV_Regimen (Regimens text, Ndrug real, Adult_prop real, Children_prop real, Adult_eff real, Children_eff real, First_line integer, Second_line integer) ''')
    # conn.execute(''' CREATE TABLE spec_2015_HIV_Regimen (Regimens text, Ndrug real, Adult_prop real, Children_prop real) ''')
    conn.close()
    return
    
def uploadSpecData():
    conn = sqlite3.connect('K_ghi.db')
    url = "ORS_Forecasting_HIV_2015.csv"
    df = pd.read_csv(url, skiprows=1)
    try:
        createTablesSpec()
        is_df_true = df.notnull()
        def clean(value):
            try:
                strVal = str(value)
                if '-' in strVal:
                    resVal = strVal.replace('-', '0')
                elif '%' in strVal:
                    resVal = strVal.replace('%', '')
                elif ',' in strVal:
                    resVal = strVal.replace(',', '')
                else:
                    resVal = strVal
                resVal = float(resVal)
                return resVal
            except:
                return 0
        spec_2015_HIV_data = []
        # print(df.iloc[0, 89])
        for i in range(2, 219):
            country = df.iloc[i, 0]
            # print(country)
            # Treatment Coverage Adult
            if is_df_true.iloc[i, 16] == True:
                Coverage_HIV_adult = clean(df.iloc[i, 16])
            else:
                Coverage_HIV_adult = 0
            if is_df_true.iloc[i, 15] == True:
                Coverage_HIV_adult_need = clean(df.iloc[i, 15])
            else:
                Coverage_HIV_adult_need = 0
            if is_df_true.iloc[i, 14] == True:
                Coverage_HIV_adult_received = clean(df.iloc[i, 14])
            else:
                Coverage_HIV_adult_received = 0
            
            # Treatment Coverage Children
            if is_df_true.iloc[i, 19] == True:
                Coverage_HIV_children = clean(df.iloc[i, 19])
            else:
                Coverage_HIV_children = 0
            if is_df_true.iloc[i, 18] == True:
                Coverage_HIV_children_need = clean(df.iloc[i, 18])
            else:
                Coverage_HIV_children_need = 0
            if is_df_true.iloc[i, 17] == True:
                Coverage_HIV_children_received = clean(df.iloc[i, 17])
            else:
                Coverage_HIV_children_received = 0
            # DALY 
            if is_df_true.iloc[i, 6] == True:
                DALY_HIV_adult = clean(df.iloc[i, 6])
            else:
                DALY_HIV_adult = 0
            if is_df_true.iloc[i, 7] == True:
                DALY_HIV_children = clean(df.iloc[i, 7])
            else:
                DALY_HIV_children = 0
            # print(DALY_HIV_children)
            # Retention rate
            if is_df_true.iloc[i, 8] == True:
                rate_HIV = clean(df.iloc[i, 8])
            else:
                rate_HIV = 0
            if is_df_true.iloc[i, 9] == True:
                rate_HIV_adult = clean(df.iloc[i, 9])
            else:
                rate_HIV_adult = 0
            if is_df_true.iloc[i, 10] == True:
                rate_HIV_children = clean(df.iloc[i, 10])
            else:
                rate_HIV_children = 0
            # print(rate_HIV_children)
            # Regimen Distribution
            
            row = [country, Coverage_HIV_adult, Coverage_HIV_adult_need, Coverage_HIV_adult_received, Coverage_HIV_children, Coverage_HIV_children_need, Coverage_HIV_children_received, DALY_HIV_adult, DALY_HIV_children, rate_HIV, rate_HIV_adult, rate_HIV_children]
            spec_2015_HIV_data.append(row)
            # print(spec_2015_HIV_data[0])
        for k in spec_2015_HIV_data:
            # print(k)
            conn.execute(''' INSERT INTO spec_2015_HIV VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ''', k)
        print("Database operation compelete")
        conn.commit()
        return 'success'
    except Exception as e:
        error = e
        conn.rollback()
        conn.close()
        return error
    return df

def clean(value):
            try:
                strVal = str(value)
                if '-' in strVal:
                    resVal = strVal.replace('-', '0')
                elif '%' in strVal:
                    resVal = strVal.replace('%', '')
                elif ',' in strVal:
                    resVal = strVal.replace(',', '')
                else:
                    resVal = strVal
                resVal = float(resVal)
                return resVal
            except:
                return 0
                
def uploadSpecDataRegimen():
    conn = sqlite3.connect('K_ghi.db')
    url = "ORS_Forecasting_HIV_2015.csv"
    df = pd.read_csv(url, skiprows=1)
    try:
        createTablesSpecRegimen()
        is_df_true = df.notnull()
        
        spec_firstline_2015_HIV_Regimen_data = []
        spec_secondline_2015_HIV_Regimen_data = []
        
        for i in range(2, 16):
            # first line proportion
            firstline_drug_name = df.iloc[i, 44]
            if is_df_true.iloc[i, 49] == True:
                firstline_drug_no = clean(df.iloc[i, 49])
            else:
                firstline_drug_no = 0
            if is_df_true.iloc[i, 45] == True:
                firstline_adult_prop = clean(df.iloc[i, 45])
            else:
                firstline_adult_prop = 0
            if is_df_true.iloc[i, 47] == True:
                firstline_children_prop = clean(df.iloc[i, 47])
            else:
                firstline_children_prop = 0
            if is_df_true.iloc[i, 46] == True:
                firstline_adult_efficacy = clean(df.iloc[i, 46])
            else:
                firstline_adult_efficacy = 0
            if is_df_true.iloc[i, 48] == True:
                firstline_children_efficacy = clean(df.iloc[i, 48])
            else:
                firstline_children_efficacy = 0
            
            firstline_row = [firstline_drug_name, firstline_drug_no, firstline_adult_prop, firstline_children_prop, firstline_adult_efficacy, firstline_children_efficacy, 1, 0]
            spec_firstline_2015_HIV_Regimen_data.append(firstline_row)
            
        for k in spec_firstline_2015_HIV_Regimen_data:
            # print(k)
            conn.execute(''' INSERT INTO spec_2015_HIV_Regimen VALUES (?,?,?,?,?,?,?,?) ''', k)
        print("Database operation compelete")
        conn.commit()


        # Second Line Regimen Data
        for i in range(18, 35):
            # first line proportion
            secondline_drug_name = df.iloc[i, 44]
            if is_df_true.iloc[i, 49] == True:
                secondline_drug_no = clean(df.iloc[i, 49])
            else:
                secondline_drug_no = 0
            if is_df_true.iloc[i, 45] == True:
                secondline_adult_prop = clean(df.iloc[i, 45])
            else:
                secondline_adult_prop = 0
            if is_df_true.iloc[i, 47] == True:
                secondline_children_prop = clean(df.iloc[i, 47])
            else:
                secondline_children_prop = 0
            if is_df_true.iloc[i, 46] == True:
                secondline_adult_efficacy = clean(df.iloc[i, 46])
            else:
                secondline_adult_efficacy = 0
            if is_df_true.iloc[i, 48] == True:
                secondline_children_efficacy = clean(df.iloc[i, 48])
            else:
                secondline_children_efficacy = 0
            
            secondline_row = [secondline_drug_name, secondline_drug_no, secondline_adult_prop, secondline_children_prop, secondline_adult_efficacy, secondline_children_efficacy, 0, 1]
            spec_secondline_2015_HIV_Regimen_data.append(secondline_row)
            
        for k in spec_secondline_2015_HIV_Regimen_data:
            # print(k)
            conn.execute(''' INSERT INTO spec_2015_HIV_Regimen VALUES (?,?,?,?,?,?,?,?) ''', k)
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
uploadSpecDataRegimen()