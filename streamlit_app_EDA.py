import streamlit as st
import pandas as pd 
import numpy as np
import os

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT * FROM D_merged_processed limit 10;', ttl="10m")

for row in df.itertuples():
    st.write(f"{row.id} has a :{row.loan_id}:")
    
st.dataframe(df, use_container_width=True)
