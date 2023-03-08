import mysql.connector
import pandas as pd 
phone_pe=mysql.connector.connect(host='localhost',
                        database='phone_pe',
                        user='root',
                        password='*****') #Your Password
mycursor = phone_pe.cursor()

#Creating table for Aggrigate Transaction:
sq1= "CREATE TABLE if not exists ATransaction (MyIndex INT NOT NULL AUTO_INCREMENT,State VARCHAR(50),Year INT,Quater INT,Transaction_type VARCHAR(100),Transaction_count BIGINT,Transaction_amount FLOAT,PRIMARY KEY (MyIndex))"

mycursor.execute(sq1)
print('Table created successfully.')
phone_pe.commit()
df=pd.read_csv(r"C:/Users/new/Desktop/PHONEPE/pulse/df_aggregated_transaction.csv")
for index, row in df.iterrows():
     quer="INSERT INTO Phone_pe.ATransaction(State,Year,Quater,Transaction_type,Transaction_count,Transaction_amount) values(%s,%s,%s,%s,%s,%s)"
     mycursor.execute(quer,(row.State,row.Year,row.Quater,row.Transaction_type,row.Transaction_count,row.Transaction_amount))
print('DataFrame Inserted successfully.')
phone_pe.commit()
#mycursor.close()

#Creating table for Aggregate userby Dvice:
sq2 ='CREATE TABLE if not exists agg_userbydevice(MyIndex INT NOT NULL AUTO_INCREMENT,State VARCHAR(100),Year INT,Quater INT,brands VARCHAR(100),Count BIGINT,Percentage BIGINT,PRIMARY KEY (MyIndex))'

mycursor.execute(sq2)
print('Table created successfully.')
phone_pe.commit()
df1=pd.read_csv(r"C:/Users/new/Desktop/PHONEPE/pulse/df_aggregated_user.csv")
for index, row in df1.iterrows():                       
     query="INSERT INTO Phone_pe.agg_userbydevice(State,Year,Quater,brands,Count,Percentage) values(%s,%s,%s,%s,%s,%s)"
     mycursor.execute(query,(row.State,row.Year,row.Quater,row.brands,row.Count,row.Percentage))
print('DataFrame Inserted successfully.')
phone_pe.commit()
#mycursor.close()

#Creating table for District wise Map Transaction:
sq='CREATE TABLE if not exists district_maptransaction(MyIndex INT NOT NULL AUTO_INCREMENT,State VARCHAR(100),Year INT,Quater INT,District VARCHAR(50),Count BIGINT,Amount BIGINT,PRIMARY KEY (MyIndex))'

mycursor.execute(sq) 
print('Table created successfully.')
phone_pe.commit()
df2=pd.read_csv(r"C:/Users/new/Desktop/PHONEPE/pulse/df_map_transaction.csv")
for index, row in df2.iterrows():      
     query2="INSERT INTO Phone_Pe.district_maptransaction(State,Year,Quater,District,Count,amount) values(%s,%s,%s,%s,%s,%s)"
     mycursor.execute(query2,(row.State,row.Year,row.Quater,row.District,row.Count,row.amount))
print('DataFrame Inserted successfully.')
phone_pe.commit()
#mycursor.close()

                                                                                
#Creating table for District wise user:
sql4 ='CREATE TABLE if not exists district_map_Registered_user(MyIndex INT NOT NULL AUTO_INCREMENT,State VARCHAR(100),Year INT,Quater INT,District VARCHAR(100),RegisteredUser BIGINT,PRIMARY KEY (MyIndex))'

mycursor.execute(sql4) 
print('Table created successfully.')
phone_pe.commit()
df3=pd.read_csv(r"C:/Users/new/Desktop/PHONEPE/pulse/df_map_user.csv")
for index, row in df3.iterrows():      
     query3="INSERT INTO Phone_Pe.district_map_Registered_user(State,Year,Quater,District,RegisteredUser) values(%s,%s,%s,%s,%s)"
     mycursor.execute(query3,(row.State,row.Year,row.Quater,row.District,row.RegisteredUser))
print('DataFrame Inserted successfully.')
phone_pe.commit()
#mycursor.close()

sql8 = 'CREATE TABLE if not exists DistrictT (MyIndex INT NOT NULL AUTO_INCREMENT,Year INT,Quater INT,District INT,Transaction_count BIGINT,Transaction_amount BIGINT,PRIMARY KEY (MyIndex))'

mycursor.execute(sql8) 
print('Table created successfully.')
phone_pe.commit()
df4=pd.read_csv(r"C:/Users/new/Desktop/PHONEPE/pulse/df_top_transaction.csv")
for index, row in df4.iterrows(): 
     df4["State"].drop    
     query4="INSERT INTO Phone_Pe.DistrictT(Year,Quater,District,Transaction_count,Transaction_amount) values(%s,%s,%s,%s,%s)"
     mycursor.execute(query4,(row.Year,row.Quater,row.District,row.Transaction_count,row.Transaction_amount))
print('DataFrame Inserted successfully.')
phone_pe.commit()
#mycursor.close()

#Creating table for District Latitude and Longitude:
sql7 ='CREATE TABLE if not exists Top_User(MyIndex INT NOT NULL AUTO_INCREMENT,State VARCHAR(100),Year INT,Quater INT,District VARCHAR(100),Registereduser BIGINT,PRIMARY KEY(MyIndex))'

mycursor.execute(sql7) 
print('Table created successfully.')
phone_pe.commit()
df5=pd.read_csv(r"C:/Users/new/Desktop/PHONEPE/pulse/df_top_user.csv")
for index, row in df5.iterrows():      
     quer5="INSERT INTO Phone_Pe.Top_User(State,Year,Quater,District,Registereduser) values(%s,%s,%s,%s,%s)"
     mycursor.execute(quer5,(row.State,row.Year,row.Quater,row.District,row.RegisteredUser))
print('DataFrame Inserted successfully.')
phone_pe.commit()
mycursor.close()