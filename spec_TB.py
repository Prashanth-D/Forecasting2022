import sqlite3
import pandas as pd
import unicodedata

def createTablesSpec():
    conn = sqlite3.connect('K_ghi.db')
    conn.execute(''' DROP TABLE IF EXISTS spec_2010_TB ''')
    conn.execute(''' DROP TABLE IF EXISTS spec_2013_TB ''')
    conn.execute(''' DROP TABLE IF EXISTS spec_2015_TB_test ''')

    

    conn.execute(''' CREATE TABLE spec_2010_TB (country text, TB_prevalance real, Coverage_TB_HIV_plus real, Coverage_TB_HIV_minus real, Coverage_MDR_TB real, Coverage_XDR_TB real, DALY_TB_HIV_plus real, DALY_TB_HIV_minus real, DALY_MDR_TB real, DALY_XDR_TB real, Coverage_TB_HIV_plus_value real, Coverage_TB_HIV_minus_value real) ''')
    conn.execute(''' CREATE TABLE spec_2013_TB (country text, TB_prevalance real, Coverage_TB_HIV_plus real, Coverage_TB_HIV_minus real, Coverage_MDR_TB real, Coverage_XDR_TB real, DALY_TB_HIV_plus real, DALY_TB_HIV_minus real, DALY_MDR_TB real, DALY_XDR_TB real, Coverage_TB_HIV_plus_value real, Coverage_TB_HIV_minus_value real) ''')
    conn.execute(''' CREATE TABLE spec_2015_TB_test (country text, TB_prevalance real, Coverage_TB_HIV_plus real, Coverage_TB_HIV_minus real, Coverage_MDR_TB real, Coverage_XDR_TB real, DALY_TB_HIV_plus real, DALY_TB_HIV_minus real, DALY_MDR_TB real, DALY_XDR_TB real, Coverage_TB_HIV_plus_value real, Coverage_TB_HIV_minus_value real) ''')

    conn.close()

    return

    
def uploadSpecData():
    conn = sqlite3.connect('K_ghi.db')
    url1 = "ORS_Forecasting_TB_2015.csv"
    url2 = "ORS_Forecasting_TB_2010.csv"
    url3 = "ORS_Forecasting_TB_2013.csv"

    df1 = pd.read_csv(url1, skiprows=1)
    df2 = pd.read_csv(url2, skiprows=1)
    df3 = pd.read_csv(url3, skiprows=1)

    try:
        createTablesSpec()
        is_df1_true = df1.notnull()
        is_df2_true = df2.notnull()
        is_df3_true = df3.notnull()

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

        spec_2010_TB_data = []
        spec_2013_TB_data = []
        spec_2015_TB_data = []

        for i in range(2, 219):
            country2 = df2.iloc[i, 0]
            #country3 = df3.iloc[i, 0]
            #print(country)

            #print(df1.iloc[i,0])
            if is_df2_true.iloc[i, 12] == True:
                TB_prevalance = clean(df2.iloc[i, 12])
            else:
                TB_prevalance = 0
            if is_df2_true.iloc[i, 28] == True:
                Coverage_TB_HIV_plus = clean(df2.iloc[i, 28])
            else:
                Coverage_TB_HIV_plus = 0
            if is_df2_true.iloc[i, 29] == True:
                Coverage_TB_HIV_minus = clean(df2.iloc[i, 29])
            else:
                Coverage_TB_HIV_minus = 0
            
            if is_df2_true.iloc[i, 42] == True:
                Coverage_MDR_TB = clean(df2.iloc[i, 42])
            else:
                Coverage_MDR_TB = 0
            if is_df2_true.iloc[i, 51] == True:
                Coverage_XDR_TB = clean(df2.iloc[i, 51])
            else:
                Coverage_XDR_TB = 0
            if is_df2_true.iloc[i, 26] == True:
                DALY_TB_HIV_plus = clean(df2.iloc[i, 26])
            else:
                DALY_TB_HIV_plus = 0
            # DALY 
            if is_df2_true.iloc[i, 27] == True:
                DALY_TB_HIV_minus = clean(df2.iloc[i, 27])
            else:
                DALY_TB_HIV_minus = 0
            if is_df2_true.iloc[i, 43] == True:
                DALY_MDR_TB = clean(df2.iloc[i, 43])
            else:
                DALY_MDR_TB = 0
            # print(DALY_HIV_children)
            # Retention rate
            if is_df2_true.iloc[i, 52] == True:
                DALY_XDR_TB = clean(df2.iloc[i, 52])
            else:
                DALY_XDR_TB = 0
            # if is_df1_true.iloc[i, 9] == True:
            #     Coverage_TB_HIV_plus_value = clean(df1.iloc[i, 9])
            # else:
            Coverage_TB_HIV_plus_value = 0
            # if is_df1_true.iloc[i, 10] == True:
            #     Coverage_TB_HIV_minus_value = clean(df1.iloc[i, 10])
            # else:
            Coverage_TB_HIV_minus_value = 0
            # # print(rate_HIV_children)
            # # Regimen Distribution
            
            row2 = [country2, TB_prevalance, Coverage_TB_HIV_plus, Coverage_TB_HIV_minus, Coverage_MDR_TB, Coverage_XDR_TB, DALY_TB_HIV_plus, DALY_TB_HIV_minus, DALY_MDR_TB, DALY_XDR_TB, Coverage_TB_HIV_plus_value, Coverage_TB_HIV_minus_value]
            spec_2010_TB_data.append(row2)

        for k in spec_2010_TB_data:
            # print(k)
            conn.execute(''' INSERT INTO spec_2010_TB VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ''', k)

        for i in range(2, 219):
            #country2 = df2.iloc[i, 0]
            country3 = df3.iloc[i, 0]
            #print(country)

            #print(df1.iloc[i,0])
            if is_df3_true.iloc[i, 12] == True:
                TB_prevalance = clean(df3.iloc[i, 12])
            else:
                TB_prevalance = 0
            if is_df3_true.iloc[i, 28] == True:
                Coverage_TB_HIV_plus = clean(df3.iloc[i, 28])
            else:
                Coverage_TB_HIV_plus = 0
            if is_df3_true.iloc[i, 29] == True:
                Coverage_TB_HIV_minus = clean(df3.iloc[i, 29])
            else:
                Coverage_TB_HIV_minus = 0
            
            if is_df3_true.iloc[i, 42] == True:
                Coverage_MDR_TB = clean(df3.iloc[i, 42])
            else:
                Coverage_MDR_TB = 0
            if is_df3_true.iloc[i, 51] == True:
                Coverage_XDR_TB = clean(df3.iloc[i, 51])
            else:
                Coverage_XDR_TB = 0
            if is_df3_true.iloc[i, 26] == True:
                DALY_TB_HIV_plus = clean(df3.iloc[i, 26])
            else:
                DALY_TB_HIV_plus = 0
            # DALY 
            if is_df3_true.iloc[i, 27] == True:
                DALY_TB_HIV_minus = clean(df3.iloc[i, 27])
            else:
                DALY_TB_HIV_minus = 0
            if is_df3_true.iloc[i, 43] == True:
                DALY_MDR_TB = clean(df3.iloc[i, 43])
            else:
                DALY_MDR_TB = 0
            # print(DALY_HIV_children)
            # Retention rate
            if is_df3_true.iloc[i, 52] == True:
                DALY_XDR_TB = clean(df3.iloc[i, 52])
            else:
                DALY_XDR_TB = 0
            # if is_df1_true.iloc[i, 9] == True:
            #     Coverage_TB_HIV_plus_value = clean(df1.iloc[i, 9])
            # else:
            Coverage_TB_HIV_plus_value = 0
            # if is_df1_true.iloc[i, 10] == True:
            #     Coverage_TB_HIV_minus_value = clean(df1.iloc[i, 10])
            # else:
            Coverage_TB_HIV_minus_value = 0
            # # print(rate_HIV_children)
            # # Regimen Distribution
            
            row3 = [country3, TB_prevalance, Coverage_TB_HIV_plus, Coverage_TB_HIV_minus, Coverage_MDR_TB, Coverage_XDR_TB, DALY_TB_HIV_plus, DALY_TB_HIV_minus, DALY_MDR_TB, DALY_XDR_TB, Coverage_TB_HIV_plus_value, Coverage_TB_HIV_minus_value]
            spec_2013_TB_data.append(row3)

        for k in spec_2013_TB_data:
            # print(k)
            conn.execute(''' INSERT INTO spec_2013_TB VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ''', k)

        for i in range(2, 219):
            country1 = df1.iloc[i, 0]
            #country3 = df3.iloc[i, 0]
            # print(country)

            #print(df1.iloc[i,0])
            if is_df1_true.iloc[i, 12] == True:
                TB_prevalance = clean(df1.iloc[i, 12])
            else:
                TB_prevalance = 0
            if is_df1_true.iloc[i, 28] == True:
                Coverage_TB_HIV_plus = clean(df1.iloc[i, 28])
            else:
                Coverage_TB_HIV_plus = 0
            if is_df1_true.iloc[i, 29] == True:
                Coverage_TB_HIV_minus = clean(df1.iloc[i, 29])
            else:
                Coverage_TB_HIV_minus = 0
            
            if is_df1_true.iloc[i, 42] == True:
                Coverage_MDR_TB = clean(df1.iloc[i, 42])
            else:
                Coverage_MDR_TB = 0
            if is_df1_true.iloc[i, 51] == True:
                Coverage_XDR_TB = clean(df1.iloc[i, 51])
            else:
                Coverage_XDR_TB = 0
            if is_df1_true.iloc[i, 26] == True:
                DALY_TB_HIV_plus = clean(df1.iloc[i, 26])
            else:
                DALY_TB_HIV_plus = 0
            # DALY 
            if is_df1_true.iloc[i, 27] == True:
                DALY_TB_HIV_minus = clean(df1.iloc[i, 27])
            else:
                DALY_TB_HIV_minus = 0
            if is_df1_true.iloc[i, 43] == True:
                DALY_MDR_TB = clean(df1.iloc[i, 43])
            else:
                DALY_MDR_TB = 0
            # print(DALY_HIV_children)
            # Retention rate
            if is_df1_true.iloc[i, 52] == True:
                DALY_XDR_TB = clean(df1.iloc[i, 52])
            else:
                DALY_XDR_TB = 0
            # if is_df1_true.iloc[i, 9] == True:
            #     Coverage_TB_HIV_plus_value = clean(df1.iloc[i, 9])
            # else:
            Coverage_TB_HIV_plus_value = 0
            # if is_df1_true.iloc[i, 10] == True:
            #     Coverage_TB_HIV_minus_value = clean(df1.iloc[i, 10])
            # else:
            Coverage_TB_HIV_minus_value = 0
            # # print(rate_HIV_children)
            # # Regimen Distribution
            
            row1 = [country1, TB_prevalance, Coverage_TB_HIV_plus, Coverage_TB_HIV_minus, Coverage_MDR_TB, Coverage_XDR_TB, DALY_TB_HIV_plus, DALY_TB_HIV_minus, DALY_MDR_TB, DALY_XDR_TB, Coverage_TB_HIV_plus_value, Coverage_TB_HIV_minus_value]
            spec_2015_TB_data.append(row1)
            # print(spec_2015_HIV_data[0])
        for k in spec_2015_TB_data:
            # print(k)
            conn.execute(''' INSERT INTO spec_2015_TB_test VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ''', k)
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
                


uploadSpecData()
