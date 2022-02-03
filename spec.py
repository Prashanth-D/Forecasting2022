import sqlite3
import pandas as pd
import math

conn = sqlite3.connect('./K_ghi.db')

conn.execute('''DROP TABLE IF EXISTS spec_2015_TB''')

conn.execute('''CREATE TABLE spec_2015_TB
             (country text, TB_prevalance text)''')
#

#datasrc = 'https://docs.google.com/spreadsheets/d/1KtWAdu4qO0mRJREY5Aje5CMZhdnxPoTPRdBXIUKN-uw/pub?gid=1560508440&single=true&output=csv'
#datasrc20102015 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=1560508440&single=true&output=csv'
datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1560508440&single=true&output=csv';
datasrc2010B2015 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=1560508440&single=true&output=csv';

df = pd.read_csv(datasrc, skiprows=1)
df2015 = pd.read_csv(datasrc2010B2015, skiprows=1)
drugdata = []
drug2010 = []
drug2013 = []
drug2010B2015 = []

for i in range(1,43):
    name = df.iloc[5,i]
    # akshay_mod
    patDate = df.iloc[3, i]
    if type(patDate) != int:
        patDate = int(max(patDate.split('/')))
    #
    for j in range(8,20):
        temp = df.iloc[j,i]
        if type(temp) != float:
            temp = float(temp.replace(',',''))

            if temp > 0:
                if j == 8 or j == 9 or j == 10:
                    disease = 'TB'
                    color = '#FFB31C'
                elif j == 11 or j == 12:
                    disease = 'Malaria'
                    color = '#0083CA'
                elif j == 13:
                    disease = 'HIV'
                    color = '#EF3E2E'
                elif j == 14:
                    disease = 'Roundworm'
                    color = '#003452'
                elif j == 15:
                    disease = 'Hookworm'
                    color = '#86AAB9'
                elif j == 16:
                    disease = 'Whipworm'
                    color = '#CAEEFD'
                elif j == 17:
                    disease = 'Schistosomiasis'
                    color = '#546675'
                elif j == 18:
                    disease = 'Onchocerciasis'
                    color = '#8A5575'
                elif j == 19:
                    disease = 'LF'
                    color = '#305516'
                # akshay_mod
                # company = df.iloc[0,i]
                company = df.iloc[1,i]
                #

                # akshay_mod
                # drugrow = [name, company, disease,temp,color]
                drugrow = [name, company, disease, temp, color, patDate]
                #
                drug2010.append(drugrow)
    score = float(df.iloc[20,i].replace(',',''))
    row = [name,score]
    drugdata.append(row)

sortedlist = sorted(drug2010, key=lambda xy: xy[3], reverse=True)

data = drugdata
maxrow = sortedlist[0]
maximum = maxrow[3]


for y in sortedlist:
    percent = (float(y[3]) / float(maximum)) * 100

    y.append(percent)
    # print(y + [y[5]])

for row in sortedlist:
    # akshay_mod
    # conn.execute('insert into drug2010 values (?,?,?,?,?,?)', row)
    conn.execute('insert into drug2010 values (?,?,?,?,?,?,?)', row)
    #

for i in range(50,95):
    name = df.iloc[5,i]
    # akshay_mod
    patDate = df.iloc[3, i]
    if (type(patDate) != int):
        check = df.isnull().iloc[3, i]
        if check == True:
            patDate = 1990
        else:
            patDate = int(min(patDate.split('/')))
    #
    for j in range(8,20):
        temp = df.iloc[j,i]
        if type(temp) != float:
            temp = float(temp.replace(',',''))

            if temp > 0:
                if j == 8 or j == 9 or j == 10:
                    disease = 'TB'
                    color = '#FFB31C'
                elif j == 11 or j == 12:
                    disease = 'Malaria'
                    color = '#0083CA'
                elif j == 13:
                    disease = 'HIV'
                    color = '#EF3E2E'
                elif j == 14:
                    disease = 'Roundworm'
                    color = '#003452'
                elif j == 15:
                    disease = 'Hookworm'
                    color = '#86AAB9'
                elif j == 16:
                    disease = 'Whipworm'
                    color = '#CAEEFD'
                elif j == 17:
                    disease = 'Schistosomiasis'
                    color = '#546675'
                elif j == 18:
                    disease = 'Onchocerciasis'
                    color = '#8A5575'
                elif j == 19:
                    disease = 'LF'
                    color = '#305516'
                # akshay_mod
                # company = df.iloc[0,i]
                company = df.iloc[1,i]
                #
                # akshay_mod
                # drugrow = [name, company, disease,temp,color]
                drugrow = [name, company, disease,temp, color, patDate]
                #
                drug2013.append(drugrow)

sortedlist = sorted(drug2013, key=lambda xy: xy[3], reverse=True)

data = drugdata
maxrow = sortedlist[0]
maximum = maxrow[3]

for y in sortedlist:
    percent = (float(y[3]) / maximum) * 100

    y.append(percent)

for row in sortedlist:
    # akshay_mod
    # conn.execute('insert into drug2013 values (?,?,?,?,?,?)', row)
    conn.execute('insert into drug2013 values (?,?,?,?,?,?,?)', row)
    #

for i in range(50,95):
    name = df2015.iloc[5,i]
    # akshay_mod
    patDate = df2015.iloc[3, i]
    if (type(patDate) != int):
        check = df2015.isnull().iloc[3, i]
        if check == True:
            patDate = 1990
        else:
            patDate = int(max(patDate.split('/')))
    #
    for j in range(8,20):
        temp = df2015.iloc[j,i]
        if type(temp) != float:
            temp = float(temp.replace(',',''))

            if temp > 0:
                if j == 8 or j == 9 or j == 10:
                    disease = 'TB'
                    color = '#FFB31C'
                elif j == 11 or j == 12:
                    disease = 'Malaria'
                    color = '#0083CA'
                elif j == 13:
                    disease = 'HIV'
                    color = '#EF3E2E'
                elif j == 14:
                    disease = 'Roundworm'
                    color = '#003452'
                elif j == 15:
                    disease = 'Hookworm'
                    color = '#86AAB9'
                elif j == 16:
                    disease = 'Whipworm'
                    color = '#CAEEFD'
                elif j == 17:
                    disease = 'Schistosomiasis'
                    color = '#546675'
                elif j == 18:
                    disease = 'Onchocerciasis'
                    color = '#8A5575'
                elif j == 19:
                    disease = 'LF'
                    color = '#305516'
                # akshay_mod
                # company = df.iloc[0,i]
                company = df2015.iloc[1,i]

                # drugrow = [name, company, disease,temp,color]
                drugrow = [name, company, disease, temp, color, patDate]
                print(str(drugrow))
                #
                drug2010B2015.append(drugrow)

sortedlist = sorted(drug2010B2015, key=lambda xy: xy[3], reverse=True)

data = drugdata
maxrow = sortedlist[0]

maximum = maxrow[3]

for y in sortedlist:
    percent = (float(y[3]) / maximum) * 100

    y.append(percent)

for row in sortedlist:
    # akshay_mod
    # conn.execute('insert into drug2015 values (?,?,?,?,?,?)', row)
    conn.execute('insert into drug2015 values (?,?,?,?,?,?,?)', row)
    #


conn.commit()
