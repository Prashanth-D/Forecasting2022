import sqlite3
import pandas as pd
import unicodedata

def createTablesCountry():
	conn = sqlite3.connect('ghi3.db')
	conn.text_factory = str
	conn.execute(''' DROP TABLE IF EXISTS drugimpact2010 ''')
	conn.execute(''' DROP TABLE IF EXISTS drugimpact2015 ''')
	conn.execute(''' CREATE TABLE drugimpact2010 (country text, tb_impact_of_active_tb_hiv_positive_treatment_regimen real, tb_impact_of_active_tb_hiv_negative_treatment_regimen real, tb_impact_of_mdr_tb_treatment_regimen_Z_S_Lfx_Eto_Cs_PAS real, tb_impact_of_mdr_tb_treatment_regimen_S_Lfx_Eto_Cs_PAS real, tb_impact_of_mdr_tb_treatment_regimen_Km_Lfx_Eto_Cs_PAS real, tb_impact_of_xdr_tb_treatment_regimen_Cs_Km_or_Amk_or_Cm_Lfx_or_Mfx_or_Gfx_or_Ofx real, malaria_p_falc_impact_of_AL real, malaria_p_falc_impact_of_AS_SP real, malaria_p_falc_impact_of_DHA_PPQ real, malaria_p_falc_impact_of_AS_MQ real, malaria_p_falc_impact_of_AS_AQ real, malaria_p_falc_impact_of_CQ_PQ real, malaria_p_falc_impact_of_DHA_PPQ_PQ real, malaria_p_falc_impact_of_ART_NQ real, malaria_p_falc_impact_of_ART_PPQ real, malaria_p_falc_impact_of_AL_PQ real, malaria_p_falc_impact_of_SP real, malaria_p_falc_impact_of_AS_MQ_PQ real, malaria_p_falc_impact_of_QN_CL real, malaria_p_falc_impact_of_QN_D real, malaria_p_vivax_impact_of_CQ_PQ real, malaria_p_vivax_impact_of_CQ real, malaria_p_vivax_impact_of_CQ_PG real, malaria_p_vivax_impact_of_AL real, malaria_p_vivax_impact_of_AL_PQ real, malaria_p_vivax_impact_of_AS_AQ real, malaria_p_vivax_impact_of_DHA_PPQ_PQ real, hiv_impact_of_3TC real, hiv_impact_of_ABC real, hiv_impact_of_AZT real, hiv_impact_of_ddl real, hiv_impact_of_d4T real, hiv_impact_of_EFV real, hiv_impact_of_FTC real, hiv_impact_of_LPV_r real, hiv_impact_of_NVP real, hiv_impact_of_TDF real, hiv_impact_of_ATV_r real, hiv_impact_of_NFV real, roundworm_Alb real, roundworm_Mbd real, roundworm_Ivm_Alb real, hook_Alb real, hook_Mbd real, whipworm_Alb real, whipworm_Mbd real, whipworm_Ivm_Alb real, schistosomiasis_PZQ real, lf_impact_of_Single_dose_of_DEC_6mg_kg_ALB_400mg real, lf_impact_of_Combination_of_ALB_400mg_IVM_400ug_kg real) ''')
	conn.execute(''' CREATE TABLE drugimpact2015 (country text, tb_impact_of_active_tb_hiv_positive_treatment_regimen real, tb_impact_of_active_tb_hiv_negative_treatment_regimen real, tb_impact_of_mdr_tb_treatment_regimen_Z_S_Lfx_Eto_Cs_PAS real, tb_impact_of_mdr_tb_treatment_regimen_S_Lfx_Eto_Cs_PAS real, tb_impact_of_mdr_tb_treatment_regimen_Km_Lfx_Eto_Cs_PAS real, tb_impact_of_xdr_tb_treatment_regimen_Cs_Km_or_Amk_or_Cm_Lfx_or_Mfx_or_Gfx_or_Ofx real, malaria_p_falc_impact_of_AL real, malaria_p_falc_impact_of_AL_PQ real, malaria_p_falc_impact_of_AM real, malaria_p_falc_impact_of_ART_NQ real, malaria_p_falc_impact_of_ART_PPQ real, malaria_p_falc_impact_of_AS_AQ real, malaria_p_falc_impact_of_AS_MQ real, malaria_p_falc_impact_of_AS_MQ_PQ real, malaria_p_falc_impact_of_AS_SP real, malaria_p_falc_impact_of_AS_SP_PQ real, malaria_p_falc_impact_of_AT_PG real, malaria_p_falc_impact_of_CQ_PQ real, malaria_p_falc_impact_of_DHA_PPQ real, malaria_p_falc_impact_of_DHA_PPQ_PQ real, malaria_p_falc_impact_of_PQ real, malaria_p_falc_impact_of_QN real, malaria_p_falc_impact_of_QN_CL real, malaria_p_falc_impact_of_QN_D real, malaria_p_vivax_impact_of_CQ_PQ real, malaria_p_vivax_impact_of_CQ real, malaria_p_vivax_impact_of_DHA_PPQ real, malaria_p_vivax_impact_of_AL real, malaria_p_vivax_impact_of_AL_PQ real, malaria_p_vivax_impact_of_AS_AQ_PQ real, hiv_impact_of_3TC real, hiv_impact_of_ABC real, hiv_impact_of_AZT real, hiv_impact_of_ddl real, hiv_impact_of_d4T real, hiv_impact_of_EFV real, hiv_impact_of_FTC real, hiv_impact_of_LPV_r real, hiv_impact_of_NVP real, hiv_impact_of_ATV_r real, hiv_impact_of_TDF real, roundworm_Alb real, roundworm_Mbd real, roundworm_Ivm_Alb real, hook_Alb real, hook_Mbd real, whipworm_Alb real, whipworm_Mbd real, whipworm_Ivm_Alb real, schistosomiasis_PZQ real, onchoceriasis_Ivermectin real, lf_impact_of_Single_dose_of_DEC_6mg_kg_ALB_400mg real, lf_impact_of_Combination_of_ALB_400mg_IVM_400ug_kg real) ''')
	conn.close()
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
        return float(0)

def uploadCountryData():
	try :
		createTablesCountry()
		conn = sqlite3.connect('ghi3.db')
		conn.text_factory = str
		url = "drugimpactdata.csv"
		df = pd.read_csv(url, skiprows=1)
		is_df_true = df.notnull()
		countrydata1 = []
		#2010
		for row in range(3, 220):
			rowData = []
			country = df.iloc[row, 0]
			rowData.append(country)
			for i in range(1,63):
				if (i not in [7,22,30,31,44,53,54,55,56,58,61,62]):
					if (is_df_true.iloc[row, i] == True):
						rowData.append(clean(df.iloc[row, i].strip()))
					else:
						rowData.append(float(0))
			countrydata1.append(rowData)
		sqlquery = ''' INSERT INTO drugimpact2010 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
		for k in countrydata1:
			conn.execute(sqlquery, k)
		#2015
		countrydata2 = []
		for row in range(3, 220):
			rowData1 = []
			country = df.iloc[row, 0]
			rowData1.append(country)
			for i in range(65,129):
				if (i not in [71,90,97,98,110,119,120,121,122,124,126]):
					if (is_df_true.iloc[row, i] == True):
						rowData1.append(clean(df.iloc[row, i].strip()))
					else:
						rowData1.append(float(0))
			countrydata2.append(rowData1)
		sqlquery2 = '''INSERT INTO drugimpact2015 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
		for k in countrydata2:
			conn.execute(sqlquery2, k)
		conn.commit()
		print("Database operation compelete")
		conn.close()
		return 'success'
	except Exception as e:
		error = e
		print(error)
		conn.rollback()
		conn.close()
		return error

uploadCountryData()
