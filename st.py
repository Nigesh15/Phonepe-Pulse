import mysql.connector
import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt 
import json
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.io as pio

pio.renderers.default = 'browser'

phone_pe=mysql.connector.connect(host='localhost',
                        database='phone_pe',
                        user='root',
                        password='*****') #your password
mycursor = phone_pe.cursor(buffered=True)
#Streamlit
st.set_page_config(page_title = "PhonePe",layout="wide")

st.title("PHONEPE PULSE")
#st.subheader('Aggrigate Transaction')

Year = st.selectbox(
    'Kindly Select The Year:',
    ('2018','2019','2020','2021','2022'))
st.write('You selected:',Year)

Quater = st.selectbox(
    'Kindly Select The Quarter:',
    ('1','2','3','4'))
st.write('You selected:',Year) 

Details = st.selectbox(
    'Kindly Select The Required Details:',
    (
    'Aggregated Transaction',
     'Top Users',
     'Registered Users'))
st.write('You selected:',Details)

display_values = {
    "Aggregated Transaction" : {
        "table_name": "ATransaction",
        "color": "Transaction_count",
        "hover_name": "State",
        "hover_data": "Transaction_amount",
        "title": "India phonepe Transaction"
    },
    
    "Registered Users" : {
        "table_name": "district_map_registered_user",
        "color": "RegisteredUser",
        "hover_name": "State",
        "hover_data": "RegisteredUser",
        "title": "India phonepe Map Registerd Users"
    },
    "Top Users" : {
        "table_name": "top_user",
        "color": "Registereduser",
        "hover_name": "State",
        "hover_data": "Registereduser",
        "title": "India phonepe Map Top Users"
    }
    
}

def displayDetails(Details):
    mycursor.execute(f"select * from {display_values[Details]['table_name']} where Year={Year} and Quater={Quater}")
    response=mycursor.fetchall()
    phone_pe.commit()
    #mycursor.close()
    
    india_states = json.load(open("C:/Users/new/Desktop/PHONEPE/pulse/states_india.geojson", "r"))
    state_id_map = {}
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]
       
    df = pd.DataFrame(response)

    mycursor.execute(f"show columns from {display_values[Details]['table_name']};")
    columns = mycursor.fetchall()
    column_names = [details[0] for details in columns]
    print(column_names)

    df.columns = column_names
    df['State']=df['State'].replace({'telangana':'Telangana', 
                                         'andaman-&-nicobar-islands':'Andaman & Nicobar Island',
                                        'andhra-pradesh':'Andhra Pradesh',
                                        'arunachal-pradesh':'Arunanchal Pradesh', 
                                        'assam':'Assam', 
                                        'bihar':'Bihar', 
                                        'chhattisgarh' :'Chhattisgarh', 
                                        'dadra-&-nagar-haveli-&-daman-&-diu':'Daman & Diu', 
                                        'goa':'Goa', 
                                        'gujarat':'Gujarat', 
                                        'haryana':'Haryana',
                                        'himachal-pradesh':'Himachal Pradesh', 
                                        'jammu-&-kashmir':'Jammu & Kashmir', 
                                        'jharkhand':'Jharkhand',
                                        'karnataka':'Karnataka', 
                                        'kerala':'Kerala', 
                                        'lakshadweep':'Lakshadweep', 
                                        'madhya-pradesh':'Madhya Pradesh', 
                                        'maharashtra':'Maharashtra', 
                                        'manipur':'Manipur', 
                                        'chandigarh':'Chandigarh', 
                                        'puducherry':'Puducherry', 
                                        'punjab':'Punjab', 
                                        'rajasthan':'Rajasthan', 
                                        'sikkim':'Sikkim', 
                                        'tamil-nadu':'Tamil Nadu', 
                                        'tripura':	'Tripura', 
                                        'uttar-pradesh':'Uttar Pradesh', 
                                        'uttarakhand':'Uttarakhand', 
                                        'west-bengal':'West Bengal', 
                                        'odisha':'Odisha', 
                                        'dadra-&-nagar-haveli-&-daman-&-diu':'Dadara & Nagar Havelli', 
                                        'meghalaya':'Meghalaya', 
                                        'mizoram': 'Mizoram', 
                                        'nagaland':'Nagaland',
                                        'ladakh':'Jammu & Kashmir',
                                        'delhi':'NCT of Delhi'} )
    df["id"] = df["State"].apply(lambda x: state_id_map[x])



        
    fig = px.choropleth(df,
                     locations="id",
                     
                     geojson=india_states,
                     # color="Transaction_count",
                     color = display_values[Details]["color"],
                     hover_name=display_values[Details]["hover_name"],
                     hover_data=[display_values[Details]["hover_data"]],
                     title=display_values[Details]["title"],
                     color_continuous_scale=[[0, 'rgb(240,240,240)'],
                                    [0.25, 'rgb(13,136,198)'],
                                    [0.5, 'rgb(191,247,202)'],
                                    [0.75, 'rgb(4,145,32)'],
                                    [1, 'rgb(227,26,28,0.5)']])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.show() 

displayDetails(Details)

# if Details == 'Aggregated_Transaction':
#     mycursor.execute(f"select * from ATransaction where Year={Year} and Quater={Quater}")
#     Aggregated_Transaction=mycursor.fetchall()
#     phone_pe.commit()
#     #mycursor.close()
    
#     india_states = json.load(open("C:/Users/new/Desktop/PHONEPE/pulse/states_india.geojson", "r"))
#     state_id_map = {}
#     for feature in india_states["features"]:
#         feature["id"] = feature["properties"]["state_code"]
#         state_id_map[feature["properties"]["st_nm"]] = feature["id"]
       
#     df = pd.DataFrame(Aggregated_Transaction)
#     df.columns = ["id", "State", "Year", "Quater", "Transaction_type", "Transaction_count", "Transaction_amount"]
#     df['State']=df['State'].replace({'telangana':'Telangana', 
#                                          'andaman-&-nicobar-islands':'Andaman & Nicobar Island',
#                                         'andhra-pradesh':'Andhra Pradesh',
#                                         'arunachal-pradesh':'Arunanchal Pradesh', 
#                                         'assam':'Assam', 
#                                         'bihar':'Bihar', 
#                                         'chhattisgarh' :'Chhattisgarh', 
#                                         'dadra-&-nagar-haveli-&-daman-&-diu':'Daman & Diu', 
#                                         'goa':'Goa', 
#                                         'gujarat':'Gujarat', 
#                                         'haryana':'Haryana',
#                                         'himachal-pradesh':'Himachal Pradesh', 
#                                         'jammu-&-kashmir':'Jammu & Kashmir', 
#                                         'jharkhand':'Jharkhand',
#                                         'karnataka':'Karnataka', 
#                                         'kerala':'Kerala', 
#                                         'lakshadweep':'Lakshadweep', 
#                                         'madhya-pradesh':'Madhya Pradesh', 
#                                         'maharashtra':'Maharashtra', 
#                                         'manipur':'Manipur', 
#                                         'chandigarh':'Chandigarh', 
#                                         'puducherry':'Puducherry', 
#                                         'punjab':'Punjab', 
#                                         'rajasthan':'Rajasthan', 
#                                         'sikkim':'Sikkim', 
#                                         'tamil-nadu':'Tamil Nadu', 
#                                         'tripura':	'Tripura', 
#                                         'uttar-pradesh':'Uttar Pradesh', 
#                                         'uttarakhand':'Uttarakhand', 
#                                         'west-bengal':'West Bengal', 
#                                         'odisha':'Odisha', 
#                                         'dadra-&-nagar-haveli-&-daman-&-diu':'Dadara & Nagar Havelli', 
#                                         'meghalaya':'Meghalaya', 
#                                         'mizoram': 'Mizoram', 
#                                         'nagaland':'Nagaland',
#                                         'ladakh':'Jammu & Kashmir',
#                                         'delhi':'NCT of Delhi'} )
#     df["id"] = df["State"].apply(lambda x: state_id_map[x])



        
#     fig = px.choropleth(df,
#                      locations="id",
                     
#                      geojson=india_states,
#                      # color="Transaction_count",
#                      color = chloropeth_values[Details]["color"]
#                      hover_name="State",
#                      hover_data=["Transaction_amount"],
#                     title="India phonepe Transaction",
#                      color_continuous_scale=[[0, 'rgb(240,240,240)'],
#                                     [0.25, 'rgb(13,136,198)'],
#                                     [0.5, 'rgb(191,247,202)'],
#                                     [0.75, 'rgb(4,145,32)'],
#                                     [1, 'rgb(227,26,28,0.5)']])
#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.show() 
                
    
# elif Details == 'Mobile_Brand_Users:':
#     mycursor.execute(f"select * from district_map_registered_user where Year={Year} and Quater={Quater}")
#     Mobile_Brand_Users = mycursor.fetchall()
#     phone_pe.commit()
#     mycursor.close()
    
#     india_states = json.load(open("C:/Users/new/Desktop/PHONEPE/pulse/states_india.geojson", "r"))
#     state_id_map = {}
#     for feature in india_states["features"]:
#         feature["id"] = feature["properties"]["state_code"]
#         state_id_map[feature["properties"]["st_nm"]] = feature["id"]
       
#     df1 = pd.DataFrame(Mobile_Brand_Users)
#     df1.columns = ["id", "State", "Year", "Quater", "District","Registereduser"]
#     df1['State']=df1['State'].replace({'telangana':'Telangana', 
#                                          'andaman-&-nicobar-islands':'Andaman & Nicobar Island',
#                                         'andhra-pradesh':'Andhra Pradesh',
#                                         'arunachal-pradesh':'Arunanchal Pradesh', 
#                                         'assam':'Assam', 
#                                         'bihar':'Bihar', 
#                                         'chhattisgarh' :'Chhattisgarh', 
#                                         'dadra-&-nagar-haveli-&-daman-&-diu':'Daman & Diu', 
#                                         'goa':'Goa', 
#                                         'gujarat':'Gujarat', 
#                                         'haryana':'Haryana',
#                                         'himachal-pradesh':'Himachal Pradesh', 
#                                         'jammu-&-kashmir':'Jammu & Kashmir', 
#                                         'jharkhand':'Jharkhand',
#                                         'karnataka':'Karnataka', 
#                                         'kerala':'Kerala', 
#                                         'lakshadweep':'Lakshadweep', 
#                                         'madhya-pradesh':'Madhya Pradesh', 
#                                         'maharashtra':'Maharashtra', 
#                                         'manipur':'Manipur', 
#                                         'chandigarh':'Chandigarh', 
#                                         'puducherry':'Puducherry', 
#                                         'punjab':'Punjab', 
#                                         'rajasthan':'Rajasthan', 
#                                         'sikkim':'Sikkim', 
#                                         'tamil-nadu':'Tamil Nadu', 
#                                         'tripura':	'Tripura', 
#                                         'uttar-pradesh':'Uttar Pradesh', 
#                                         'uttarakhand':'Uttarakhand', 
#                                         'west-bengal':'West Bengal', 
#                                         'odisha':'Odisha', 
#                                         'dadra-&-nagar-haveli-&-daman-&-diu':'Dadara & Nagar Havelli', 
#                                         'meghalaya':'Meghalaya', 
#                                         'mizoram': 'Mizoram', 
#                                         'nagaland':'Nagaland',
#                                         'ladakh':'Jammu & Kashmir',
#                                         'delhi':'NCT of Delhi'} )
#     df1["id"] = df1["State"].apply(lambda x: state_id_map[x])



        
#     fig = px.choropleth(df1,
#                      locations="id",
                     
#                      geojson=india_states,
#                      color="Registereduser",
#                      hover_name="State",
#                      hover_data=["Registereduser"],
#                     title="India phonepe Map Transaction",
#                      color_continuous_scale=[[0, 'rgb(240,240,240)'],
#                                     [0.25, 'rgb(13,136,198)'],
#                                     [0.5, 'rgb(191,247,202)'],
#                                     [0.75, 'rgb(4,145,32)'],
#                                     [1, 'rgb(227,26,28,0.5)']])
#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.show() 

#     #mycursor.close()
# # print(Agg_Transaction)



#elif Details == 'Mobile_Brand_Users':

#mycursor.execute(f'select * from agg_userbydevice where Year = {Year},Quater={Quater}, brands,Count,Percentage')
 #   Mobile_Brand_Users=mycursor.fetchall
  #  phone_pe.commit()
  #  mycursor.close()
# mycursor.execute('select * from district_maptransaction')
# District_Transaction=mycursor.fetchall
# mycursor.execute('select * from district_map_Registered_user')
# District_Map_Registered_user=mycursor.fetchall
# mycursor.execute('select * from State_LL')
# State_LL=mycursor.fetchall
# mycursor.execute('select * from District_LL')
# District_LL=mycursor.fetchall


# india_states = json.load(open("C:/Users/new/Desktop/PHONEPE/pulse/states_india.geojson", "r"))

# state_id_map = {}
# for feature in india_states["features"]:
#     feature["id"] = feature["properties"]["state_code"]
#     state_id_map[feature["properties"]["st_nm"]] = feature["id"]
# #df = pd.read_json('states_india.geojson')

# df = pd.DataFrame(Aggregated_Transaction)
# df.columns = ["id", "State", "Year", "Quater", "Transaction_type", "Transaction_count", "Transaction_amount"]
# # df['State'].drop('ladakh')
# df['State']=df['State'].replace({'telangana':'Telangana', 
#  'andaman-&-nicobar-islands':'Andaman & Nicobar Island',
#  'andhra-pradesh':'Andhra Pradesh',
#  'arunachal-pradesh':'Arunanchal Pradesh', 
#  'assam':'Assam', 
#  'bihar':'Bihar', 
#  'chhattisgarh' :'Chhattisgarh', 
#  'dadra-&-nagar-haveli-&-daman-&-diu':'Daman & Diu', 
#  'goa':'Goa', 
#  'gujarat':'Gujarat', 
#  'haryana':'Haryana',
#  'himachal-pradesh':'Himachal Pradesh', 
#  'jammu-&-kashmir':'Jammu & Kashmir', 
#  'jharkhand':'Jharkhand',
#  'karnataka':'Karnataka', 
#  'kerala':'Kerala', 
#  'lakshadweep':'Lakshadweep', 
#  'madhya-pradesh':'Madhya Pradesh', 
#  'maharashtra':'Maharashtra', 
#  'manipur':'Manipur', 
#  'chandigarh':'Chandigarh', 
#  'puducherry':'Puducherry', 
#  'punjab':'Punjab', 
#  'rajasthan':'Rajasthan', 
#  'sikkim':'Sikkim', 
#  'tamil-nadu':'Tamil Nadu', 
#  'tripura':	'Tripura', 
#  'uttar-pradesh':'Uttar Pradesh', 
#  'uttarakhand':'Uttarakhand', 
#  'west-bengal':'West Bengal', 
#  'odisha':'Odisha', 
#  'dadra-&-nagar-haveli-&-daman-&-diu':'Dadara & Nagar Havelli', 
#  'meghalaya':'Meghalaya', 
#  'mizoram': 'Mizoram', 
#  'nagaland':'Nagaland',
#  'ladakh':'Jammu & Kashmir',
#  'delhi':'NCT of Delhi'} )
# # print(df[:5])
# df["id"] = df["State"].apply(lambda x: state_id_map[x])



#  fig = px.choropleth(df,
#                      locations="id",
                     
#                      geojson=india_states,
#                     color="Transaction_count",
#                     hover_name="State",
#                     hover_data=["Transaction_amount"],
#                     title="India phonepe Transaction",
#                     color_continuous_scale=[[0, 'rgb(240,240,240)'],
#                                     [0.25, 'rgb(13,136,198)'],
#                                     [0.5, 'rgb(191,247,202)'],
#                                     [0.75, 'rgb(4,145,32)'],
#                                     [1, 'rgb(227,26,28,0.5)']])
#                 fig.update_geos(fitbounds="locations", visible=False)
#                 fig.show() 
   

# # st.title('PHONEPE PULSE')
# # st.subheader('Aggrigate Transaction')
# # st.slider('Year',2018,2019,2020,2021,2022)
# # st.slider('Quarter',1,2,3,4)
