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

# define cost function
def costs():
    
    # set machining variables
    annual_hrs=st.session_state.annual_hrs
    hrly_op_cost=st.session_state.hrly_op_cost
    hrly_mtool_cost=st.session_state.hrly_mtool_cost
    insert_cost=st.session_state.insert_cost
    
    # set flooded variables
    mwf_costperlitre=st.session_state.mwf_costperlitre
    mwf_annual_litres=st.session_state.mwf_annual_litres
    flooded_tool_life=st.session_state.flooded_tool_life 
    mwf_annual_cost = mwf_costperlitre*mwf_annual_litres
    flooded_annual_tools = int(60*annual_hrs/flooded_tool_life)+1
    flooded_tool_cost = insert_cost*flooded_annual_tools
    flooded_annual_cost = (hrly_op_cost+hrly_mtool_cost)*annual_hrs \
        + mwf_annual_cost + flooded_tool_cost

    # plot relative costs on bar charts
    fc1 = (hrly_op_cost+hrly_mtool_cost)*annual_hrs
    fc2 = mwf_annual_cost
    fc3 = flooded_tool_cost
    
    return flooded_annual_cost,fc1,fc2,fc3

def on_plot():
    
    plt.figure(figsize=(12,8))
    flooded_annual_cost,fc1,fc2,fc3 = costs()
    flooded_plotdata = pd.DataFrame({
        "machining":[fc1],
        "mwf":[fc2],
        "inserts":[fc3]},
         index=["Flooded"])
    flooded_plotdata.plot(kind='bar', stacked=True,width=0.2)
    
    # plot conditions on graph
    plt.text(0.15,0.6*flooded_annual_cost,'AH: '+ str(st.session_state.annual_hrs))
    plt.text(0.15,0.55*flooded_annual_cost,'HOC: '+ str(st.session_state.hrly_op_cost))
    plt.text(0.15,0.5*flooded_annual_cost,'HMC: '+ str(st.session_state.hrly_mtool_cost))
    plt.text(0.15,0.45*flooded_annual_cost,'MWFCPL: '+ str(st.session_state.mwf_costperlitre))
    plt.text(0.15,0.4*flooded_annual_cost,'MWFAL: '+ str(st.session_state.mwf_annual_litres))
    plt.text(0.15,0.35*flooded_annual_cost,'IC: '+ str(st.session_state.insert_cost))
    plt.text(0.15,0.3*flooded_annual_cost,'TL: '+ str(st.session_state.flooded_tool_life))
    plt.title("Contributions to Flooded Costs")
    plt.savefig('flooded_stackedbar.jpg')    
    st.pyplot(plt)

def on_testplot():
    
    fig = plt.figure(figsize=(12,8))
    flooded_annual_cost,fc1,fc2,fc3 = costs()
    flooded_plotdata = pd.DataFrame({
        "machining":[fc1],
        "mwf":[fc2],
        "inserts":[fc3]},
         index=["Flooded"])
    flooded_plotdata.plot(kind='bar', stacked=True,width=0.2)
    
    # plot conditions on graph
    plt.text(0.15,0.6*flooded_annual_cost,'AH: '+ str(st.session_state.annual_hrs))
    plt.text(0.15,0.55*flooded_annual_cost,'HOC: '+ str(st.session_state.hrly_op_cost))
    plt.text(0.15,0.5*flooded_annual_cost,'HMC: '+ str(st.session_state.hrly_mtool_cost))
    plt.text(0.15,0.45*flooded_annual_cost,'MWFCPL: '+ str(st.session_state.mwf_costperlitre))
    plt.text(0.15,0.4*flooded_annual_cost,'MWFAL: '+ str(st.session_state.mwf_annual_litres))
    plt.text(0.15,0.35*flooded_annual_cost,'IC: '+ str(st.session_state.insert_cost))
    plt.text(0.15,0.3*flooded_annual_cost,'TL: '+ str(st.session_state.flooded_tool_life))
    plt.title("Contributions to Flooded Costs")
    plt.savefig('flooded_stackedbar.jpg')    
    return plt

# Add heading and introductory text
st.set_page_config(layout='wide')

st.title("Flooded Cost Modelling Program")
st.write("This application enables you to calculate the total cost of flooded or scCO2 + MQL cooling")
st.markdown("---")

if 'pwdcheck' not in st.session_state:
    st.session_state['pwdcheck'] = 0
    password_guess = st.text_input('What is the password?')
    if password_guess != st.secrets["password"]:
        st.stop()
    
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
    plt = on_testplot()
    row1[3].pyplot(plt)

# Create the input slides - Row 2
row2 = st.columns([1,1,1,3])

#  MWF Cost Per Litre
default_value = 9.15
st.session_state.mwf_costperlitre = default_value
mwf_costperlitre = row2[0].slider("MWF Cost Per Litre (£)", 8.00, 12.00, default_value)
st.session_state.mwf_costperlitre = mwf_costperlitre

#  MWF Annual Litres
default_value = 150.0
st.session_state.mwf_annual_litres = default_value
mwf_annual_litres = row2[1].slider("MWF Annual Litres", 100.0, 400.00, default_value)
st.session_state.mwf_annual_litres = mwf_annual_litres

#  Insert Cost
default_value = 12.0
st.session_state.insert_cost = default_value
insert_cost = row2[2].slider("Insert Cost (£)", 10.0, 40.00, default_value)
st.session_state.insert_cost = insert_cost

# Create the input slides - Row 3
row3 = st.columns([1,1,1,3])

#  Tool Life (mins)
default_value = 10.0
st.session_state.flooded_tool_life = default_value
flooded_tool_life = row3[0].slider("Tool Life (mins)", 1.0, 100.00, default_value)
st.session_state.flooded_tool_life = flooded_tool_life

flooded_annual_cost,fc1,fc2,fc3 = costs()
st.write("Flooded Annual Cost (£)",flooded_annual_cost)

