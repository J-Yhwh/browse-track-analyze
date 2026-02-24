
import sys
import os


#Interactive plot libraries
from pathlib import Path
from src.analyzer import main as analyzer_main
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


#Repo root designed to work exactly as categorized in project file-structure git
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, REPO_ROOT)


#######################################################################################################################
##The idea is to run from "src/analyzer_eda.py", then extract the output for mroe readable diagrams & chart summaries##
#######################################################################################################################



#Thin wrapper: runs analyzer.py logic + adds interactive EDA extras

if __name__ == "__main__":
    # Run the CLI-style analysis first (generates reports)
    analyzer_main()  # this will process CSVs and save three reports

    # Now add EDA extras (plots, deeper stats, etc.)
    print("\nRunning interactive EDA extras...")

    # Re-load for plotting (or reuse from analyzer if you refactor)
    REPO_ROOT = Path.home() / "Desktop" / "main"
    macos_df = pd.read_csv(REPO_ROOT / "data" / "brave_macos_cookies.csv")
    ios_df   = pd.read_csv(REPO_ROOT / "data" / "brave_ios_emulated_cookies.csv")

    combined = pd.concat([
        macos_df.assign(platform='macOS'),
        ios_df.assign(platform='iOS')
    ], ignore_index=True)

# Cookie Expiration Analysis

# Convert expiration timestamps to datetime (adjust column name if needed)
combined['expires_date'] = pd.to_datetime(combined['expires_date'], errors='coerce')
combined['days_to_expire'] = (combined['expires_date'] - pd.Timestamp.now()).dt.days

# Summary stats
print("\n=== Cookie Expiration Summary ===")
print(combined.groupby('platform')['days_to_expire'].describe())


# Secure vs Non-Secure Pie Chart - Robust Version (handles missing data)

print("=== iOS Data Debug ===")
print("iOS columns:", ios_df.columns.tolist())

if 'is_secure' in ios_df.columns:
    print("\n'is_secure' value counts in iOS data:")
    print(ios_df['is_secure'].value_counts(dropna=False))
    print("\nNumber of rows in iOS:", len(ios_df))
    print("Sample iOS 'is_secure' values:")
    print(ios_df['is_secure'].head(10))
else:
    print("\n'is_secure' column MISSING in iOS CSV!")

    print("Possible similar columns:", [col for col in ios_df.columns if 'secure' in col.lower()])

# Compute secure_counts (only for rows that have 'is_secure')
if 'is_secure' in combined.columns:
    secure_counts = combined.groupby(['platform', 'is_secure']).size().unstack(fill_value=0)
else:
    secure_counts = pd.DataFrame(index=combined['platform'].unique(), columns=[False, True], data=0)
    print("Warning: 'is_secure' column missing — all cookies treated as non-secure.")

# Debug print (for missing/ invalid data error msgs
print("\n=== Secure Counts (after fix) ===\n", secure_counts)

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

platforms = combined['platform'].unique()

for i, platform in enumerate(platforms):
    if platform not in secure_counts.index or secure_counts.loc[platform].sum() == 0:
        axes[i].text(0.5, 0.5, f'No data for {platform}', ha='center', va='center', fontsize=12)
        axes[i].axis('off')
        continue
    if platform in secure_counts.index:
        counts = secure_counts.loc[platform]
        total = counts.sum()
        if total == 0:
            counts = pd.Series([1, 0], index=[False, True])  # avoid zero-sum crash
            print(f"Note: Zero cookies for {platform} — showing placeholder pie.")
    else:
        counts = pd.Series([0, 0], index=[False, True])
        print(f"Note: No data for {platform} — showing empty pie.")

    # Pie chart with zero-sum protection
    wedges, texts, autotexts = axes[i].pie(
        counts,
        labels=['Non-Secure', 'Secure'],
        autopct='%1.1f%%' if counts.sum() > 0 else None,
        colors=['#e74c3c', '#3498db'],
        startangle=90,
        shadow=True,
        explode=[0.08, 0.02],
        pctdistance=0.85,
        textprops={'fontsize': 12}
    )

    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    axes[i].add_artist(centre_circle)

    axes[i].set_title(f'{platform} Secure vs Non-Secure', fontsize=14, pad=20)
    axes[i].axis('equal')

plt.suptitle('Secure vs Non-Secure Cookies by Platform', fontsize=16, y=1.05)
plt.tight_layout()
plt.show()

print("Pie charts generated (with handling for missing data)!")

