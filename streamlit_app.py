# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:00:05 2024

@author: harveythompson
"""

import streamlit as st

flooded_page = st.Page("v5floodedcostmodelling.py", title="Flooded")
scco2_page = st.Page("scco2costmodelling.py",title="ScCO2 + MQL")

pg = st.navigation([flooded_page, scco2_page])
pg.run()