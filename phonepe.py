import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pandas as pd
import plotly.express as px
import requests
import json

#DataFrame Creation

#sql conection
mydb = sql.connect(host="localhost",
                    user="root",
                    password="Akshay@123",
                    database="phonepe"
                    )
cursor = mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT *FROM aggregated_insurance")
table1= cursor.fetchall()
Aggre_insurance=pd.DataFrame(table1,columns=("States","Years", "Quarter",
                                            "Transaction_type", "Transaction_count", "Transaction_amount"))

#aggre_transaction_df
cursor.execute("SELECT *FROM aggregated_transaction")
table1= cursor.fetchall()
Aggre_transaction=pd.DataFrame(table1,columns=("States","Years", "Quarter",
                                            "Transaction_type", "Transaction_count", "Transaction_amount"))


#aggre_user_df
cursor.execute("SELECT *FROM aggregated_user")
table1= cursor.fetchall()
Aggre_user=pd.DataFrame(table1,columns=("States","Years", "Quarter",
                                     "Brands", "Transaction_count", "Percentage"))

#map_insurance_df
cursor.execute("SELECT *FROM map_insurance")
table1= cursor.fetchall()
Map_insurance=pd.DataFrame(table1,columns=("States","Years", "Quarter",
                                            "Districts", "Transaction_count", "Transaction_amount"))


#map_transcation_df
cursor.execute("SELECT *FROM map_transaction")
table1= cursor.fetchall()
Map_transction=pd.DataFrame(table1,columns=("States","Years", "Quarter",
                                            "Districts", "Transaction_count", "Transaction_amount"))


#map_user_df
cursor.execute("SELECT *FROM map_user")
table1= cursor.fetchall()
Map_user=pd.DataFrame(table1,columns=("States","Years", "Quarter",
                                            "Districts", "RegisteredUsers", "AppOpens"))


#top_insurance_df
cursor.execute("SELECT *FROM top_insurance")
table1= cursor.fetchall()
Top_insurance=pd.DataFrame(table1,columns=("States","Years", "Quarter",
                                            "Pincodes", "Transaction_count", "Transaction_amount"))


#top_transaction_df
cursor.execute("SELECT *FROM top_transaction")
table1= cursor.fetchall()
Top_transaction=pd.DataFrame(table1,columns=("States","Years", "Quarter",
                                            "Pincodes", "Transaction_count", "Transaction_amount"))


#top_user_df
cursor.execute("SELECT *FROM top_user")
table1= cursor.fetchall()
Top_user=pd.DataFrame(table1,columns=("States","Years", "Quarter",
                                            "Pincodes", "RegisteredUsers"))

cursor.close()
mydb.commit()


def Transaction_amount_count_Y(df, year):
    

    tacy = df[df["Years"] == year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount",title=f"{year} TRANSACTION_AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount) 


    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count",title=f"{year} TRANSACTION_COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=650,width=600)
        st.plotly_chart(fig_count) 

    col1,col2 = st.columns(2)
    with col1:



        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM", 
                                    color= "Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color = (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name="States", title = f"{year} TRANSACTION AMOUNT", fitbounds = "locations",
                                                    height=600,width=600 )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM", 
                                    color= "Transaction_count",color_continuous_scale="Rainbow",
                                    range_color = (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name="States", title = f"{year} TRANSACTION COUNT", fitbounds = "locations",
                                                    height=600,width=600 )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df, quarter):

    tacy = df[df["Quarter"] == quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:


        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION_AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count = px.bar(tacyg, x="States", y="Transaction_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION_COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM", 
                                    color= "Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color = (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name="States", title = f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds = "locations",
                                                    height=600,width=600 )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:    

        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM", 
                                    color= "Transaction_count",color_continuous_scale="Rainbow",
                                    range_color = (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name="States", title = f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds = "locations",
                                                    height=600,width=600 )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy


def Aggre_Transaction_type(df,state):
    
    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame= tacyg, names="Transaction_type", values = "Transaction_amount",
                                width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame= tacyg, names="Transaction_type", values = "Transaction_count",
                                width=600, title=f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)

#Aggre_user_analysis_1
def Aggre_user_plot_1(df, year):

    aguy = df[df["Years"]==year]
    aguy.reset_index(drop= True, inplace =  True)


    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace = True)

    fig_bar_1 = px.bar(aguyg, x = "Brands", y ="Transaction_count", title = f"{year} BRANDS AND TRANSACTION COUNT",
                    width = 1000, color_discrete_sequence=px.colors.sequential.haline_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy
#Aggre_user_analysis_2
def Aggre_user_plot_2(df,quarter):
    aguyq = df[df["Quarter"]==quarter]
    aguyq.reset_index(drop= True, inplace =  True)
    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyqg, x = "Brands", y ="Transaction_count", title = f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                        width = 1000, color_discrete_sequence=px.colors.sequential.Magenta_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#Aggre_user_analysis_3
def Aggre_user_plot_3(df, state):
    auyqs = df[df["States"] == state]
    auyqs.reset_index(drop=True,inplace= True)

    fig_line_1= px.line(auyqs, x = "Brands", y= "Transaction_count", hover_data="Percentage",
                        title=f"{state.upper()} BRANDS, TRANSACTION COUNT,PERCENTAGE", width= 1000, markers = True)
    st.plotly_chart(fig_line_1)

#Map_insurance_district

def Map_insur_District(df,state):
    
    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tacyg, x = "Transaction_amount", y = "Districts", orientation= "h", height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 =px.bar(tacyg, x = "Transaction_amount", y = "Districts", orientation= "h", height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.matter_r)
        st.plotly_chart(fig_bar_2)


#map_user_plot_1
def map_use_plot_1(df,year):
    muy = df[df["Years"]==year]
    muy.reset_index(drop= True, inplace =  True)

    muyg = muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace = True)

    fig_line_1= px.line(muyg, x = "States", y= ["RegisteredUsers", "AppOpens"],
                            title= f"{year}  REGISTEREDUSER APPOPENS", width= 1000, markers = True)
    st.plotly_chart(fig_line_1)

    return muy

#map_user_plot_2
def map_use_plot_2(df,quarter):
    muyq = df[df["Quarter"]==quarter]
    muyq.reset_index(drop= True, inplace =  True)

    muyqg = muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace = True)
    fig_line_1= px.line(muyqg, x = "States", y= ["RegisteredUsers", "AppOpens"],
                            title= f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTEREDUSER APPOPENS", width= 1000,
                            markers= True, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq


#map_user_plot_3
def map_use_plot_3(df, states):
    muyqs = df[df["States"]==states]
    muyqs.reset_index(drop=True, inplace=True)

    if muyqs.empty:
        st.warning(f"No data available for the selected state: {states}")
        return None

    col1, col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x="RegisteredUsers", y="Districts", orientation="h",
                                    title=f"{states.upper()} REGISTERED USER", height=800, 
                                    color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2 = px.bar(muyqs, x="AppOpens", y="Districts", orientation="h",
                                    title=f"{states.upper()} APPOPENS", height=800, 
                                    color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

    return muyqs



#top_insurance_plot_1
def Top_insurance_plot_1(df,state):
    tiy= df[df["States"]==state]
    tiy.reset_index(drop= True, inplace =  True)

    tiyg = tiy.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    tiyg.reset_index(inplace = True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1 = px.bar(tiy, x = "Quarter", y = "Transaction_amount", hover_data="Pincodes",
                                    title="TRANSACTION AMOUNT", height= 650, width=600, color_discrete_sequence=px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:
        fig_top_insur_bar_2 = px.bar(tiy, x = "Quarter", y = "Transaction_count", hover_data="Pincodes",
                                    title="TRANSACTION COUNT", height= 650, width=600,color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)


#top_user_plot_1
def top_user_plot_1(df, year):
    tuy = df[df["Years"] == year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg = tuy.groupby(["States", "Years", "Quarter", "Pincodes"]).agg({'RegisteredUsers': 'sum'}).reset_index()

    fig_top_bar_1 = px.bar(tuyg, x="States", y="RegisteredUsers", color="Quarter", 
                           width=1000, height=800, color_discrete_sequence=px.colors.sequential.Burgyl, 
                           hover_name="Pincodes", title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_bar_1)

    return tuyg

#top_user_plot_2
def top_user_plot_2(df, state):
    tuys = df[df["States"]==state]
    tuys.reset_index(drop= True, inplace =  True)

    fig_top_plot_2 = px.bar(tuys, x = "Quarter", y = "RegisteredUsers",title = "REGISTREDUSERS,PINCODES,QUARTER",
                            width=1000,height=800,color="RegisteredUsers", hover_data="Pincodes",
                            color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)



#Streamlit Part

st.set_page_config(layout="wide")

st.title("PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION")
st.markdown("<h3 style='text-align: right;'>Akshay Kumar Adapa</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])  # Create columns with widths in the ratio 1:2:1
with col2:
    st.image("https://miro.medium.com/v2/resize:fit:496/1*1326fTEDmsXaGunZU11PaA.png", caption="Phonepe Logo", use_column_width=500)

select = st.selectbox("Main Menu", ["HOME", "DATA EXPLORATION & ANALYSIS"])

# Display content based on selection
if select == "HOME":
    st.header("Welcome to Phonepe Pulse Data Visualization and Exploration")
    st.write("This tool allows you to analyze and visualize data from the Phonepe Pulse GitHub repository.")

    st.header("Problem Statement")
    st.write("The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtaininsights and information that can be visualized in a user-friendly manner.")

    st.header("Solution Overview")
    st.write("Our solution is a user-friendly tool built using Streamlit and Plotly. It involves the following steps:")
    st.write("1. Extracting data from the Phonepe Pulse GitHub repository through scripting and cloning it.")
    st.write("2. Transforming the data into a suitable format and performing necessary cleaning and pre-processing.")
    st.write("3. Inserting the transformed data into a MySQL database for efficient storage and retrieval.")
    st.write("4. Creating an interactive dashboard using Streamlit and Plotly to visualize the data.")
    st.write("5. Fetching the data from the MySQL database to display in the dashboard.")
    st.write("6. Providing at least 10 different dropdown options for users to select different facts and figures to display on the dashboard.")

    st.header("Technologies Used")
    st.write("The following technologies were utilized in the project:")
    st.write("- GitHub Cloning")
    st.write("- Python")
    st.write("- Pandas")
    st.write("- MySQL")
    st.write("- mysql-connector-python")
    st.write("- Streamlit")
    st.write("- Plotly")

    st.header("Main Features")
    st.write("Key features of the tool include:")
    st.write("- Interactive Dashboard: Visualize data in an interactive and visually appealing manner.")
    st.write("- Data Retrieval: Fetch data from MySQL database for real-time visualization.")
    st.write("- Dropdown Options: Select different metrics and insights using dropdown menus.")

    st.header("User-Friendly Design")
    st.write("The tool is designed with user-friendliness in mind, featuring:")
    st.write("- Easy Navigation: Intuitive interface for effortless exploration.")
    st.write("- Clear Instructions: Guidance provided at every step for smooth user experience.")
    st.write("- Intuitive Controls: Simple controls for seamless interaction with the dashboard.")

    

elif select=="DATA EXPLORATION & ANALYSIS":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method1 = st.radio("Select The Method",["Aggregate Insurance","Aggregate Transaction", "Aggregate User"])

        if method1 == "Aggregate Insurance":

            col1,col2 = st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance, years)

            col1, col2 = st.columns(2)
            with col1:

                quarter=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarter)

        elif method1 == "Aggregate Transaction":
            
            col1,col2 = st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggre_tran_tac_Y["States"].unique())
            
            Aggre_Transaction_type(Aggre_tran_tac_Y,states)

            col1, col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["States"].unique())
            
            Aggre_Transaction_type(Aggre_tran_tac_Y_Q,states)

        elif method1 == "Aggregate User":

            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", Aggre_user["Years"].min(), Aggre_user["Years"].max(), Aggre_user["Years"].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)

            col1, col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())
            
            Aggre_user_plot_3(Aggre_user_Y_Q,states)




          
    with tab2:

        method2 = st.radio("Select The Method",["Map Insurance","Map Transaction", "Map User"])

        if method2 == "Map Insurance":

            col1,col2 = st.columns(2)
            with col1:

                years=st.slider("Select The Year (Map Insurance)",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            Map_insurance_tac_Y=Transaction_amount_count_Y(Map_insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State (Map Insurance)", Map_insurance_tac_Y["States"].unique())
            
            Map_insur_District(Map_insurance_tac_Y,states)

            col1, col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter (Map Insurance)",Map_insurance_tac_Y["Quarter"].min(),Map_insurance_tac_Y["Quarter"].max(),Map_insurance_tac_Y["Quarter"].min())
            Map_insurance_tac_Y_Q = Transaction_amount_count_Y_Q(Map_insurance_tac_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State (Map Insurance by Quarter)", Map_insurance_tac_Y_Q["States"].unique())
            
            Map_insur_District(Map_insurance_tac_Y_Q,states)



        elif method2 == "Map Transaction":
        
            col1,col2 = st.columns(2)
            with col1:

                years=st.slider("Select The Year (Map Transaction)",Map_transction["Years"].min(),Map_transction["Years"].max(),Map_transction["Years"].min())
            Map_tran_tac_Y=Transaction_amount_count_Y(Map_transction, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State (Map Transaction)", Map_tran_tac_Y["States"].unique())
            
            Map_insur_District(Map_tran_tac_Y,states)

            col1, col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter (Map Transaction)",Map_tran_tac_Y["Quarter"].min(),Map_tran_tac_Y["Quarter"].max(),Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Map_tran_tac_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State (Map Transaction by Quarter)", Map_tran_tac_Y_Q["States"].unique())
            
            Map_insur_District(Map_tran_tac_Y_Q,states)


        elif method2 == "Map User":
           
            col1,col2 = st.columns(2)
            with col1:

                years=st.slider("Select The Year (Map User)",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            Map_user_Y=map_use_plot_1(Map_user, years)

            col1, col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter (Map User)",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_Y_Q = map_use_plot_2(Map_user_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State (Map User)", Map_user_Y_Q["States"].unique())
            
            map_use_plot_3(Map_user_Y_Q,states)


    with tab3:

        method3 = st.radio("Select The Method",["Top Insurance","Top Transaction", "Top User"])

        if method3 == "Top Insurance":
            col1,col2 = st.columns(2)
            with col1:

                years=st.slider("Select The Year (Top Insurance)",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            Top_insur_tac_Y=Transaction_amount_count_Y(Top_insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State (Top Insurance)", Top_insur_tac_Y["States"].unique())
            
            Top_insurance_plot_1(Top_insur_tac_Y,states)

            col1, col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter (Top Insurance)",Top_insur_tac_Y["Quarter"].min(),Top_insur_tac_Y["Quarter"].max(),Top_insur_tac_Y["Quarter"].min())
            Top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(Top_insur_tac_Y, quarters)



        elif method3 == "Top Transaction":
            col1,col2 = st.columns(2)
            with col1:

                years=st.slider("Select The Year (Top Transaction)",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            Top_tran_tac_Y=Transaction_amount_count_Y(Top_transaction, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State (Top Transaction)", Top_tran_tac_Y["States"].unique())
            
            Top_insurance_plot_1(Top_tran_tac_Y,states)

            col1, col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter (Top Transcation)",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Top_tran_tac_Y, quarters)


        elif method3 == "Top User":
            col1,col2 = st.columns(2)
            with col1:

                years=st.slider("Select The Year (Top User)",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_tac_Y=top_user_plot_1(Top_user, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State (Top User)", Top_user_tac_Y["States"].unique())
            
            top_user_plot_2(Top_user_tac_Y,states)



