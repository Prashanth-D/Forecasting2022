import sqlite3
import pandas as pd
import unicodedata

def createTablesSpec():
    conn = sqlite3.connect('K_ghi.db')
    conn.execute(''' DROP TABLE IF EXISTS spec_2015_Malaria_test ''')
    conn.execute(''' DROP TABLE IF EXISTS spec_2013_Malaria ''')
    conn.execute(''' DROP TABLE IF EXISTS spec_2010_Malaria ''')

    

    conn.execute(''' CREATE TABLE spec_2015_Malaria_test
	(country text, Malaria_prevalance real, Coverage_Malaria_PFalc real, Coverage_Malaria_PVivax real, DALY_Malaria_Prop_PFalc real, DALY_Malaria_Prop_PVivax real,DALY_Malaria real,Eff_PFalc_AL real, Eff_PFalc_AL_PQ real,Eff_PFalc_AM real,Eff_PFalc_ART_NQ real,Eff_PFalc_ART_PPQ real,Eff_PFalc_AS_AQ real,Eff_PFalc_AS_MQ real,Eff_PFalc_AS_MQ_PQ real,Eff_PFalc_AS_SP real,Eff_PFalc_AS_SP_PQ real,Eff_PFalc_AT_PG real,Eff_PFalc_CQ_PQ real,Eff_PFalc_DHA_PPQ real,Eff_PFalc_DHA_PPQ_PQ real,Eff_PFalc_PQ real,Eff_PFalc_QN real,Eff_PFalc_QN_CL real,Eff_PFalc_QN_D real, Eff_PVivax_CQ_PQ real,Eff_PVivax_CQ real,Eff_PVivax_DHA_PPQ real,Eff_PVivax_AL real,Eff_PVivax_AS_AQ_PQ real,Eff_PVivax_AL_PQ real ) ''')
    conn.execute(''' CREATE TABLE spec_2013_Malaria
	(country text, Malaria_prevalance real, Coverage_Malaria_PFalc real, Coverage_Malaria_PVivax real, DALY_Malaria_Prop_PFalc real, DALY_Malaria_Prop_PVivax real,DALY_Malaria real,Eff_PFalc_AL real, Eff_PFalc_AL_PQ real,Eff_PFalc_AM real,Eff_PFalc_ART_NQ real,Eff_PFalc_ART_PPQ real,Eff_PFalc_AS_AQ real,Eff_PFalc_AS_MQ real,Eff_PFalc_AS_MQ_PQ real,Eff_PFalc_AS_SP real,Eff_PFalc_AS_SP_PQ real,Eff_PFalc_AT_PG real,Eff_PFalc_CQ_PQ real,Eff_PFalc_DHA_PPQ real,Eff_PFalc_DHA_PPQ_PQ real,Eff_PFalc_PQ real,Eff_PFalc_QN real,Eff_PFalc_QN_CL real,Eff_PFalc_QN_D real, Eff_PVivax_CQ_PQ real,Eff_PVivax_CQ real,Eff_PVivax_DHA_PPQ real,Eff_PVivax_AL real,Eff_PVivax_AS_AQ_PQ real,Eff_PVivax_AL_PQ real ) ''')
    conn.execute(''' CREATE TABLE spec_2010_Malaria
	(country text, Malaria_prevalance real, Coverage_Malaria_PFalc real, Coverage_Malaria_PVivax real, DALY_Malaria_Prop_PFalc real, DALY_Malaria_Prop_PVivax real,DALY_Malaria real,Eff_PFalc_AL real, Eff_PFalc_AL_PQ real,Eff_PFalc_AM real,Eff_PFalc_ART_NQ real,Eff_PFalc_ART_PPQ real,Eff_PFalc_AS_AQ real,Eff_PFalc_AS_MQ real,Eff_PFalc_AS_MQ_PQ real,Eff_PFalc_AS_SP real,Eff_PFalc_AS_SP_PQ real,Eff_PFalc_AT_PG real,Eff_PFalc_CQ_PQ real,Eff_PFalc_DHA_PPQ real,Eff_PFalc_DHA_PPQ_PQ real,Eff_PFalc_PQ real,Eff_PFalc_QN real,Eff_PFalc_QN_CL real,Eff_PFalc_QN_D real, Eff_PVivax_CQ_PQ real,Eff_PVivax_CQ real,Eff_PVivax_DHA_PPQ real,Eff_PVivax_AL real,Eff_PVivax_AS_AQ_PQ real,Eff_PVivax_AL_PQ real ) ''')

    conn.close()

    return
    
def uploadSpecData():
    conn = sqlite3.connect('K_ghi.db')
    url1 = "ORS_Forecasting_Malaria_2015.csv"
    url2 = "ORS_Forecasting_Malaria_2013.csv"
    url3 = "ORS_Forecasting_Malaria_2010.csv"

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
        spec_2015_Malaria_data = []
        spec_2013_Malaria_data = []
        spec_2010_Malaria_data = []

        for i in range(2, 219):
            
            country1 = df1.iloc[i+1, 0]
            # print(df.iloc[i + 1, 7])
            if is_df1_true.iloc[i+1, 7] == True:
                malaria_prevalance = clean(df1.iloc[i+1, 7])
            else:
                malaria_prevalance = 0
            # print (malaria_prevalance)
            if is_df1_true.iloc[i+1, 4] == True:
                Coverage_Malaria_PFalc = clean(df1.iloc[i+1, 4])
            else:
                Coverage_Malaria_PFalc = 0
            if is_df1_true.iloc[i+1, 89] == True:
                Coverage_Malaria_PVivax = clean(df1.iloc[i+1, 89])
            else:
                Coverage_Malaria_PVivax = 0
            # DALY Proportion
            if is_df1_true.iloc[i+1, 8] == True:
                DALY_Malaria_Prop_PFalc = clean(df1.iloc[i+1, 8])
            else:
                DALY_Malaria_Prop_PFalc = 0
            if is_df1_true.iloc[i+1, 86] == True:
                DALY_Malaria_Prop_PVivax = clean(df1.iloc[i+1, 86])
            else:
                DALY_Malaria = 0
            # if is_df_true.iloc[i+1, 117] == True:
            if is_df1_true.iloc[i + 1, 6] == True:
                DALY_Malaria = clean(df1.iloc[i+1, 6])
            else:
                DALY_Malaria = 0
            print(country1, DALY_Malaria)
            # Efficacy PFalc
            if is_df1_true.iloc[i+1, 48] == True:
                Eff_PFalc_AL = clean(df1.iloc[i+1, 48])
            else:
                Eff_PFalc_AL = 0
            
            if is_df1_true.iloc[i+1, 49] == True:
                Eff_PFalc_AL_PQ = clean(df1.iloc[i+1, 49])
            else:
                Eff_PFalc_AL_PQ = 0
            
            if is_df1_true.iloc[i+1, 50] == True:
                Eff_PFalc_AM = clean(df1.iloc[i+1, 50])
            else:
                Eff_PFalc_AM = 0
            
            if is_df1_true.iloc[i+1, 51] == True:
                Eff_PFalc_ART_NQ = clean(df1.iloc[i+1, 51])
            else:
                Eff_PFalc_ART_NQ = 0
            
            if is_df1_true.iloc[i+1, 52] == True:
                Eff_PFalc_ART_PPQ = clean(df1.iloc[i+1, 52])
            else:
                Eff_PFalc_ART_PPQ = 0

            if is_df1_true.iloc[i+1, 53] == True:
                Eff_PFalc_AS_AQ = clean(df1.iloc[i+1, 53])
            else:
                Eff_PFalc_AS_AQ = 0

            if is_df1_true.iloc[i+1, 54] == True:
                Eff_PFalc_AS_MQ = clean(df1.iloc[i+1, 54])
            else:
                Eff_PFalc_AS_MQ = 0
            
            if is_df1_true.iloc[i+1, 55] == True:
                Eff_PFalc_AS_MQ_PQ = clean(df1.iloc[i+1, 55])
            else:
                Eff_PFalc_AS_MQ_PQ = 0
            
            if is_df1_true.iloc[i+1, 56] == True:
                Eff_PFalc_AS_SP = clean(df1.iloc[i+1, 56])
            else:
                Eff_PFalc_AS_SP = 0
            
            if is_df1_true.iloc[i+1, 57] == True:
                Eff_PFalc_AS_SP_PQ = clean(df1.iloc[i+1, 57])
            else:
                Eff_PFalc_AS_SP_PQ = 0
            
            if is_df1_true.iloc[i+1, 58] == True:
                Eff_PFalc_AT_PG = clean(df1.iloc[i+1, 58])
            else:
                Eff_PFalc_AT_PG = 0

            if is_df1_true.iloc[i+1, 59] == True:
                Eff_PFalc_CQ_PQ = clean(df1.iloc[i+1, 59])
            else:
                Eff_PFalc_CQ_PQ = 0

            if is_df1_true.iloc[i+1, 60] == True:
                Eff_PFalc_DHA_PPQ = clean(df1.iloc[i+1, 60])
            else:
                Eff_PFalc_DHA_PPQ = 0
            
            if is_df1_true.iloc[i+1, 61] == True:
                Eff_PFalc_DHA_PPQ_PQ = clean(df1.iloc[i+1, 61])
            else:
                Eff_PFalc_DHA_PPQ_PQ = 0

            if is_df1_true.iloc[i+1, 62] == True:
                Eff_PFalc_PQ = clean(df1.iloc[i+1, 62])
            else:
                Eff_PFalc_PQ = 0

            if is_df1_true.iloc[i+1, 63] == True:
                Eff_PFalc_QN = clean(df1.iloc[i+1, 63])
            else:
                Eff_PFalc_QN = 0
            
            if is_df1_true.iloc[i+1, 64] == True:
                Eff_PFalc_QN_CL = clean(df1.iloc[i+1, 64])
            else:
                Eff_PFalc_QN_CL = 0
            
            if is_df1_true.iloc[i+1, 65] == True:
                Eff_PFalc_QN_D = clean(df1.iloc[i+1, 65])
            else:
                Eff_PFalc_QN_D = 0

            # Efficacy PVivax
            if is_df1_true.iloc[i+1, 96] == True:
                Eff_PVivax_CQ_PQ = clean(df1.iloc[i+1, 96])
            else:
                Eff_PVivax_CQ_PQ = 0
            
            if is_df1_true.iloc[i+1, 97] == True:
                Eff_PVivax_CQ = clean(df1.iloc[i+1, 97])
            else:
                Eff_PVivax_CQ = 0
            
            if is_df1_true.iloc[i+1, 98] == True:
                Eff_PVivax_DHA_PPQ = clean(df1.iloc[i+1, 98])
            else:
                Eff_PVivax_DHA_PPQ = 0

            if is_df1_true.iloc[i+1, 99] == True:
                Eff_PVivax_AL = clean(df1.iloc[i+1, 99])
            else:
                Eff_PVivax_AL = 0

            if is_df1_true.iloc[i+1, 100] == True:
                Eff_PVivax_AS_AQ_PQ = clean(df1.iloc[i+1, 100])
            else:
                Eff_PVivax_AS_AQ_PQ = 0

            if is_df1_true.iloc[i+1, 101] == True:
                Eff_PVivax_AL_PQ = clean(df1.iloc[i+1, 101])
            else:
                Eff_PVivax_AL_PQ = 0
            
            row1= [country1, malaria_prevalance, Coverage_Malaria_PFalc, Coverage_Malaria_PVivax, DALY_Malaria_Prop_PFalc, DALY_Malaria_Prop_PVivax,DALY_Malaria,Eff_PFalc_AL,Eff_PFalc_AL_PQ,Eff_PFalc_AM,Eff_PFalc_ART_NQ,Eff_PFalc_ART_PPQ,Eff_PFalc_AS_AQ,Eff_PFalc_AS_MQ,Eff_PFalc_AS_MQ_PQ,Eff_PFalc_AS_SP,Eff_PFalc_AS_SP_PQ,Eff_PFalc_AT_PG,Eff_PFalc_CQ_PQ,Eff_PFalc_DHA_PPQ,Eff_PFalc_DHA_PPQ_PQ,Eff_PFalc_PQ,Eff_PFalc_QN,Eff_PFalc_QN_CL,Eff_PFalc_QN_D,Eff_PVivax_CQ_PQ,Eff_PVivax_CQ,Eff_PVivax_DHA_PPQ,Eff_PVivax_AL,Eff_PVivax_AS_AQ_PQ,Eff_PVivax_AL_PQ]
            # row = [country]
            spec_2015_Malaria_data.append(row1)

        for k in spec_2015_Malaria_data:
            # print(k)
            conn.execute(''' INSERT INTO spec_2015_Malaria_test VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', k)
        
        
        for i in range(2, 219):
            
            country2 = df1.iloc[i+1, 0]
            # print(df.iloc[i + 1, 7])
            if is_df2_true.iloc[i+1, 7] == True:
                malaria_prevalance = clean(df2.iloc[i+1, 7])
            else:
                malaria_prevalance = 0
            # print (malaria_prevalance)
            if is_df2_true.iloc[i+1, 4] == True:
                Coverage_Malaria_PFalc = clean(df2.iloc[i+1, 4])
            else:
                Coverage_Malaria_PFalc = 0
            if is_df2_true.iloc[i+1, 89] == True:
                Coverage_Malaria_PVivax = clean(df2.iloc[i+1, 89])
            else:
                Coverage_Malaria_PVivax = 0
            # DALY Proportion
            if is_df2_true.iloc[i+1, 8] == True:
                DALY_Malaria_Prop_PFalc = clean(df2.iloc[i+1, 8])
            else:
                DALY_Malaria_Prop_PFalc = 0
            if is_df2_true.iloc[i+1, 86] == True:
                DALY_Malaria_Prop_PVivax = clean(df2.iloc[i+1, 86])
            else:
                DALY_Malaria = 0
            # if is_df_true.iloc[i+1, 117] == True:
            if is_df2_true.iloc[i + 1, 6] == True:
                DALY_Malaria = clean(df2.iloc[i+1, 6])
            else:
                DALY_Malaria = 0
            print(country2, DALY_Malaria)
            # Efficacy PFalc
            if is_df2_true.iloc[i+1, 48] == True:
                Eff_PFalc_AL = clean(df2.iloc[i+1, 48])
            else:
                Eff_PFalc_AL = 0
            
            if is_df2_true.iloc[i+1, 49] == True:
                Eff_PFalc_AL_PQ = clean(df2.iloc[i+1, 49])
            else:
                Eff_PFalc_AL_PQ = 0
            
            if is_df2_true.iloc[i+1, 50] == True:
                Eff_PFalc_AM = clean(df2.iloc[i+1, 50])
            else:
                Eff_PFalc_AM = 0
            
            if is_df2_true.iloc[i+1, 51] == True:
                Eff_PFalc_ART_NQ = clean(df2.iloc[i+1, 51])
            else:
                Eff_PFalc_ART_NQ = 0
            
            if is_df2_true.iloc[i+1, 52] == True:
                Eff_PFalc_ART_PPQ = clean(df2.iloc[i+1, 52])
            else:
                Eff_PFalc_ART_PPQ = 0

            if is_df2_true.iloc[i+1, 53] == True:
                Eff_PFalc_AS_AQ = clean(df2.iloc[i+1, 53])
            else:
                Eff_PFalc_AS_AQ = 0

            if is_df2_true.iloc[i+1, 54] == True:
                Eff_PFalc_AS_MQ = clean(df2.iloc[i+1, 54])
            else:
                Eff_PFalc_AS_MQ = 0
            
            if is_df2_true.iloc[i+1, 55] == True:
                Eff_PFalc_AS_MQ_PQ = clean(df2.iloc[i+1, 55])
            else:
                Eff_PFalc_AS_MQ_PQ = 0
            
            if is_df2_true.iloc[i+1, 56] == True:
                Eff_PFalc_AS_SP = clean(df2.iloc[i+1, 56])
            else:
                Eff_PFalc_AS_SP = 0
            
            if is_df2_true.iloc[i+1, 57] == True:
                Eff_PFalc_AS_SP_PQ = clean(df2.iloc[i+1, 57])
            else:
                Eff_PFalc_AS_SP_PQ = 0
            
            if is_df2_true.iloc[i+1, 58] == True:
                Eff_PFalc_AT_PG = clean(df2.iloc[i+1, 58])
            else:
                Eff_PFalc_AT_PG = 0

            if is_df2_true.iloc[i+1, 59] == True:
                Eff_PFalc_CQ_PQ = clean(df2.iloc[i+1, 59])
            else:
                Eff_PFalc_CQ_PQ = 0

            if is_df2_true.iloc[i+1, 60] == True:
                Eff_PFalc_DHA_PPQ = clean(df2.iloc[i+1, 60])
            else:
                Eff_PFalc_DHA_PPQ = 0
            
            if is_df2_true.iloc[i+1, 61] == True:
                Eff_PFalc_DHA_PPQ_PQ = clean(df2.iloc[i+1, 61])
            else:
                Eff_PFalc_DHA_PPQ_PQ = 0

            if is_df2_true.iloc[i+1, 62] == True:
                Eff_PFalc_PQ = clean(df2.iloc[i+1, 62])
            else:
                Eff_PFalc_PQ = 0

            if is_df2_true.iloc[i+1, 63] == True:
                Eff_PFalc_QN = clean(df2.iloc[i+1, 63])
            else:
                Eff_PFalc_QN = 0
            
            if is_df2_true.iloc[i+1, 64] == True:
                Eff_PFalc_QN_CL = clean(df2.iloc[i+1, 64])
            else:
                Eff_PFalc_QN_CL = 0
            
            if is_df2_true.iloc[i+1, 65] == True:
                Eff_PFalc_QN_D = clean(df2.iloc[i+1, 65])
            else:
                Eff_PFalc_QN_D = 0

            # Efficacy PVivax
            if is_df2_true.iloc[i+1, 96] == True:
                Eff_PVivax_CQ_PQ = clean(df2.iloc[i+1, 96])
            else:
                Eff_PVivax_CQ_PQ = 0
            
            if is_df2_true.iloc[i+1, 97] == True:
                Eff_PVivax_CQ = clean(df2.iloc[i+1, 97])
            else:
                Eff_PVivax_CQ = 0
            
            if is_df2_true.iloc[i+1, 98] == True:
                Eff_PVivax_DHA_PPQ = clean(df2.iloc[i+1, 98])
            else:
                Eff_PVivax_DHA_PPQ = 0

            if is_df2_true.iloc[i+1, 99] == True:
                Eff_PVivax_AL = clean(df2.iloc[i+1, 99])
            else:
                Eff_PVivax_AL = 0

            if is_df2_true.iloc[i+1, 100] == True:
                Eff_PVivax_AS_AQ_PQ = clean(df2.iloc[i+1, 100])
            else:
                Eff_PVivax_AS_AQ_PQ = 0

            if is_df2_true.iloc[i+1, 101] == True:
                Eff_PVivax_AL_PQ = clean(df2.iloc[i+1, 101])
            else:
                Eff_PVivax_AL_PQ = 0
            
            row2= [country2, malaria_prevalance, Coverage_Malaria_PFalc, Coverage_Malaria_PVivax, DALY_Malaria_Prop_PFalc, DALY_Malaria_Prop_PVivax,DALY_Malaria,Eff_PFalc_AL,Eff_PFalc_AL_PQ,Eff_PFalc_AM,Eff_PFalc_ART_NQ,Eff_PFalc_ART_PPQ,Eff_PFalc_AS_AQ,Eff_PFalc_AS_MQ,Eff_PFalc_AS_MQ_PQ,Eff_PFalc_AS_SP,Eff_PFalc_AS_SP_PQ,Eff_PFalc_AT_PG,Eff_PFalc_CQ_PQ,Eff_PFalc_DHA_PPQ,Eff_PFalc_DHA_PPQ_PQ,Eff_PFalc_PQ,Eff_PFalc_QN,Eff_PFalc_QN_CL,Eff_PFalc_QN_D,Eff_PVivax_CQ_PQ,Eff_PVivax_CQ,Eff_PVivax_DHA_PPQ,Eff_PVivax_AL,Eff_PVivax_AS_AQ_PQ,Eff_PVivax_AL_PQ]
            # row = [country]
            spec_2013_Malaria_data.append(row2)

        for k in spec_2013_Malaria_data:
            # print(k)
            conn.execute(''' INSERT INTO spec_2013_Malaria VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', k)
        

        for i in range(2, 219):
            
            country3 = df3.iloc[i+1, 0]
            # print(df.iloc[i + 1, 7])
            if is_df3_true.iloc[i+1, 7] == True:
                malaria_prevalance = clean(df3.iloc[i+1, 7])
            else:
                malaria_prevalance = 0
            # print (malaria_prevalance)
            if is_df3_true.iloc[i+1, 4] == True:
                Coverage_Malaria_PFalc = clean(df3.iloc[i+1, 4])
            else:
                Coverage_Malaria_PFalc = 0
            if is_df3_true.iloc[i+1, 89] == True:
                Coverage_Malaria_PVivax = clean(df3.iloc[i+1, 89])
            else:
                Coverage_Malaria_PVivax = 0
            # DALY Proportion
            if is_df3_true.iloc[i+1, 8] == True:
                DALY_Malaria_Prop_PFalc = clean(df3.iloc[i+1, 8])
            else:
                DALY_Malaria_Prop_PFalc = 0
            if is_df3_true.iloc[i+1, 86] == True:
                DALY_Malaria_Prop_PVivax = clean(df3.iloc[i+1, 86])
            else:
                DALY_Malaria = 0
            # if is_df_true.iloc[i+1, 117] == True:
            if is_df3_true.iloc[i + 1, 6] == True:
                DALY_Malaria = clean(df3.iloc[i+1, 6])
            else:
                DALY_Malaria = 0
            print(country3, DALY_Malaria)
            # Efficacy PFalc
            if is_df3_true.iloc[i+1, 48] == True:
                Eff_PFalc_AL = clean(df3.iloc[i+1, 48])
            else:
                Eff_PFalc_AL = 0
            
            if is_df3_true.iloc[i+1, 49] == True:
                Eff_PFalc_AL_PQ = clean(df3.iloc[i+1, 49])
            else:
                Eff_PFalc_AL_PQ = 0
            
            if is_df3_true.iloc[i+1, 50] == True:
                Eff_PFalc_AM = clean(df3.iloc[i+1, 50])
            else:
                Eff_PFalc_AM = 0
            
            if is_df3_true.iloc[i+1, 51] == True:
                Eff_PFalc_ART_NQ = clean(df3.iloc[i+1, 51])
            else:
                Eff_PFalc_ART_NQ = 0
            
            if is_df3_true.iloc[i+1, 52] == True:
                Eff_PFalc_ART_PPQ = clean(df3.iloc[i+1, 52])
            else:
                Eff_PFalc_ART_PPQ = 0

            if is_df3_true.iloc[i+1, 53] == True:
                Eff_PFalc_AS_AQ = clean(df3.iloc[i+1, 53])
            else:
                Eff_PFalc_AS_AQ = 0

            if is_df3_true.iloc[i+1, 54] == True:
                Eff_PFalc_AS_MQ = clean(df3.iloc[i+1, 54])
            else:
                Eff_PFalc_AS_MQ = 0
            
            if is_df3_true.iloc[i+1, 55] == True:
                Eff_PFalc_AS_MQ_PQ = clean(df3.iloc[i+1, 55])
            else:
                Eff_PFalc_AS_MQ_PQ = 0
            
            if is_df3_true.iloc[i+1, 56] == True:
                Eff_PFalc_AS_SP = clean(df3.iloc[i+1, 56])
            else:
                Eff_PFalc_AS_SP = 0
            
            if is_df3_true.iloc[i+1, 57] == True:
                Eff_PFalc_AS_SP_PQ = clean(df3.iloc[i+1, 57])
            else:
                Eff_PFalc_AS_SP_PQ = 0
            
            if is_df3_true.iloc[i+1, 58] == True:
                Eff_PFalc_AT_PG = clean(df3.iloc[i+1, 58])
            else:
                Eff_PFalc_AT_PG = 0

            if is_df3_true.iloc[i+1, 59] == True:
                Eff_PFalc_CQ_PQ = clean(df3.iloc[i+1, 59])
            else:
                Eff_PFalc_CQ_PQ = 0

            if is_df3_true.iloc[i+1, 60] == True:
                Eff_PFalc_DHA_PPQ = clean(df3.iloc[i+1, 60])
            else:
                Eff_PFalc_DHA_PPQ = 0
            
            if is_df3_true.iloc[i+1, 61] == True:
                Eff_PFalc_DHA_PPQ_PQ = clean(df3.iloc[i+1, 61])
            else:
                Eff_PFalc_DHA_PPQ_PQ = 0

            if is_df3_true.iloc[i+1, 62] == True:
                Eff_PFalc_PQ = clean(df3.iloc[i+1, 62])
            else:
                Eff_PFalc_PQ = 0

            if is_df3_true.iloc[i+1, 63] == True:
                Eff_PFalc_QN = clean(df3.iloc[i+1, 63])
            else:
                Eff_PFalc_QN = 0
            
            if is_df3_true.iloc[i+1, 64] == True:
                Eff_PFalc_QN_CL = clean(df3.iloc[i+1, 64])
            else:
                Eff_PFalc_QN_CL = 0
            
            if is_df3_true.iloc[i+1, 65] == True:
                Eff_PFalc_QN_D = clean(df3.iloc[i+1, 65])
            else:
                Eff_PFalc_QN_D = 0

            # Efficacy PVivax
            if is_df3_true.iloc[i+1, 96] == True:
                Eff_PVivax_CQ_PQ = clean(df3.iloc[i+1, 96])
            else:
                Eff_PVivax_CQ_PQ = 0
            
            if is_df3_true.iloc[i+1, 97] == True:
                Eff_PVivax_CQ = clean(df3.iloc[i+1, 97])
            else:
                Eff_PVivax_CQ = 0
            
            if is_df3_true.iloc[i+1, 98] == True:
                Eff_PVivax_DHA_PPQ = clean(df3.iloc[i+1, 98])
            else:
                Eff_PVivax_DHA_PPQ = 0

            if is_df3_true.iloc[i+1, 99] == True:
                Eff_PVivax_AL = clean(df3.iloc[i+1, 99])
            else:
                Eff_PVivax_AL = 0

            if is_df3_true.iloc[i+1, 100] == True:
                Eff_PVivax_AS_AQ_PQ = clean(df3.iloc[i+1, 100])
            else:
                Eff_PVivax_AS_AQ_PQ = 0

            if is_df3_true.iloc[i+1, 101] == True:
                Eff_PVivax_AL_PQ = clean(df3.iloc[i+1, 101])
            else:
                Eff_PVivax_AL_PQ = 0
            
            row3= [country3, malaria_prevalance, Coverage_Malaria_PFalc, Coverage_Malaria_PVivax, DALY_Malaria_Prop_PFalc, DALY_Malaria_Prop_PVivax,DALY_Malaria,Eff_PFalc_AL,Eff_PFalc_AL_PQ,Eff_PFalc_AM,Eff_PFalc_ART_NQ,Eff_PFalc_ART_PPQ,Eff_PFalc_AS_AQ,Eff_PFalc_AS_MQ,Eff_PFalc_AS_MQ_PQ,Eff_PFalc_AS_SP,Eff_PFalc_AS_SP_PQ,Eff_PFalc_AT_PG,Eff_PFalc_CQ_PQ,Eff_PFalc_DHA_PPQ,Eff_PFalc_DHA_PPQ_PQ,Eff_PFalc_PQ,Eff_PFalc_QN,Eff_PFalc_QN_CL,Eff_PFalc_QN_D,Eff_PVivax_CQ_PQ,Eff_PVivax_CQ,Eff_PVivax_DHA_PPQ,Eff_PVivax_AL,Eff_PVivax_AS_AQ_PQ,Eff_PVivax_AL_PQ]
            # row = [country]
            spec_2010_Malaria_data.append(row3)

        for k in spec_2010_Malaria_data:
            # print(k)
            conn.execute(''' INSERT INTO spec_2010_Malaria VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', k)
        
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
