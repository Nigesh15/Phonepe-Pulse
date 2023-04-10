import mysql.connector
import pandas as pd
import json
import streamlit as st
import plotly.express as px
import plotly.io as pio
from decimal import Decimal

pio.renderers.default = 'browser'

phone_pe=mysql.connector.connect(host='localhost',
                        database='phone_pe',
                        user='root',
                        password='V!vin2812')#Your password
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
st.write('1=January to March')
st.write('2=April to June')
st.write('3=July to September')
st.write('4 =October to December')
st.write('You selected:',Quater) 

Type = st.selectbox(
    'Kindly select the Payment:',
    ('Recharge & bill payments','Peer-to-peer payments','Merchant payments','Financial Services','Others'))
st.write('You selected:',Type) 


Details = st.selectbox(
    'Kindly Select The Required Details:',
    (
    'Aggregated Transaction',
     'Top Users',
     'Registered Users'))

st.write('You selected:',Details)

# Type = st.selectbox(
#     'Kindly select the Type of Payment:',
#     ('Recharge & bill payments','Peer-to-peer payments','Merchant payments','Financial Services','Others'))

display_values = {
    "Aggregated Transaction" : {
        "table_name": "ATransaction",
        # "color": "Transaction_count",
        "color": "Transaction_amount",
        "hover_name": "State",
        # "hover_data":"",
        "hover_data": "Transaction_type",
        # "hover_data":f"{Type}"
        # "facet_row":"Type",        
        # "hover_data":"Quater",
        # "hover_data":"Year",
        "title": "India phonepe Transaction"
    },  
    
    "Registered Users" : {
        "table_name": "district_map_registered_user",
        "color": "id",
        "hover_name": "State",
        "hover_data": "RegisteredUserSum",
        # "hover_data": "Quater",
        # "custom_data":"Quater",
        "title": "India phonepe Map Registerd Users"
    },
    "Top Users" : {
        "table_name": "top_user",
        "color": "Registereduser",
        "hover_name": "State",
        "hover_data": "Quater",
        # "custom_data":"Quater",
        "title": "India phonepe Map Top Users"
    }
    
}

# mycursor.execute(f"select * from {display_values[Details]['table_name']} where Year={Year} and Transaction_type={Type} ")
if Details == "Aggregated Transaction":
    mycursor.execute(f"select * from {display_values[Details]['table_name']} where Year={Year} and Quater={Quater} and Transaction_type='{Type}'")
elif Details == "Registered Users":
    # mycursor.execute(f"select State,Year,Quater,District, SUM(RegisteredUser) as RegisteredUserSum from {display_values[Details]['table_name']} where Year={Year} and Quater={Quater} GROUP BY State")
    mycursor.execute(f"select State,Year,Quater,SUM(RegisteredUser) as RegisteredUserSum from {display_values[Details]['table_name']} where Year={Year} and Quater={Quater} Group By State, Year, Quater")

response=mycursor.fetchall()
phone_pe.commit()
response_list = []
if Details == "Registered Users":
    print("registered")
    response_list = [list(x) for x in response]
    for index, r in enumerate(response_list):
        if type(r[-1]) == Decimal:
            response_list[index] = [r[0], r[1], r[2], int(r[3])]
    respones = response_list
            
print(response_list)
# print(response_list)

india_states = json.load(open("C:/Users/new/Desktop/PHONEPE/pulse/states_india.geojson", "r"))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]
    
df = pd.DataFrame(response)

mycursor.execute(f"show columns from {display_values[Details]['table_name']};")
columns = mycursor.fetchall()
column_names = [details[0] for details in columns]
if Details == "Registered Users":
    column_names.remove("MyIndex")
    column_names.remove("RegisteredUser")
    column_names.remove("District")
    column_names.append("RegisteredUserSum")
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

print("Test2")
print(display_values[Details]["hover_data"])

print(df)
    
fig = px.choropleth(df,
                    locations="id",
                    
                    geojson=india_states,
                    # color="Transaction_count",
                    color = display_values[Details]["color"],
                    hover_name=display_values[Details]["hover_name"],
                    hover_data=[display_values[Details]["hover_data"]],
                #  facet_row=display_values[Details]["facet_row"],
                    title=display_values[Details]["title"],
                #  custom_data=[display_values[Details]["custom_data"]],
                #  color_continuous_scale=[[0, 'rgb(240,240,240)'],
                #                 [0.25, 'rgb(13,136,198)'],
                #                 [0.5, 'rgb(191,247,202)'],
                #                 [0.75, 'rgb(4,145,32)'],
                #                 [1, 'rgb(227,26,28,0.5)']]
                )
print("Test3")
fig.update_geos(fitbounds="locations", visible=False)
# fig.show() 
print("Test4")

st.plotly_chart(fig,theme=None, use_container_width=True)

print("Test5")
