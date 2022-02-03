import sqlite3
import pandas as pd
import unicodedata

def createTablesSpec():
    conn = sqlite3.connect('K_ghi.db')
    conn.execute(''' DROP TABLE IF EXISTS country_codes ''')
    conn.execute(''' CREATE TABLE country_codes (country text, ccode text) ''')
    conn.close()
    return

def uploadSpecData():
    conn = sqlite3.connect('K_ghi.db')
    url = "ccode.csv"
    df = pd.read_csv(url)
    try:
        createTablesSpec()
        table = []
        for index, row in df.iterrows():
            country = row['Name']
            code = row['Code']
            trow = [country, code]
            table.append(trow)
        for k in table:
            conn.execute(''' INSERT INTO country_codes VALUES (?,?)''', k)
        print("Database operation compelete")
        conn.commit()
        return 'success'
    except Exception as e:
        error = e
        conn.rollback()
        conn.close()
        return error
    return

uploadSpecData()