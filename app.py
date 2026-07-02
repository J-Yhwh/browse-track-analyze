# Copyright (c) 2026. Jac LL
# All Rights Reserved. 
# Unauthorized use or distribution is prohibited.

import streamlit as st
import pandas as pd
import polars as pl
from pathlib import Path
import plotly.express as px
from datetime import datetime

# ML Libraries for data amalgamation and computing
import seaborn as sns
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Preparation of Steamlit Dashboard for high-level cross-CSV analysis and presentation
st.set_page_config(page_title="Browser Tracker Analyzer", layout="wide")
st.title("🕵️‍♀️ Browser Track Analyze")
st.markdown("**Privacy-focused cross-platform browser cookie & tracking analysis**")

# ====================== DATA LOADING ======================
@st.cache_data
def load_all_data(data_folder="data"):
    data_path = Path(data_folder)
    st.write(f"🔍 Looking in: {data_path.absolute()}")

    csv_files = list(data_path.glob("*.csv"))
    st.write(f"📂 Found {len(csv_files)} CSV files: {[f.name for f in csv_files]}")

    all_dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            df['source_file'] = file.name

            # Infer Browser & OS from filename
            fname = file.name.lower()
            
            if 'brave' in fname and 'windows' in fname:
                df['browser'] = 'Brave'
                df['os'] = 'windowsOS'
            elif 'brave' in fname and 'ios' in fname:
                df['browser'] = 'Brave'
                df['os'] = 'iOS (Playwright)'
            elif 'safari' in fname and 'ios' in fname:
                df['browser'] = 'Safari'
                df['os'] = 'iOS (Playwright)'
            elif 'brave' in fname:
                df['browser'] = 'Brave'
                df['os'] = 'macOS'
            elif 'safari' in fname:
                df['browser'] = 'Safari'
                df['os'] = 'macOS'
            elif 'edge' in fname or 'msedge' in fname:
                df['browser'] = 'Edge'
                df['os'] = 'windowsOS'
            else:
                df['browser'] = 'Unknown'
                df['os'] = 'Unknown'

            all_dfs.append(df)
            st.success(f"✅ Loaded {file.name} -> {len(df)} rows ({df['browser'].iloc[0]} on {df['os'].iloc[0]})")

        except Exception as e:
            st.error(f"Failed to load {file.name}: {e}")

    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return pd.DataFrame()

df = load_all_data()


# ====================== POLARS ENHANCEMENT====================

if not df.empty:
    # Convert once to Polars for fast operations
    df_pl = pl.from.pandas(df)
    st.success(f"✅ Enhanced with Polars: {len(df_pl):,} rows ready for fast processing")

    st.subheader("Advanced Filters (Powered by Polars)")

    selected_browsers = st.multiselect("Browser(s)", options=df['browser'].unique(), default=df['browser'].unique())

    # Fast filtering with Polars
    
    filtered_pl = df_pl.filter(pl.col("browser").is_in(selected_browsers))
    filtered_df = filtered_pl.to_pandas()   # Convert back only when needed for Streamlit

else:
    filtered_df = pd.DataFrame()    

# ====================== DASHBOARD ======================
if filtered_df.empty:
    st.info("No data loaded yet. Double-check your 'data/' folder.")
else:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Cookies", len(filtered_df))
    with col2:
        st.metric("Unique Domains", filtered_df['domain'].nunique() if 'domain' in filtered_df.columns else 0)
    with col3:
        st.metric("Browsers", filtered_df['browser'].nunique())
    with col4:
        st.metric("OS Variants", filtered_df['os'].nunique())
    with col5:
        st.metric("Secure", filtered_df['secure'].nunique() if 'secure' in filtered_df.columns else 0)

    # Cookies by browser + OS
    st.subheader("Cookies by Browser & OS")
    count_df = filtered_df.groupby(['browser','os']).size().reset_index(name='count')
    fig = px.bar(count_df, x='browser', y='count', color='os', text='count', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

    # Top Domains
    if 'domain' in filtered_df.columns:
        st.subheader("Top 10 Domains")
        top_domains = filtered_df['domain'].value_counts().head(10).reset_index()
        top_domains.columns = ['Domain', 'Count']
        fig2 = px.bar(top_domains, x='Domain', y='Count', color='Domain', text='Count')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Raw Data Preview")
    st.dataframe(filtered_df.head(150), use_container_width=True)

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Built By Jacqueline Liao")



