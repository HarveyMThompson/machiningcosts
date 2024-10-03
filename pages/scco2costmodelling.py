# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 14:41:30 2024

@author: harveythompson
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

###############################################################################
# Functions
###############################################################################

# define cost function for ScCO2 + MQL cooling
def scco2_costs():
    
    # set machining variables
    annual_hrs=st.session_state.annual_hrs
    hrly_op_cost=st.session_state.hrly_op_cost
    hrly_mtool_cost=st.session_state.hrly_mtool_cost
    insert_cost=st.session_state.insert_cost
    
    # set scCO2 variables
    co2_costperkg=st.session_state.co2_costperkg
    co2_hrly_consumption=st.session_state.co2_hrly_consumption
    scco2_tool_life=st.session_state.scco2_tool_life 
    mql_costperkg = st.session_state.mql_costperkg
    mql_hrly_consumption = st.session_state.mql_hrly_consumption
    
    co2_costperhr = co2_costperkg*co2_hrly_consumption
    co2_annual_cost = co2_costperhr*annual_hrs
    mql_costperhr = mql_costperkg*mql_hrly_consumption
    mql_annual_cost = mql_costperhr*annual_hrs
    scco2_annual_tools = int(60*annual_hrs/scco2_tool_life)+1
    scco2_tool_cost = insert_cost*scco2_annual_tools
    scco2_annual_cost = (hrly_op_cost+hrly_mtool_cost)*annual_hrs \
        + co2_annual_cost + mql_annual_cost + scco2_tool_cost

    # plot relative costs on bar charts
    scco2c1 = (hrly_op_cost+hrly_mtool_cost)*annual_hrs
    scco2c2 = scco2_annual_cost
    scco2c3 = mql_annual_cost
    scco2c4 = scco2_tool_cost

    return scco2_annual_cost,scco2c1,scco2c2,scco2c3,scco2c4

def on_plot():
    scco2_annual_cost,scco2c1,scco2c2,scco2c3,scco2c4 = scco2_costs()
    scco2_plotdata = pd.DataFrame({
        "machining":[scco2c1],"CO2":[scco2c2],"MQL":[scco2c3],"Inserts":[scco2c4]},        
        index=["scCO2"])
    scco2_plotdata.plot(kind='bar', stacked=True,width=0.2)
    # plot conditions on graph
    plt.text(0.15,0.9*scco2_annual_cost,'AH: '+ str(st.session_state.annual_hrs))
    plt.text(0.15,0.8*scco2_annual_cost,'HOC: '+ str(st.session_state.hrly_op_cost))
    plt.text(0.15,0.7*scco2_annual_cost,'HMC: '+ str(st.session_state.hrly_mtool_cost))
    plt.text(0.15,0.6*scco2_annual_cost,'CO2C: '+ str(st.session_state.co2_costperkg))
    plt.text(0.15,0.5*scco2_annual_cost,'CO2Cons: '+ str(st.session_state.co2_hrly_consumption))
    plt.text(0.15,0.4*scco2_annual_cost,'IC: '+ str(st.session_state.insert_cost))
    plt.text(0.15,0.3*scco2_annual_cost,'TL: '+ str(st.session_state.scco2_tool_life))
    plt.text(0.15,0.2*scco2_annual_cost,'MQLC: '+ str(st.session_state.mql_costperkg))
    plt.text(0.15,0.1*scco2_annual_cost,'MQLCons: '+ str(st.session_state.mql_hrly_consumption))
    plt.title("Contributions to scCO2 Costs")
    plt.savefig('scco2_stackedbar.jpg')    
    return plt


# Add heading and introductory text
st.set_page_config(layout='wide')

st.title("ScCO2 Cost Modelling Program")
st.write("This application enables you to calculate the total cost of scCO2 + MQL cooling")
st.markdown("---")

# Create the input slides - Row 1
row1 = st.columns([1,1,1,3])

#  Total Annual Hours
default_value = 1000.0
st.session_state.annual_hrs = default_value
annual_hrs = row1[0].slider("Annual Hours", 900.00, 1100.00, default_value)
st.session_state.annual_hrs = annual_hrs

#  Hourly Operator Cost
default_value = 60.0
st.session_state.hrly_op_cost = default_value
hrly_op_cost = row1[1].slider("Hourly Operator Cost (£)", 20.00, 100.00, default_value)
st.session_state.hrly_op_cost = hrly_op_cost

#  Hourly MachineCost
default_value = 60.0
st.session_state.hrly_mtool_cost = default_value
hrly_mtool_cost = row1[2].slider("Hourly Machine Cost (£)", 20.00, 100.00, default_value)
st.session_state.hrly_mtool_cost = hrly_mtool_cost

if row1[3].button("Plot Graph"):
    plt = on_plot()
    row1[3].pyplot(plt)

# Create the input slides - Row 2
row2 = st.columns([1,1,1,3])

#  CO2 Cost (£/kg)
default_value = 1.00
st.session_state.co2_costperkg = default_value
co2_costperkg = row2[0].slider("CO2 Cost (£/kg)", 0.50, 2.00, default_value)
st.session_state.co2_costperkg = co2_costperkg

#  CO2 hourly consumption (kg/hour)
default_value = 30.0
st.session_state.co2_hrly_consumption = default_value
co2_hrly_consumption = row2[1].slider("CO2 consumption (kg/hour)", 10.0, 60.0, default_value)
st.session_state.co2_hrly_consumption = co2_hrly_consumption

#  Insert Cost
default_value = 12.0
st.session_state.insert_cost = default_value
insert_cost = row2[2].slider("Insert Cost (£)", 10.0, 40.00, default_value)
st.session_state.insert_cost = insert_cost

# Create the input slides - Row 3
row3 = st.columns([1,1,1,3])

#  Tool Life (mins)
default_value = 10.0
st.session_state.scco2_tool_life = default_value
scco2_tool_life = row3[0].slider("Tool Life (mins)", 1.0, 100.00, default_value)
st.session_state.scco2_tool_life = scco2_tool_life

#  MQL cost (£/kg)
default_value = 1000.0
st.session_state.mql_costperkg = default_value
mql_costperkg = row3[1].slider("MQL cost (£/kg)", 500.0, 2000.00, default_value)
st.session_state.mql_costperkg = mql_costperkg

#  MQL consumption (kg/hour)
default_value = 0.10
st.session_state.mql_hrly_consumption = default_value
mql_hrly_consumption = 0.001*row3[2].slider("MQL consumption (g/hour)", 0.01, 1.00, default_value)
st.session_state.mql_hrly_consumption = mql_hrly_consumption

scco2_annual_cost,scco2c1,scco2c2,scco2c3,scco2c4 = scco2_costs()
st.write("scCO2 Annual Cost (£)",scco2_annual_cost)

