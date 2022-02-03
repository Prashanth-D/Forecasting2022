import sqlite3
import pandas as pd
import unicodedata

def createTablesCountry():
	conn = sqlite3.connect('ghi2.db')
	conn.execute(''' DROP TABLE IF EXISTS country2010 ''')
	conn.execute(''' DROP TABLE IF EXISTS country2015 ''')
	conn.execute(''' CREATE TABLE country2010 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, lf real) ''')
	conn.execute(''' CREATE TABLE country2015 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchoceriasis real, lf real) ''')
	conn.close()
	return

def uploadCountryData():
	conn = sqlite3.connect('ghi2.db')
	url = "ORS_Impact_Score_2010B_2015.csv"
	df = pd.read_csv(url, skiprows=2)
	print(df.iloc[1])

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
		countrydata1 = []
		#2010
		for i in range(3, 220):
			country = df.iloc[i, 0]
			if is_df_true.iloc[i, 7] == True:
				tb = clean(df.iloc[i, 7])
			else:
				tb = 0
			if is_df_true.iloc[i, 34] == True:
				malaria = clean(df.iloc[i, 34])
			else:
				malaria = 0
			if is_df_true.iloc[i, 47] == True:
				hiv = clean(df.iloc[i, 47])
			else:
				hiv = 0
			if is_df_true.iloc[i, 56] == True:
				roundworm = clean(df.iloc[i, 56])
			else:
				roundworm = 0
			if is_df_true.iloc[i, 57] == True:
				hookworm = clean(df.iloc[i, 57])
			else:
				hookworm = 0
			if is_df_true.iloc[i, 58] == True:
				whipworm = clean(df.iloc[i, 58])
			else:
				whipworm = 0
			if is_df_true.iloc[i, 61] == True:
				schistosomiasis = clean(df.iloc[i, 61])
			else:
				schistosomiasis = 0
			if is_df_true.iloc[i, 64] == True:
				lf = clean(df.iloc[i, 64])
			else:
				lf = 0
			total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistosomiasis + lf
			row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf]
			countrydata1.append(row)
		for k in countrydata1:
			conn.execute(''' INSERT INTO country2010 VALUES (?,?,?,?,?,?,?,?,?,?) ''', k)
		conn.commit()
		countrydata2 = []
		for i in range(3, 220):
			country = df.iloc[i, 67]
			if is_df_true.iloc[i, 74] == True:
				tb = clean(df.iloc[i, 74])
			else:
				tb = 0
			if is_df_true.iloc[i, 104] == True:
				malaria = clean(df.iloc[i, 104])
			else:
				malaria = 0
			if is_df_true.iloc[i, 115] == True:
				hiv = clean(df.iloc[i, 115])
			else:
				hiv = 0
			if is_df_true.iloc[i, 124] == True:
				roundworm = clean(df.iloc[i, 124])
			else:
				roundworm = 0
			if is_df_true.iloc[i, 125] == True:
				hookworm = clean(df.iloc[i, 125])
			else:
				hookworm = 0
			if is_df_true.iloc[i, 126] == True:
				whipworm = clean(df.iloc[i, 126])
			else:
				whipworm = 0
			if is_df_true.iloc[i, 129] == True:
				schistosomiasis = clean(df.iloc[i, 129])
			else:
				schistosomiasis = 0
			if is_df_true.iloc[i, 131] == True:
				onchoceriasis = clean(df.iloc[i, 131])
			else:
				onchoceriasis = 0
			if is_df_true.iloc[i, 134] == True:
				lf = clean(df.iloc[i, 134])
			else:
				lf = 0
			total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistosomiasis + onchoceriasis + lf
			row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchoceriasis, lf]
			countrydata2.append(row)
		for k in countrydata2:
			conn.execute(''' INSERT INTO country2015 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', k)
		conn.commit()
		conn.close()
		print("Database operation compelete")
		return 'success'
	except Exception as e:
		error = e
		conn.rollback()
		conn.close()
		return error
	return df
uploadCountryData()
