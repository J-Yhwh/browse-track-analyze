
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
    st.write(f"🔍 Looking in: {data_path.absolute()}")

    csv_files = list(data_path.glob("*.csv"))
    st.write(f"📂 Found {len(csv_files)} CSV files: {[f.name for f in csv_files]}")

    all_dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            df['source_file'] = file.name

            # Infer Browser & OS
            fname = file.name.lower()
            if 'brave' in fname and 'windows' in fname:
                df['browser'] = 'Brave'
                df['os'] = 'windowsOS'
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

# ====================== SIDEBAR FILTERS ======================
st.sidebar.header("🔍 Advanced Filters")

if not df.empty:
    # Browser & OS Filters
    selected_browsers = st.sidebar.multiselect("Browser(s)", sorted(df['browser'].unique()), default=df['browser'].unique())
    selected_os = st.sidebar.multiselect("OS", sorted(df['os'].unique()), default=df['os'].unique())

    if 'domain' in df.columns:
        domain_search = st.sidebar.text_input("Search Domain", "")
        selected_domains = st.sidebar.multiselect("Filter Domains", sorted(df['domain'].unique()), default=[])
    
    cookie_search = st.sidebar.text_input("Search Cookie Name", "")

    # Security Filters
    secure_only = st.sidebar.checkbox("Secure cookies only", value=False)
    httponly_only = st.sidebar.checkbox("HttpOnly cookies only", value=False)

# ====================== APPLY FILTERS ======================
filtered_df = df.copy()

if not df.empty:
    if selected_browsers:
        filtered_df = filtered_df[filtered_df['browser'].isin(selected_browsers)]  
    if selected_os:
        filtered_df = filtered_df[filtered_df['os'].isin(selected_os)]
    if 'domain' in filtered_df.columns and selected_domains:
        filtered_df = filtered_df[filtered_df['domain'].isin(selected_domains)]
    if cookie_search and 'name' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['name'].str.contains(cookie_search, case=False, na=False)]
    if secure_only and 'secure' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['secure'] == True]
    if httponly_only and 'httpOnly' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['httpOnly'] == True]

# ====================== DASHBOARD ======================
if filtered_df.empty:
    st.info("No data loaded yet. Double-check you 'data/' folder to ensure the CSV files are in place.")
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
        st.metric("secure", filtered_df['secure'].nunique())

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

    st.subheader("📊 Summary Findings & Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Key Observations**")
        total_cookies = len(filtered_df)
        unique_domains = filtered_df['domain'].nunique() if 'domain' in filtered_df.columns else 0
        secure_ratio = (filtered_df['secure'].mean() * 100) if 'secure' in filtered_df.columns else 0
        httponly_ratio = (filtered_df['httpOnly'].mean() * 100) if 'httpOnly' in filtered_df.columns else 0

        st.write(f"- **Total cookies analyzed**: {total_cookies:,}")
        st.write(f"- **Unique domains tracked**: {unique_domains}")
        st.write(f"- **Secure cookies**: {secure_ratio:.1f}%")
        st.write(f"- **HttpOnly cookies**: {httponly_ratio: .1f}%")

        if 'domain' in filtered_df.columns:
            top_domain = filtered_df['domain'].value_counts().idxmax()
            st.write(f"- **Most tracked domain**: '{top_domain}'")

    with col2:
        st.markdown("**Cross-Platform Insights**")
        os_browser = filtered_df.groupby(['os','browser'])
        st.dataframe(os_browser, use_container_width=True)
        
    st.markdown("---")
    st.info("""
    • Brave and Edge on Windows tend to have more persistent cookies compared to Safari on macOS.  
    • A high percentage of HttpOnly cookies indicates better security practices.  
    • Major tracking domains (google, facebook, etc.) appear consistently across browsers.
    """)    


    st.subheader("Raw Data Preview")
    st.dataframe(filtered_df.head(150), use_container_width=True)

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Built By Jacqueline Liao")
