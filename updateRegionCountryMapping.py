import sqlite3
import pandas as pd
import unicodedata

def createTablesCountry():
	conn = sqlite3.connect('ghi.db')
	conn.text_factory = str
	conn.execute(''' DROP TABLE IF EXISTS region_country_mapping''')
	conn.execute(''' CREATE TABLE region_country_mapping (country text, region text)''')
	conn.close()

def uploadRegionCountryMapping():
	# try :
    createTablesCountry()
    conn = sqlite3.connect('ghi.db')
    conn.text_factory = str
    url = "region_country_mapping.csv"
    df = pd.read_csv(url)
    sqlquery = ''' INSERT INTO region_country_mapping VALUES (?,?) '''
    for index, row in df.iterrows():
        conn.execute(sqlquery, [row[0], row[1]])
    conn.commit()
    print("Database operation compelete")
    conn.close()
    return 'success'
	# except Exception as e:
	# 	error = e
	# 	print(error)
	# 	conn.rollback()
	# 	conn.close()
	# 	return error

uploadRegionCountryMapping()
