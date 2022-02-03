import sqlite3
import pandas as pd
import unicodedata

def createTablesSpec():
    conn = sqlite3.connect('K_ghi.db')
    conn.execute(''' DROP TABLE IF EXISTS spec_2015_NTD ''')
    conn.execute(''' CREATE TABLE spec_2015_NTD
    (country text, worm_preSac_coverage real, worm_Sac_coverage real, roundworm_prevalance_child real, roundworm_prevalance_adult real, roundworm_Efficacy_ALB real, roundworm_Efficacy_Mbd real, roundworm_Efficacy_Ivm_Alb real, roundworm_DALY_child real, roundworm_DALY_adult real,
    hookworm_prevalance_child real, hookworm_prevalance_adult real, hookworm_Efficacy_ALB real, hookworm_Efficacy_Mbd real, hookworm_DALY_child real, hookworm_DALY_adult real,
    whipworm_prevalance_child real, whipworm_prevalance_adult real, whipworm_Efficacy_ALB real, whipworm_Efficacy_Mbd real, whipworm_Efficacy_Ivm_Alb real, whipworm_DALY_child real, whipworm_DALY_adult real,
    schi_prevalance real,schi_coverage real, schi_Efficacy real,schi_DALY real,
    onch_prevalance real, onch_coverage real, onch_Efficacy real, onch_DALY real,
    LF_prevalance real, LF_coverage real, LF_Efficacy_DEC real, LF_Efficacy_DEC_ALB real, LF_Efficacy_IVM_ALB real,LF_DALY real) ''')
    
    conn.close()
    return

def uploadSpecData():
    conn = sqlite3.connect('K_ghi.db')
    url = "ORS_Forecasting_NTD_2015.csv"
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
        spec_2015_NTD_data = []
        # print(df.iloc[0, 89])
        for i in range(1, 218):
            country = df.iloc[i, 0]
            # Worms
            if is_df_true.iloc[i, 22] == True:
                worm_preSac_coverage = clean(df.iloc[i, 22])
            else:
                worm_preSac_coverage = 0
            if is_df_true.iloc[i, 24] == True:
                worm_Sac_coverage = clean(df.iloc[i, 24])
            else:
                worm_Sac_coverage = 0
            # Roundworm
            if is_df_true.iloc[i, 36] == True:
                roundworm_prevalance_child = clean(df.iloc[i, 36])
            else:
                roundworm_prevalance_child = 0
                
            if is_df_true.iloc[i, 37] == True:
                roundworm_prevalance_adult = clean(df.iloc[i, 37])
            else:
                roundworm_prevalance_adult = 0
            
            if is_df_true.iloc[i, 58] == True:
                roundworm_Efficacy_ALB = clean(df.iloc[i, 58])
            else:
                roundworm_Efficacy_ALB = 0
            if is_df_true.iloc[i, 60] == True:
                roundworm_Efficacy_Mbd = clean(df.iloc[i, 60])
            else:
                roundworm_Efficacy_Mbd = 0
            if is_df_true.iloc[i, 62] == True:
                roundworm_Efficacy_Ivm_Alb = clean(df.iloc[i, 62])
            else:
                roundworm_Efficacy_Ivm_Alb = 0
            if is_df_true.iloc[i, 11] == True:
                roundworm_DALY_child = clean(df.iloc[i, 11])
            else:
                roundworm_DALY_child = 0
            if is_df_true.iloc[i, 12] == True:
                roundworm_DALY_adult = clean(df.iloc[i, 12])
            else:
                roundworm_DALY_adult = 0
            
            # Hookworm
            if is_df_true.iloc[i, 34] == True:
                hookworm_prevalance_child = clean(df.iloc[i, 34])
            else:
                hookworm_prevalance_child = 0
                
            if is_df_true.iloc[i, 35] == True:
                hookworm_prevalance_adult = clean(df.iloc[i, 35])
            else:
                hookworm_prevalance_adult = 0
            
            if is_df_true.iloc[i, 54] == True:
                hookworm_Efficacy_ALB = clean(df.iloc[i, 54])
            else:
                hookworm_Efficacy_ALB = 0
            if is_df_true.iloc[i, 56] == True:
                hookworm_Efficacy_Mbd = clean(df.iloc[i, 56])
            else:
                hookworm_Efficacy_Mbd = 0
            if is_df_true.iloc[i, 8] == True:
                hookworm_DALY_child = clean(df.iloc[i, 8])
            else:
                hookworm_DALY_child = 0
            if is_df_true.iloc[i, 9] == True:
                hookworm_DALY_adult = clean(df.iloc[i, 9])
            else:
                hookworm_DALY_adult = 0
            
            # Whipworm
            if is_df_true.iloc[i, 32] == True:
                whipworm_prevalance_child = clean(df.iloc[i, 32])
            else:
                whipworm_prevalance_child = 0
                
            if is_df_true.iloc[i, 33] == True:
                whipworm_prevalance_adult = clean(df.iloc[i, 33])
            else:
                whipworm_prevalance_adult = 0
            
            if is_df_true.iloc[i, 48] == True:
                whipworm_Efficacy_ALB = clean(df.iloc[i, 48])
            else:
                whipworm_Efficacy_ALB = 0
            if is_df_true.iloc[i, 50] == True:
                whipworm_Efficacy_Mbd = clean(df.iloc[i, 50])
            else:
                whipworm_Efficacy_Mbd = 0
            if is_df_true.iloc[i, 52] == True:
                whipworm_Efficacy_Ivm_Alb = clean(df.iloc[i, 52])
            else:
                whipworm_Efficacy_Ivm_Alb = 0
            if is_df_true.iloc[i, 5] == True:
                whipworm_DALY_child = clean(df.iloc[i, 5])
            else:
                whipworm_DALY_child = 0
            if is_df_true.iloc[i, 6] == True:
                whipworm_DALY_adult = clean(df.iloc[i, 6])
            else:
                whipworm_DALY_adult = 0

            # Schistosomiasis 
            if is_df_true.iloc[i, 30] == True:
                schi_prevalance = clean(df.iloc[i, 30])
            else:
                schi_prevalance = 0
            if is_df_true.iloc[i, 20] == True:
                schi_coverage = clean(df.iloc[i, 20])
            else:
                schi_coverage = 0
            if is_df_true.iloc[i, 46] == True:
                schi_Efficacy = clean(df.iloc[i, 46])
            else:
                schi_Efficacy = 0
            if is_df_true.iloc[i, 4] == True:
                schi_DALY = clean(df.iloc[i, 4])
            else:
                schi_DALY = 0
            
            # Oncheriasis 
            if is_df_true.iloc[i, 38] == True:
                onch_prevalance = clean(df.iloc[i, 38])
            else:
                onch_prevalance = 0
            if is_df_true.iloc[i, 28] == True:
                onch_coverage = clean(df.iloc[i, 28])
            else:
                onch_coverage = 0
            if is_df_true.iloc[i, 64] == True:
                onch_Efficacy = clean(df.iloc[i, 64])
            else:
                onch_Efficacy = 0
            if is_df_true.iloc[i, 14] == True:
                onch_DALY = clean(df.iloc[i, 14])
            else:
                onch_DALY = 0
            # LF 
            if is_df_true.iloc[i, 29] == True:
                LF_prevalance = clean(df.iloc[i, 29])
            else:
                LF_prevalance = 0
            if is_df_true.iloc[i, 18] == True:
                LF_coverage = clean(df.iloc[i, 18])
            else:
                LF_coverage = 0
            if is_df_true.iloc[i, 40] == True:
                LF_Efficacy_DEC = clean(df.iloc[i, 40])
            else:
                LF_Efficacy_DEC = 0
            if is_df_true.iloc[i, 42] == True:
                LF_Efficacy_DEC_ALB = clean(df.iloc[i, 42])
            else:
                LF_Efficacy_DEC_ALB = 0
            if is_df_true.iloc[i, 44] == True:
                LF_Efficacy_IVM_ALB = clean(df.iloc[i, 44])
            else:
                LF_Efficacy_IVM_ALB = 0
            if is_df_true.iloc[i, 3] == True:
                LF_DALY = clean(df.iloc[i, 3])
            else:
                LF_DALY = 0
            
            row = [country, worm_preSac_coverage, worm_Sac_coverage, roundworm_prevalance_child, roundworm_prevalance_adult, roundworm_Efficacy_ALB, roundworm_Efficacy_Mbd, roundworm_Efficacy_Ivm_Alb, roundworm_DALY_child, roundworm_DALY_adult,
            hookworm_prevalance_child, hookworm_prevalance_adult, hookworm_Efficacy_ALB, hookworm_Efficacy_Mbd, hookworm_DALY_child, hookworm_DALY_adult,
            whipworm_prevalance_child, whipworm_prevalance_adult, whipworm_Efficacy_ALB, whipworm_Efficacy_Mbd, whipworm_Efficacy_Ivm_Alb, whipworm_DALY_child, whipworm_DALY_adult,
            schi_prevalance,schi_coverage, schi_Efficacy,schi_DALY,
            onch_prevalance, onch_coverage, onch_Efficacy, onch_DALY,
            LF_prevalance, LF_coverage, LF_Efficacy_DEC, LF_Efficacy_DEC_ALB, LF_Efficacy_IVM_ALB,LF_DALY]
            
            spec_2015_NTD_data.append(row)
            
        for k in spec_2015_NTD_data:
            print(k)
            conn.execute(''' INSERT INTO spec_2015_NTD VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', k)
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
