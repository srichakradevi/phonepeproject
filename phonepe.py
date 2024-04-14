import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import requests
import json
from PIL import Image
import mysql.connector
import pandas as pd

#creating the dataframe
#establish the connection to mysql
connection_mysql = mysql.connector.connect(host="localhost",user="root",password="12345",database="phonepe_data")
mycursor_mysql = connection_mysql.cursor()

#dataframe of aggregated transaction
mycursor_mysql.execute("SELECT *FROM aggregated_transaction")
table1=mycursor_mysql.fetchall()

Aggre_transaction=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))


#dataframe of aggregated user
mycursor_mysql.execute("SELECT * FROM aggregated_user")
table2=mycursor_mysql.fetchall()

Aggre_user=pd.DataFrame(table2,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))


#dataframe for map transaction
mycursor_mysql.execute("SELECT *FROM map_transaction")
table3=mycursor_mysql.fetchall()

Map_transaction=pd.DataFrame(table3,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))


#dataframe for map user
mycursor_mysql.execute("SELECT * FROM map_user")
table4=mycursor_mysql.fetchall()

Map_user=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","RegisteredUsers","AppOpens"))


#dataframe for top transaction
mycursor_mysql.execute("SELECT *FROM top_transaction")
table5=mycursor_mysql.fetchall()

Top_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))


#dataframe for top user
mycursor_mysql.execute("SELECT * FROM top_user")
table6=mycursor_mysql.fetchall()

Top_user=pd.DataFrame(table6,columns=("States","Years","Quarter","Pincodes","RegisteredUsers"))


def Transaction_amount_count_Y(df,year):
    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)
        
    with col2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_count)
    
    col1,col2=st.columns(2)
    
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
        
    states_name.sort()
    with col1:
        fig_india_1=px.choropleth(tacyg, geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="temps",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        
        fig_india_1.update_geos(visible=False)
    
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States",title=f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        
        fig_india_2.update_geos(visible=False)
        
        st.plotly_chart(fig_india_2) 
    return tacy
        
        
def Transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_count)
    
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
        
    states_name.sort()
    col1,col2=st.columns(2)
    with col1:
        fig_india_1=px.choropleth(tacyg, geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="temps",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        
        fig_india_1.update_geos(visible=False)
        
        st.plotly_chart(fig_india_1)
    with col2:   
        fig_india_2=px.choropleth(tacyg, geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        
        fig_india_2.update_geos(visible=False)
        
        st.plotly_chart(fig_india_2)
        
    return tacy
    
def Aggre_Tran_Transaction_type(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True, inplace=True)
    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_amount",width=600,
                        title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.2)
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_count",width=600,
                        title=f"{state.upper()} TRANSACTION COUNT",hole=0.2)
        st.plotly_chart(fig_pie_2)

def Aggre_user_plot_1(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace=True)
    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)
    fig_bar_1=px.bar(aguyg,x="Brands",y="Transaction_count",title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=800,color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    return aguy

#aggregated user analysis based on quarter
def Aggre_user_plot_2(df,quarter):
    aguyq=df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True, inplace=True)
    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyqg,x="Brands",y="Transaction_count",title=f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                        width=800,color_discrete_sequence=px.colors.sequential.haline)
    st.plotly_chart(fig_bar_1)
    return aguyq
    
 
def Aggre_user_plot_3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True,inplace=True)


    fig_line_1=px.bar(auyqs,y="Brands",x="Transaction_count",hover_data="Percentage",orientation='h',
                    title=f"{state.upper()} BRANDS, TRANSACTION COUNT AND PERCENTAGE",width=1000,height=650)
    st.plotly_chart(fig_line_1)
    
    
def Map_Tran_Districts(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True, inplace=True)
    
    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(tacyg,y="Transaction_amount",x="Districts",width=300,height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(tacyg,x="Districts",y="Transaction_count",width=300,height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Emrld)
        st.plotly_chart(fig_bar_2)
        
#Map_User_plot_1
def map_user_plot_1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True, inplace=True)

    muyg=muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg,x="States",y=["RegisteredUsers", "AppOpens"],
                    title=f"{year} REGISTERED USER, APPOPENS",width=1000, height=800, markers=True)
    st.plotly_chart(fig_line_1)
    
    return muy

#Map_User_plot_2
def map_user_plot_2(df,quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg=muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(muyqg,x="States",y=["RegisteredUsers", "AppOpens"],
                    title=f"{df['Years'].min()}YEAR {quarter}QUARTER REGISTERED USER, APPOPENS",width=1000, height=800, markers=True,
                    color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)
    
    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs=df[df["States"]==states]
    muyqs.reset_index(drop=True, inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar_1=px.bar(muyqs, x="RegisteredUsers", y="Districts", title=f"{states.upper()} REGISTERED USER", 
                                  height=800, orientation="h",color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)
    with col2:
        fig_map_user_bar_2=px.bar(muyqs, x="AppOpens", y="Districts", title=f"{states.upper()} APPOPENS", 
                                  height=800,orientation="h",color_discrete_sequence=px.colors.sequential.Emrld_r)
        st.plotly_chart(fig_map_user_bar_2)
        
# Top_transaction_plot_1
def Top_tran_plot_1(df,states):
    tty=df[df["States"]=="West Bengal"]
    tty.reset_index(drop=True, inplace=True)

    ttyg=tty.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    ttyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_top_tran_bar_1=px.bar(tty, x="Quarter", y="Transaction_amount",hover_data="Pincodes",
                                title="TRANSACTION AMOUNT", height=800, color_discrete_sequence=px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_tran_bar_1)
    with col2:
        fig_top_tran_bar_2=px.bar(tty, x="Quarter", y="Transaction_count",hover_data="Pincodes",
                                title="TRANSACTION COUNT", height=800, color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_top_tran_bar_2)
            
#top user plot 1
def top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg, x="States", y="RegisteredUsers", color="Quarter", width=1000, height=800,
                        color_discrete_sequence=px.colors.sequential.algae_r, hover_name="States",
                        title=f"{year} REGISTERED USER")
    st.plotly_chart(fig_top_plot_1)
    return tuy

# top user plot 2
def top_user_plot_2(df,state):
    tuys=df[df["States"]==state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2=px.bar(tuys,x="Quarter", y="RegisteredUsers", title="REGISTERED USER, PINCODES, QUARTER",
                        width=1000, height=800, color="RegisteredUsers", hover_data="Pincodes",
                        color_continuous_scale= px.colors.sequential.Blugrn)
    st.plotly_chart(fig_top_plot_2)


def top_chart_transaction_amount(table_name):

    #establish the connection to mysql
    connection_mysql = mysql.connector.connect(host="localhost",user="root",password="12345",database="phonepe_data")
    mycursor_mysql = connection_mysql.cursor()
    # plot query1
    query1=f'''select States, SUM(Transaction_amount) as Transaction_amount
                        from {table_name}
                        group by States
                        order by Transaction_amount desc
                        limit 10;'''
    mycursor_mysql.execute(query1)
    table_1=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_1=pd.DataFrame(table_1,columns=("States", "Transaction_amount"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1,x="States",y="Transaction_amount",title="TRANSACTION AMOUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount_1)


    #plot query2
    query2=f'''select States, SUM(Transaction_amount) as Transaction_amount
                        from {table_name}
                        group by States
                        order by Transaction_amount 
                        limit 10;'''
    mycursor_mysql.execute(query2)
    table_2=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_2=pd.DataFrame(table_2,columns=("States", "Transaction_amount"))
    with col2:
        fig_amount_2=px.bar(df_2,x="States",y="Transaction_amount",title="TRANSACTION AMOUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)



    #plot query3
    query3=f'''select States, AVG(Transaction_amount) as Transaction_amount
                        from {table_name}
                        group by States
                        order by Transaction_amount;'''
    mycursor_mysql.execute(query3)
    table_3=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_3=pd.DataFrame(table_3,columns=("States", "Transaction_amount"))

    fig_amount_3=px.bar(df_3,y="States",x="Transaction_amount",title="AVERAGE OF TRANSACTION AMOUNT", hover_name="States", orientation="h",
                    color_discrete_sequence=px.colors.sequential.BuGn_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)


def top_chart_transaction_count(table_name):

    #establish the connection to mysql
    connection_mysql = mysql.connector.connect(host="localhost",user="root",password="12345",database="phonepe_data")
    mycursor_mysql = connection_mysql.cursor()
    # plot query1
    query1=f'''select States, SUM(Transaction_count) as Transaction_count
                        from {table_name}
                        group by States
                        order by Transaction_count desc
                        limit 10;'''
    mycursor_mysql.execute(query1)
    table_1=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_1=pd.DataFrame(table_1,columns=("States", "Transaction_count"))
    col1,col2=st.columns(2)
    with col1:

        fig_amount_1=px.bar(df_1,x="States",y="Transaction_count",title="TRANSACTION COUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount_1)


    #plot query2
    query2=f'''select States, SUM(Transaction_count) as Transaction_count
                        from {table_name}
                        group by States
                        order by Transaction_count 
                        limit 10;'''
    mycursor_mysql.execute(query2)
    table_2=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_2=pd.DataFrame(table_2,columns=("States", "Transaction_count"))
    with col2:

        fig_amount_2=px.bar(df_2,x="States",y="Transaction_count",title="TRANSACTION COUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)



    #plot query3
    query3=f'''select States, AVG(Transaction_count) as Transaction_count
                        from {table_name}
                        group by States
                        order by Transaction_count;'''
    mycursor_mysql.execute(query3)
    table_3=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_3=pd.DataFrame(table_3,columns=("States", "Transaction_count"))

    fig_amount_3=px.bar(df_3,y="States",x="Transaction_count",title="AVERAGE OF TRANSACTION COUNT", hover_name="States", orientation="h",
                    color_discrete_sequence=px.colors.sequential.BuGn_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)
    

def top_chart_registered_user(table_name,state):

    #establish the connection to mysql
    connection_mysql = mysql.connector.connect(host="localhost",user="root",password="12345",database="phonepe_data")
    mycursor_mysql = connection_mysql.cursor()
    # plot query1
    query1=f'''select Districts, SUM(RegisteredUsers) as RegisteredUsers
                        from {table_name}
                        where States='{state}'
                        group by Districts
                        order by RegisteredUsers;'''
    mycursor_mysql.execute(query1)
    table_1=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_1=pd.DataFrame(table_1,columns=("Districts", "RegisteredUsers"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1,x="Districts",y="RegisteredUsers",title="REGISTERED USERS", hover_name="Districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=500)
        st.plotly_chart(fig_amount_1)

    #plot query2
    query2=f'''select Districts, AVG(RegisteredUsers) as RegisteredUsers
                        from {table_name}
                        where States='{state}'
                        group by Districts
                        order by RegisteredUsers ;'''
    mycursor_mysql.execute(query2)
    table_2=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_2=pd.DataFrame(table_2,columns=("Districts", "RegisteredUsers"))
    with col2:
        fig_amount_2=px.bar(df_2,y="Districts",x="RegisteredUsers",title="AVERAGE OF REGISTERED USER", hover_name="Districts", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=500)
        st.plotly_chart(fig_amount_2)

def top_chart_appopens(table_name,state):

    #establish the connection to mysql
    connection_mysql = mysql.connector.connect(host="localhost",user="root",password="12345",database="phonepe_data")
    mycursor_mysql = connection_mysql.cursor()
    # plot query1
    query1=f'''select Districts, SUM(AppOpens) as AppOpens
                        from {table_name}
                        where States='{state}'
                        group by Districts
                        order by AppOpens;'''
    mycursor_mysql.execute(query1)
    table_1=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_1=pd.DataFrame(table_1,columns=("Districts", "AppOpens"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1,x="Districts",y="AppOpens",title="APPOPENS", hover_name="Districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=500)
        st.plotly_chart(fig_amount_1)

    #plot query2
    query2=f'''select Districts, AVG(AppOpens) as AppOpens
                        from {table_name}
                        where States='{state}'
                        group by Districts
                        order by AppOpens ;'''
    mycursor_mysql.execute(query2)
    table_2=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_2=pd.DataFrame(table_2,columns=("Districts", "AppOpens"))
    with col2:
        fig_amount_2=px.bar(df_2,y="Districts",x="AppOpens",title="AVERAGE OF APPOPENS", hover_name="Districts", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=500)
        st.plotly_chart(fig_amount_2)

def top_chart_registered_users(table_name):

    #establish the connection to mysql
    connection_mysql = mysql.connector.connect(host="localhost",user="root",password="12345",database="phonepe_data")
    mycursor_mysql = connection_mysql.cursor()
    # plot query1
    query1=f'''select States, SUM(RegisteredUsers) as RegisteredUsers
                    from {table_name}
                    group by States
                    order by RegisteredUsers ;'''
    mycursor_mysql.execute(query1)
    table_1=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_1=pd.DataFrame(table_1,columns=("States", "RegisteredUsers"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1,x="States",y="RegisteredUsers",title="REGISTERED USERS", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=1000)
        st.plotly_chart(fig_amount_1)

    #plot query2
    query2=f'''select States, AVG(RegisteredUsers) as RegisteredUsers
                    from {table_name}
                    group by States
                    order by RegisteredUsers;'''
    mycursor_mysql.execute(query2)
    table_2=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_2=pd.DataFrame(table_2,columns=("States", "RegisteredUsers"))
    with col2:
        fig_amount_2=px.bar(df_2,y="States",x="RegisteredUsers",title="AVERAGE OF REGISTERED USERS", hover_name="States", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=1000)
        st.plotly_chart(fig_amount_2)
        
def top_chart_Percentage(table_name):

    #establish the connection to mysql
    connection_mysql = mysql.connector.connect(host="localhost",user="root",password="12345",database="phonepe_data")
    mycursor_mysql = connection_mysql.cursor()
    # plot query1
    query1=f'''select Brands, sum(Percentage) as Percentage 
                from {table_name} group by Brands
                order by Percentage;'''
    mycursor_mysql.execute(query1)
    table_1=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_1=pd.DataFrame(table_1,columns=("Brands", "Percentage"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1,x="Brands",y="Percentage",title="PERCENTAGES", hover_name="Brands",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=500)
        #fig_amount_1.update_layout(yaxis=dict(range=[50.5,51.5]))
        st.plotly_chart(fig_amount_1)

    #plot query2
    query2=f'''select Brands, avg(Percentage) as Percentage 
                from {table_name} group by Brands
                order by Percentage'''
    mycursor_mysql.execute(query2)
    table_2=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_2=pd.DataFrame(table_2,columns=("Brands", "Percentage"))
    with col2:
        fig_amount_2=px.bar(df_2,y="Brands",x="Percentage",title="AVERAGE OF PERCENTAGES", hover_name="Brands", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=500)
        st.plotly_chart(fig_amount_2)


def top_chart_Brands(table_name):

    #establish the connection to mysql
    connection_mysql = mysql.connector.connect(host="localhost",user="root",password="12345",database="phonepe_data")
    mycursor_mysql = connection_mysql.cursor()
    # plot query1
    query1=f'''select Brands, sum(Transaction_count) as Transaction_count 
                    from {table_name}
                    group by Brands
                    order by Transaction_count desc
                    limit 10;'''
    mycursor_mysql.execute(query1)
    table_1=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_1=pd.DataFrame(table_1,columns=("Brands", "Transaction_count"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1,x="Brands",y="Transaction_count",title="TOP 10 BRANDS", hover_name="Brands",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=500)
        st.plotly_chart(fig_amount_1)
        
    # plot query2
    query2=f'''select Brands, sum(Transaction_count) as Transaction_count 
                    from {table_name}
                    group by Brands
                    order by Transaction_count
                    limit 10;'''
    mycursor_mysql.execute(query2)
    table_2=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_2=pd.DataFrame(table_2,columns=("Brands", "Transaction_count"))
    with col2:
        fig_amount_2=px.bar(df_2,x="Brands",y="Transaction_count",title="LAST 10 BRANDS", hover_name="Brands",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=500)
        st.plotly_chart(fig_amount_2)

    #plot query3
    query3=f'''select Brands, AVG(Transaction_count) as Transaction_count 
                        from aggregated_user
                        group by Brands
                        order by Transaction_count;'''
    mycursor_mysql.execute(query3)
    table_3=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_3=pd.DataFrame(table_3,columns=("Brands", "Transaction_count"))

    fig_amount_3=px.bar(df_3,y="Brands",x="Transaction_count",title="AVERAGE OF TRANSACTION COUNT OF BRANDS ", hover_name="Brands", orientation="h",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)
    
def top_chart_transaction_type(table_name,state):

    #establish the connection to mysql
    connection_mysql = mysql.connector.connect(host="localhost",user="root",password="12345",database="phonepe_data")
    mycursor_mysql = connection_mysql.cursor()
    # plot query1
    query1=f'''select Transaction_type, sum(Transaction_count) as Transaction_count 
                        from {table_name}
                        where States='{state}'
                        group by Transaction_type
                        order by Transaction_count;'''
    mycursor_mysql.execute(query1)
    table_1=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_1=pd.DataFrame(table_1,columns=("Transaction_type", "Transaction_count"))
    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(df_1,names="Transaction_type",values="Transaction_count",title= f"{state.upper()} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,hole=0.5,width=600)
        st.plotly_chart(fig_pie_1)
    #plot query2
    query2=f'''select Transaction_type, avg(Transaction_count) as Transaction_count 
                        from {table_name}
                        where States='{state}'
                        group by Transaction_type
                        order by Transaction_count;'''
    mycursor_mysql.execute(query2)
    table_2=mycursor_mysql.fetchall()
    connection_mysql.commit()
    df_2=pd.DataFrame(table_2,columns=("Transaction_type", "Transaction_count"))
    with col2:
        fig_pie_2=px.pie(df_2,names="Transaction_type",values="Transaction_count",title= f"{state.upper()} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.BuGn_r,hole=0.5,width=600)
        st.plotly_chart(fig_pie_2)

#streamlit part
st.set_page_config(layout= "wide")
img=Image.open(r"C:\Users\Sriram\Desktop\phonepeimg\phonepelogo1.png")
img1=st.image(img,width=800)

st.title(":red[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]")

with st.sidebar:
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])
    
if select=="HOME":
    st.markdown("### :blue[A User-Friendly Tool Using Streamlit and Plotly]")
    st.markdown("### :blue[This streamlit app can be used to visualize the PhonePe pulse data and gain lots of insights on Transactions]")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("### :blue[Phonepe is an Indian digital payments and financial technology company]")
        st.write("FEATURES:")
        st.write("Credit and Debit card linking")
        st.write("Bank balance check")
        st.download_button("DOWNLOAD THE APP NOW","https://www.phonepe.com/app-download/")                 
    with col2:
        
        st.image(Image.open(r"C:\Users\Sriram\Desktop\phonepeimg\phonepe.jpg"),width=400)
    col3,col4=st.columns(2)
    with col3:
        st.image(Image.open(r"C:\Users\Sriram\Desktop\phonepeimg\phonepegeo.jpg"),width=300)
    with col4:
        st.markdown("PhonePe is a popular digital payment service in India that enables users to transfer money from their wallets to bank accounts. ")
        st.markdown(" It also offers services like mobile recharge, bill payments, and buying gold. ")
        st.write("Pay directly to any bank account from any bank account instantly")
    st.video(r"C:\Users\Sriram\Downloads\phonepe_video_streamlit.mp4")
        
elif select=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    with tab1:
        method1=st.radio("Select The Method",["Aggregated Transaction Analysis","Aggregated User Analysis"])
        
        if method1=="Aggregated Transaction Analysis":
            
            years=st.selectbox("select the year",Aggre_transaction["Years"].unique())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)
            
            states=st.selectbox("select the State",Aggre_tran_tac_Y["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)
            
            quarters=st.selectbox("select the Quarter",Aggre_tran_tac_Y["Quarter"].unique())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)
            
            states=st.selectbox("select the State based on transaction type",Aggre_transaction["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)
            
        elif method1=="Aggregated User Analysis":
            
            years=st.selectbox("select the year",Aggre_user["Years"].unique())
            Aggre_user_Y=Aggre_user_plot_1(Aggre_user,years)
            
            quarters=st.selectbox("select the Quarter",Aggre_user_Y["Quarter"].unique())
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y,quarters)
            
            states=st.selectbox("select the State",Aggre_user_Y_Q["States"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q,states)
            
    with tab2:
        method2=st.radio("Select The Method",["Map Transaction Analysis","Map User Analysis"]) 
        
        if method2=="Map Transaction Analysis":
            
            years=st.selectbox("select the year for map transaction",Map_transaction["Years"].unique())
            Map_tran_tac_Y=Transaction_amount_count_Y(Map_transaction,years)
            
            states=st.selectbox("select the State for map transaction",Map_tran_tac_Y["States"].unique())
            Map_Tran_Districts(Map_tran_tac_Y,states)
            
            quarters=st.selectbox("select the Quarter for map transaction",Map_tran_tac_Y["Quarter"].unique())
            Map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Map_tran_tac_Y,quarters)
            
            states=st.selectbox("select the State for map transaction quarter wise",Map_tran_tac_Y_Q["States"].unique())
            Map_Tran_Districts(Map_tran_tac_Y_Q,states)
            
        elif method2=="Map User Analysis":
            
            years=st.selectbox("select the year for map user",Map_user["Years"].unique())
            Map_user_Y=map_user_plot_1(Map_user,years)
            
            quarters=st.selectbox("select the Quarter for map user",Map_user_Y["Quarter"].unique())
            Map_user_Y_Q=map_user_plot_2(Map_user_Y,quarters)
            
            states=st.selectbox("select the State for map user",Map_user_Y_Q["States"].unique())
            map_user_plot_3(Map_user_Y_Q,states)
            
            
    with tab3:
        method3=st.radio("Select The Method",["Top Transaction Analysis","Top User Analysis"])
        if method3=="Top Transaction Analysis":
            
            years=st.selectbox("select the year for top transaction",Top_transaction["Years"].unique())
            Top_tran_tac_Y=Transaction_amount_count_Y(Top_transaction,years)
            
            states=st.selectbox("select the State for top transaction",Top_tran_tac_Y["States"].unique())
            Top_tran_plot_1(Top_tran_tac_Y,states)
            
            quarters=st.selectbox("select the Quarter for top transaction",Top_tran_tac_Y["Quarter"].unique())
            Top_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Top_tran_tac_Y,quarters)
            
            
            
        elif method3=="Top User Analysis":
            years=st.selectbox("select the year for top user",Top_user["Years"].unique())
            Top_user_Y=top_user_plot_1(Top_user,years)
            
            states=st.selectbox("select the State for top user",Top_user_Y["States"].unique())
            top_user_plot_2(Top_user_Y,states)
            
elif select=="TOP CHARTS":
    questions=st.selectbox("Select the Question:",["1. Transaction Amount and Count of Aggregated Transaction",
                                                   "2. Transaction Amount and Count of Map Transaction",
                                                   "3. Transaction Amount and Count of Top Transaction",
                                                   "4. Transaction Count of Aggregated User",
                                                   "5. Registered users of Map User",
                                                   "6. App Opens of Map User",
                                                   "7. Registered users of Top User",
                                                   "8. Percentages of Brands",
                                                   "9. Transaction count of Brands",
                                                   "10. Transaction count of Transaction type"])
    
    if questions== "1. Transaction Amount and Count of Aggregated Transaction":
        top_chart_transaction_amount("aggregated_transaction")
        top_chart_transaction_count("aggregated_transaction")   
    elif questions=="2. Transaction Amount and Count of Map Transaction":
        top_chart_transaction_amount("map_transaction")
        top_chart_transaction_count("map_transaction")
    elif questions== "3. Transaction Amount and Count of Top Transaction":
        top_chart_transaction_amount("top_transaction")
        top_chart_transaction_count("top_transaction")
    elif questions== "4. Transaction Count of Aggregated User":
        top_chart_transaction_count("aggregated_user")
    elif questions=="5. Registered users of Map User":
        states=st.selectbox("select the state", Map_user["States"].unique())
        top_chart_registered_user("map_user",states)
    elif questions=="6. App Opens of Map User":
        states=st.selectbox("select the state", Map_user["States"].unique())
        top_chart_appopens("map_user",states)
    elif questions=="7. Registered users of Top User":
        top_chart_registered_users("top_user")
    elif questions=="8. Percentages of Brands":
        top_chart_Percentage("aggregated_user")
    elif questions=="9. Transaction count of Brands":
        top_chart_Brands("aggregated_user")
    elif questions=="10. Transaction count of Transaction type":
        states=st.selectbox("select the state", Aggre_transaction["States"].unique())
        top_chart_transaction_type("aggregated_transaction",states)
      
        

    
        