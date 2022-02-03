import sqlite3
import pandas as pd
import unicodedata

conn = sqlite3.connect('K_ghi.db')
conn.execute('''DROP TABLE IF EXISTS spec_treatment_regimen_2015''')
conn.execute('''CREATE TABLE spec_treatment_regimen_2015
             (drug text,tb_hiv_plus text,tb_hiv_minus text, tb_mdr text, tb_xdr text,malaria_PFalc text,malaria_PVivax text)''')
#datasrc2015 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=1560508440&single=true&output=csv';
#df2015 = pd.read_csv(datasrc2015, skiprows=1)

#url_datasrc2015 = 'ORS_Global_Burden_of_Disease_2015.csv'
#df2015 = pd.read_csv(url_datasrc2015, skiprows=1)
drug2015 = []

url = "Impact_Score.csv"
df_impact_score = pd.read_csv(url, skiprows=1)

# Malaria PFalc
drug = []
drug_PFalc = []
for i in range(72,90):
    drug_PFalc.append(df_impact_score.iloc[0,i])
    # drug.append(df_impact_score.iloc[0,i])
drug = drug + list(set(drug_PFalc) - set(drug))

# Malaria PVivax
drug_PVivax = []
for i in range(91,97):
    drug_PVivax.append(df_impact_score.iloc[0,i])
# print(drug_PVivax)  
# print("\n\n")  
drug = drug + list(set(drug_PVivax) - set(drug))

# TB
arr_treat_reg_tb_hiv_plus = []
treat_reg_tb_hiv_plus = list(df_impact_score.iloc[1,65].split(","))
for i in treat_reg_tb_hiv_plus:
    i = str(i)
    arr_treat_reg_tb_hiv_plus.append(i[i.find('(')+1 : i.find(')')])
drug = drug + list(set(arr_treat_reg_tb_hiv_plus) - set(drug))


arr_treat_reg_tb_hiv_minus = []
treat_reg_tb_hiv_minus = list(df_impact_score.iloc[1,66].split(","))
for i in treat_reg_tb_hiv_minus:
    i = str(i)
    arr_treat_reg_tb_hiv_minus.append(i[i.find('(')+1 : i.find(')')])
drug = drug + list(set(arr_treat_reg_tb_hiv_minus) - set(drug))

treat_reg_mdr = list(df_impact_score.iloc[1,67].replace('+',',').replace('(or)',',').split(','))
# drug = drug + list(set(treat_reg_mdr) - set(drug))

treat_reg_mdr1 = list(df_impact_score.iloc[1,68].replace('+',',').replace('(or)',',').split(','))
treat_reg_mdr = treat_reg_mdr + list(set(treat_reg_mdr1) - set(treat_reg_mdr))

treat_reg_mdr2 = list(df_impact_score.iloc[1,69].replace('+',',').replace('(or)',',').split(','))
treat_reg_mdr = treat_reg_mdr + list(set(treat_reg_mdr2) - set(treat_reg_mdr))
drug = drug + list(set(treat_reg_mdr) - set(drug))

treat_reg_xdr = list(df_impact_score.iloc[1,70].replace('+',',').replace('(or)',',').split(','))
drug = drug + list(set(treat_reg_xdr) - set(drug))
# print(treat_reg_xdr)


sortedlist = sorted(drug, reverse=False)
# print(sortedlist)
# print("\n\n")  

drug2015 = []
for i in sortedlist:
    drug_name = i
    if(i in arr_treat_reg_tb_hiv_plus):
        tb_hiv_plus = 'True'
    else:
        tb_hiv_plus = 'False'

    if(i in arr_treat_reg_tb_hiv_minus):
        tb_hiv_minus = 'True'
    else:
        tb_hiv_minus = 'False'

    if(i in treat_reg_mdr):
        tb_mdr = 'True'
    else:
        tb_mdr = 'False'

    if(i in treat_reg_xdr):
        tb_xdr = 'True'
    else:
        tb_xdr = 'False'
    
    if(i in drug_PFalc):
        malaria_PFalc = 'True'
    else:
        malaria_PFalc = 'False'
    
    if(i in drug_PVivax):
        malaria_PVivax = 'True'
    else:
        malaria_PVivax = 'False'

    drugrow = [drug_name,tb_hiv_plus,tb_hiv_minus,tb_mdr,tb_xdr,malaria_PFalc,malaria_PVivax]
    # print(drugrow)
    drug2015.append(drugrow)
# print(drug2015)

sortedlist = sorted(drug2015, reverse=False)
for row in sortedlist:
    # print(row)
    conn.execute('insert into spec_treatment_regimen_2015 values (?,?,?,?,?,?,?)', row)
conn.commit()
conn.close()
print("Database operation compelete")