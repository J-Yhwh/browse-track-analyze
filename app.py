

import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Browser Tracker Analyzer", layout="wide")
st.title("🕵️‍♀️ Browser Track Analyze")
st.markdown("**Privacy-focused cross-platform browser cookie & tracking analysis**")

# ====================== DATA LOADING ======================
@st.cache_data
def load_all_data(data_folder="data"):
    data_path = Path(data_folder)
    if not data_path.exists():
        st.error(f"Folder '{data_folder}' not found!")
        return pd.DataFrame()
    
    csv_files = list(data_path.glob("*.csv"))
    if not csv_files:
        st.warning("No CSV files found in data folder.")
        return pd.DataFrame()
    
    all_dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            df['source_file'] = file.name
            
            # Infer browser from filename
            fname = file.name.lower()
            if 'brave' in fname:
                df['browser'] = 'Brave'
            elif 'safari' in fname:
                df['browser'] = 'Safari'
            elif 'edge' in fname:
                df['browser'] = 'Edge'
            else:
                df['browser'] = 'Unknown'
            
            all_dfs.append(df)
            
        except Exception as e:
            st.warning(f"Could not load {file.name}: {e}")
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return pd.DataFrame()

df = load_all_data()

# ====================== SIDEBAR FILTERS ======================
st.sidebar.header("🔍 Advanced Filters")

if not df.empty:
    browsers = sorted(df['browser'].unique())
    selected_browsers = st.sidebar.multiselect("Browser(s)", browsers, default=browsers)

    if 'domain' in df.columns:
        domain_search = st.sidebar.text_input("Search Domain", "")
        domains = sorted(df['domain'].unique())
        if domain_search:
            domains = [d for d in domains if domain_search.lower() in d.lower()]
        selected_domains = st.sidebar.multiselect("Filter Domains", domains, default=[])

    cookie_search = st.sidebar.text_input("Search Cookie Name", "")

    secure_only = st.sidebar.checkbox("Secure cookies only", value=False)
    httponly_only = st.sidebar.checkbox("HttpOnly cookies only", value=False)

# ====================== APPLY FILTERS ======================
filtered_df = df.copy()

if not df.empty:
    if selected_browsers:
        filtered_df = filtered_df[filtered_df['browser'].isin(selected_browsers)]
    
    if 'domain' in filtered_df.columns and 'selected_domains' in locals() and selected_domains:
        filtered_df = filtered_df[filtered_df['domain'].isin(selected_domains)]
    
    if cookie_search and 'name' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['name'].str.contains(cookie_search, case=False, na=False)]
    
    if secure_only and 'secure' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['secure'] == True]
    
    if httponly_only and 'httpOnly' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['httpOnly'] == True]

# ====================== MAIN DASHBOARD ======================
if filtered_df.empty:
    st.info("No data loaded yet. Place your CSV files in the `data/` folder.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Cookies", len(filtered_df))
    with col2:
        st.metric("Unique Domains", filtered_df['domain'].nunique() if 'domain' in filtered_df.columns else 0)
    with col3:
        st.metric("Browsers", filtered_df['browser'].nunique())

    st.subheader("Cookies per Browser")
    browser_count = filtered_df['browser'].value_counts().reset_index()
    browser_count.columns = ['Browser', 'Count']
    fig = px.bar(browser_count, x='Browser', y='Count', color='Browser', text='Count')
    st.plotly_chart(fig, use_container_width=True)

    if 'domain' in filtered_df.columns:
        st.subheader("Top 10 Domains")
        top_domains = filtered_df['domain'].value_counts().head(10).reset_index()
        top_domains.columns = ['Domain', 'Count']
        fig2 = px.bar(top_domains, x='Domain', y='Count', color='Domain', text='Count')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Raw Data Preview")
    st.dataframe(filtered_df.head(100), use_container_width=True)

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Built with ❤️")
