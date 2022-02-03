import sqlite3
import pandas as pd
import unicodedata

def createTablesSpec():
    conn = sqlite3.connect('K_ghi.db')
    conn.execute(''' DROP TABLE IF EXISTS spec_2010_HIV ''')
    conn.execute(''' CREATE TABLE spec_2010_HIV (country text, Coverage_HIV_adult real, Coverage_HIV_adult_need real, Coverage_HIV_adult_received real, Coverage_HIV_children real, Coverage_HIV_children_need real, Coverage_HIV_children_received real,DALY_HIV_adult real, DALY_HIV_children real, rate_HIV real, rate_HIV_adult real, rate_HIV_children real, grp text) ''')
    conn.close()
    return

def createTablesSpecRegimen():
    conn = sqlite3.connect('K_ghi.db')
    # Regimen Distribution
    conn.execute(''' DROP TABLE IF EXISTS spec_2010_HIV_Regimen ''')
    conn.execute(''' CREATE TABLE spec_2010_HIV_Regimen (Regimens text, Ndrug real, Adult_prop real, Children_prop real, Adult_eff real, Children_eff real, First_line integer, Second_line integer, grp text) ''')
    conn.close()
    return

def uploadSpecData():
    conn = sqlite3.connect('K_ghi.db')
    url = "ORS_Forecasting_HIV_2010.csv"
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
        spec_2010_HIV_data = []
        # print(df.iloc[0, 89])
        for i in range(2, 219):
            country = df.iloc[i, 0]
            grp = df.iloc[i,4]
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
            
            row = [country, Coverage_HIV_adult, Coverage_HIV_adult_need, Coverage_HIV_adult_received, Coverage_HIV_children, Coverage_HIV_children_need, Coverage_HIV_children_received, DALY_HIV_adult, DALY_HIV_children, rate_HIV, rate_HIV_adult, rate_HIV_children, grp]
            spec_2010_HIV_data.append(row)
            # print(spec_2010_HIV_data[0])
        for k in spec_2010_HIV_data:
            
            conn.execute(''' INSERT INTO spec_2010_HIV VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) ''', k)
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
    url = "ORS_Forecasting_HIV_2010.csv"
    df = pd.read_csv(url, skiprows=1)
    try:
        createTablesSpecRegimen()
        is_df_true = df.notnull()

        spec_firstline_2010_HIV_Regimen_data = []
        spec_secondline_2010_HIV_Regimen_data = []
        
        #Group A adult first
        for i in range(4, 13):
            firstline_drug_name = df.iloc[i, 45]
            if(firstline_drug_name == ""):
                break
            firstline_drug_no = firstline_drug_name.count("+")+1
            if is_df_true.iloc[i, 46] == True:
                firstline_adult_prop = clean(df.iloc[i, 46])/100
            else:
                firstline_adult_prop = 0
            if is_df_true.iloc[i, 47] == True:
                firstline_adult_efficacy = clean(df.iloc[i, 47])/100
            else:
                firstline_adult_efficacy = 0
            
            row = [firstline_drug_name, firstline_drug_no, firstline_adult_prop, firstline_adult_efficacy, 1, 0, 1, 0,'A']
            spec_firstline_2010_HIV_Regimen_data.append(row)
            
        
        #Group A child first
        for i in range(28, 37):
            firstline_drug_name = df.iloc[i, 45]
            if(firstline_drug_name == ""):
                break
            firstline_drug_no = firstline_drug_name.count("+")+1
            if is_df_true.iloc[i, 46] == True:
                firstline_child_prop = clean(df.iloc[i, 46])/100
            else:
                firstline_child_prop = 0
            if is_df_true.iloc[i, 47] == True:
                firstline_child_efficacy = clean(df.iloc[i, 47])/100
            else:
                firstline_child_efficacy = 0
            
            row = [firstline_drug_name, firstline_drug_no, firstline_child_prop, firstline_child_efficacy, 1, 0, 0, 1,'A']
            spec_firstline_2010_HIV_Regimen_data.append(row)

        #Group A adult second
        for i in range(15, 25):
            firstline_drug_name = df.iloc[i, 45]
            if(firstline_drug_name == ""):
                break
            firstline_drug_no = firstline_drug_name.count("+")+1
            if is_df_true.iloc[i, 46] == True:
                firstline_adult_prop = clean(df.iloc[i, 46])/100
            else:
                firstline_adult_prop = 0
            if is_df_true.iloc[i, 47] == True:
                firstline_adult_efficacy = clean(df.iloc[i, 47])/100
            else:
                firstline_adult_efficacy = 0
            
            row = [firstline_drug_name, firstline_drug_no, firstline_adult_prop, firstline_adult_efficacy, 0, 1, 1, 0,'A']
            spec_firstline_2010_HIV_Regimen_data.append(row)

        #Group A child second
        for i in range(39, 49):
            firstline_drug_name = df.iloc[i, 45]
            if(firstline_drug_name == ""):
                break
            firstline_drug_no = firstline_drug_name.count("+")+1
            if is_df_true.iloc[i, 46] == True:
                firstline_chil_prop = clean(df.iloc[i, 46])/100
            else:
                firstline_child_prop = 0
            if is_df_true.iloc[i, 47] == True:
                firstline_child_efficacy = clean(df.iloc[i, 47])/100
            else:
                firstline_child_efficacy = 0
            
            row = [firstline_drug_name, firstline_drug_no, firstline_child_prop, firstline_child_efficacy, 0, 1, 0, 1,'A']
            spec_firstline_2010_HIV_Regimen_data.append(row)

        #Group B adult first
        for i in range(4, 13):
            firstline_drug_name = df.iloc[i, 48]
            if(firstline_drug_name == ""):
                break
            firstline_drug_no = firstline_drug_name.count("+")+1
            if is_df_true.iloc[i, 49] == True:
                firstline_adult_prop = clean(df.iloc[i, 49])/100
            else:
                firstline_adult_prop = 0
            if is_df_true.iloc[i, 50] == True:
                firstline_adult_efficacy = clean(df.iloc[i, 50])/100
            else:
                firstline_adult_efficacy = 0
            
            row = [firstline_drug_name, firstline_drug_no, firstline_adult_prop, firstline_adult_efficacy, 1, 0, 1, 0,'B']
            spec_firstline_2010_HIV_Regimen_data.append(row)

        #Group B child first
        for i in range(28, 35):
            firstline_drug_name = df.iloc[i, 48]
            if(firstline_drug_name == ""):
                break
            firstline_drug_no = firstline_drug_name.count("+")+1
            if is_df_true.iloc[i, 49] == True:
                firstline_adult_prop = clean(df.iloc[i, 49])/100
            else:
                firstline_adult_prop = 0
            if is_df_true.iloc[i, 50] == True:
                firstline_adult_efficacy = clean(df.iloc[i, 50])/100
            else:
                firstline_adult_efficacy = 0
            
            row = [firstline_drug_name, firstline_drug_no, firstline_adult_prop, firstline_adult_efficacy, 1, 0, 0, 1,'B']
            spec_firstline_2010_HIV_Regimen_data.append(row)
        
        #Group B adult second
        for i in range(15, 25):
            firstline_drug_name = df.iloc[i, 48]
            if(firstline_drug_name == ""):
                break
            firstline_drug_no = firstline_drug_name.count("+")+1
            if is_df_true.iloc[i, 49] == True:
                firstline_adult_prop = clean(df.iloc[i, 49])/100
            else:
                firstline_adult_prop = 0
            if is_df_true.iloc[i, 50] == True:
                firstline_adult_efficacy = clean(df.iloc[i,50])/100
            else:
                firstline_adult_efficacy = 0
            
            row = [firstline_drug_name, firstline_drug_no, firstline_adult_prop, firstline_adult_efficacy, 0, 1, 1, 0,'B']
            spec_firstline_2010_HIV_Regimen_data.append(row)

        #Group B child second
        for i in range(39, 46):
            firstline_drug_name = df.iloc[i, 48]
            if(firstline_drug_name == ""):
                break
            firstline_drug_no = firstline_drug_name.count("+")+1
            if is_df_true.iloc[i, 49] == True:
                firstline_adult_prop = clean(df.iloc[i, 49])/100
            else:
                firstline_adult_prop = 0
            if is_df_true.iloc[i, 50] == True:
                firstline_adult_efficacy = clean(df.iloc[i, 50])/100
            else:
                firstline_adult_efficacy = 0
            
            row = [firstline_drug_name, firstline_drug_no, firstline_adult_prop, firstline_adult_efficacy, 0, 1, 0, 1,'B']
            spec_firstline_2010_HIV_Regimen_data.append(row)
            
            
        for k in spec_firstline_2010_HIV_Regimen_data:
            # print(k)
            conn.execute(''' INSERT INTO spec_2010_HIV_Regimen VALUES (?,?,?,?,?,?,?,?,?) ''', k)
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