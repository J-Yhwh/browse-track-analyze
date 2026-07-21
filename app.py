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
    st.write(f"🔍 Looking in: data/folder")

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
            elif 'brave' in fname and 'macos' in fname:
                df['browser'] = 'Brave'
                df['os'] = 'macOS'
            elif 'safari' in fname and 'macos' in fname:
                df['browser'] = 'Safari'
                df['os'] = 'macOS'
            elif 'edge' in fname or 'msedge' in fname:
                df['browser'] = 'Edge'
                df['os'] = 'windowsOS'
            elif 'brave' in fname and 'ios' in fname:
                df['browser'] = 'Brave'
                df['os'] = 'iOS (Playwright)'
            elif 'safari' in fname and 'ios' in fname:
                df['browser'] = 'Safari'
                df['os'] = 'iOS (Playwright)'
            elif 'brave' in fname and 'android' in fname:
                df['browser'] = 'Brave'
                df['os'] = 'Android (Playwright)'
            elif 'chrome' in fname and 'android' in fname:
                df['browser'] = 'Chrome'
                df['os'] = 'Android (Playwright)'
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


# ====================== POLARS ENHANCEMENT + FILTERS ==============================

if not df.empty:
    df_clean = df.copy()
    
    # Fix boolean columns 
    for col in ['secure', 'httpOnly']:
        if col in df_clean.columns:
            # Fill NaN with False and convert to integer (0/1)
            df_clean[col] = df_clean[col].fillna(False).astype(bool).astype(int)
    
    # Now safely convert to Polars
    df_pl = pl.from_pandas(df_clean)
    st.success(f"✅ Enhanced with Polars: {len(df_pl):,} rows")


    # =======FILTERS (Checkboxes)
    st.subheader("🔍Filters")
    col_a, col_b = st.columns(2)
    with col_a:
        http_only_filter = st.checkbox("Show httpOnly cookies", value=False)
    with col_b:
        intrusive_filter = st.checkbox("Show only intrusive cookies", value=False)

    #Apply filters with Polars
    filtered_pl = df_pl

    if http_only_filter:
        filtered_pl = filtered_pl.filter(pl.col("httpOnly") == True)
        
    if intrusive_filter:
        filtered_pl = filtered_pl.filter(
            (pl.col("httpOnly") == False) & (pl.col("secure") == False)
        )

    #Convert back to  Pandas for Streamlit display 
    filtered_df = filtered_pl.to_pandas()
    

else:
    filtered_df = pd.DataFrame()
    


 # ================= Visual & Interactive Filters =======================================

if not filtered_df.empty:
    st.subheader("📊 Cookies By Browser & OS")

    # Interactive filters
    col1, col2 = st.columns(2)
    with col1:
        selected_browsers = st.multiselect(
            "Filter Browsers",
            options=sorted(filtered_df['browser'].unique()),
            default=sorted(filtered_df['browser'].unique())
        )
    with col2:
        selected_os = st.multiselect(
            "Filter OS",
            options=sorted(filtered_df['os'].unique()),
            default=sorted(filtered_df['os'].unique())
        )


    # Apply browser & OS filters
    viz_df = filtered_df.copy()
    if selected_browsers:
        viz_df = viz_df[viz_df['browser'].isin(selected_browsers)]
    if selected_os:
        viz_df = viz_df[viz_df['os'].isin(selected_os)]

    # ===============INTERACTIVE DASHBOARD FEATURING DYNAMIC METRICS ===============================
    st.markdown("### 📈 Key Metrics (updates with Filters)")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Cookies", f"{len(viz_df):,}")
    with col2:
        st.metric("Unique Domains", viz_df['domain'].nunique() if 'domain' in viz_df.columns else 0)
    with col3:
        st.metric("Browsers", viz_df['browser'].nunique())
    with col4:
        st.metric("OS Variants", viz_df['os'].nunique())
    with col5:
        secure_count = viz_df['secure'].sum() if 'secure' in viz_df.columns else 0
        st.metric("Secure Cookies", f"{secure_count:,}")
    

    # Cookies Distribution by Browser & OS
    if not viz_df.empty:
        count_df = viz_df.groupby(['browser', 'os']).size().reset_index(name='count')
        fig = px.bar(
            count_df,
            x='browser',
            y='count',
            color='os',
            text='count',
            title= 'Cookies Distribution by Browser & OS',
            barmode='group'
        )
        fig.update_layout(xaxis_title="Browser", yaxis_title="Cookie Count")
        st.plotly_chart(fig, use_container_width=True)


        #  Secure vs HttpOnly
        st.subheader("🔐 Secure vs HttpOnly Cookies")

        col_a, col_b, col_c = st.columns(3)
        
        if 'secure' in viz_df.columns and 'httpOnly' in viz_df.columns:
            secure_ratio = (viz_df['secure'].mean() * 100)
            httponly_ratio = (viz_df['httponly'].mean() * 100)
            both_ratio = ((viz_df['secure'] == 1) & (viz_df['httpOnly'] == 1)).mean() * 100

            
            with col_a:
                st.metric("Secure Cookies", f"{secure_ratio:.1f}%")
            with col_b:
                st.metric("HttpOnly Cookies", f"{httponly_ratio:.1f}%")
            with col_c:
                st.metric("Both Secure & HttpOnly", f"{both_ratio:.1f}%")

            # Heatmap of Secure vs HttpOnly Cookies (seperate & combined)
            fig2 = plt.figure(figsize=(6, 4))
            correlation = viz_df[['secure', 'httpOnly']].corr()
            sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, fmt=".2f")    
            st.pyplot(fig2)
    else:
        st.warning("No data left after applying filters.")
          
    

#XG Boost Section
if not filtered_df.empty and 'domain' in filtered_df.columns:
    st.subheader("📈 XG Boost - Tracking Cookie Prediction")


    df_ml = filtered_df.copy()

    for col in ['secure', 'httpOnly']:
        if col in df_ml.columns:
            df_ml[col] = df_ml[col].astype(bool).astype(int)

    df_ml['domain_length'] = df_ml['domain'].str.len()
    df_ml['is_tracking'] = df_ml['domain'].str.contains(
        r'(google|facebook|doubleclick|analytics|pixel|ads|track)',
        case=False, na=False).astype(int)

    features = ['secure', 'httpOnly', 'domain_length']
    X = df_ml[features].fillna(0)
    y = df_ml['is_tracking']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = xgb.XGBClassifier(random_state=42, eval_metric='logloss')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc =accuracy_score(y_test, y_pred)

    st.success(f"Model Accuracy: **{acc:1%}**")

    importance = pd.DataFrame({
        'Feature': features,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    fig_imp = px.bar(importance, x='Importance', y='Feature', orientation='h', title='Feature_Importance')
    st.plotly_chart(fig_imp, use_container_width=True)


with st.expander("📋 Raw Data Preview (Click to expand)", expanded=False):
    st.dataframe(viz_df.head(200), use_container_width=True)
    st.caption(f"Showing first 200 rows of {len(viz_df):,} total cookies")
    


st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Built By Jacqueline Liao")


