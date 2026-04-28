
# BROWSER TRACKER ANALYZER - CONCEPT 

__A privacy focused tool for understanding how websites track users across different browsers and operating systems.__ 

This project utilises Python-based analytic tools and scripts to **scrape** browser cookies and tracker data from mujltiple platforms  (macOS Safari, Brave on macOS/Windows, Microsoft Edge, etc.) in latent form from the cache. The collected data are then collated and parsed by EDA(Exploratory Data Analytics), and then Machine Learning is applied to identify behavourial patterns, clustering, and potentially invasive tracking.

### Goal
Move beyond simple detection → **quantify and compare** the extent different browsers and OS environments allow for tracking, and **raise awareness about the sheer volume of trackers** users encounter daily.

### TOOLS ###

1. [![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
2. [![Playwright](https://img.shields.io/badge/Playwright-1.48+-green)](https://playwright.dev/)
3. [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---
### FEATURES
- Cross-platform cookie extraction (Brave, Safari, MS Edge, etc)
- Raw data export to CSV
- Breakdown of cookie and domain details, including security
- **Planned**: Streamlit dashboards for amalgamation of results for  comparison
- **Planned**: ML pipelines for tracker clustering and invasiveness prediction
---

### Version 1.2 - Released Febuary 2026 ### 
Main scripts:  extract_cookies_brave_macos.py, extract_cookies_ios_emulation.py
Source:  analyzer.py, analyzer_eda.py - for amalgmation and concatenating features of extracted cookies data (for all scripts)

### Version 1.4 UPDATE - Released April 2026 ### 
Included additional Py cookie-scraping scripts for:  

1. Safari on MacOS (native browser environment):  extract_cookies_safari_macos.py 
2. Brave on WindowsOS:  extract_cookies_brave_windowsOS.py 

### Upcoming Additional Pipelines:  ###
1. Streamlit dashboards for master-data organisation and analytics (of extracted databases from the relevant scripts) 
2. New .py script  Windows-native browser IE (Internet Explorer) 

__________________________________________________________________________________________________________________________________________________

### PROJECT STRUCTURE & CONFIGURATION ###

```
- 'src/'       - Core analysis logic
- 'notebook/' - Jupyter notebooks for EDA reports and experiments
- 'scripts/'   - Standalone utilities for data extraction,fingerprinting, reporting
- 'data/'      - Sample outputs

browser-tracker-analyzer/
├── src/
│   ├── analyzer.py           # Core Python scripts
├── notebook/                 # Jupyter notebook of detailed analysis
│   ├── eda.ipynb
├── scripts                   # standalone utility scripts
│   ├── fingerprint.py        # Fingerprint detection functions
    └── report.py             # Report generation (JSON/CSV/HTML)
    └── extract_cookies_brave_macos.py
    └── extract_cookies_brave_windowsOS.py       
    └── extract_cookies_ios_emulation.py
    └── extract_cookies_safari_macos.py
    └── test.py                # confirms all relevant project libraries & dependencies
    └── compare_cookies.py     # (optional) future merge script 
├── data/
│   ├── brave_macos_cookies.csv   #CSV report derived from 'scripts/extract_cookies_macos.py'
│   └── brave_ios_cookies.csv     #CSV report derived from'scripts/extract_ios_emulation.py'
├── requirements.txt
├── README.md
```

### REQUIREMENTS AND DEPENDENCIES ###


See requirements.txt for full list.
**Key dependencies: Playwright, pandas, csv**
NOTE:  Adherence to the minimal versions listed for each dependency in 'requirement.txt' is highly recommended
for the desired results or outcome.



## Installation:
```
bash 
pip install -r  requirements.txt
playwright install  --with-deps
```

### QUICK START ###
```
bash
## Run macOS Brave cookie extraction
python3  scripts/extract_cookies_brave_macos.py

## Run macOS Safari cookie extraction
python3  scripts/extract_cookies_safari__macos.py 

## Run iOS emulation cookie extraction
python3  scripts/extracts/ioc/emulation.py

## Create EDA notebook for deeper visual presentation of cookie behaviour analytics (optional)
bash pip3 install jupyter  (if not in system)
Jupyter Notebook
```

### Next Steps
```
## Analysis Tools

Two versions available in `src/`:

- **analyzer.py**  
  Fast CLI tool to process CSVs and generate JSON/CSV/HTML reports.  
  ```bash
  python src/analyzer.py --mode csv --output analysis --format json
  OR
  cd ~/...filepath/PYTHONPATH=. python3 src/analyzer_eda.py --mode csv --output eda_test --format json

- **analyzer_eda.py**
  An extension of 'analyzer.py'. Interactive, scripted EDA version with summaries, stats, and plots.
  Run directly as shown above (bash).
```

## Sample Output

<img width="1229" height="687" alt="Screenshot 2026-02-24 at 2 56 46 pm" src="https://github.com/user-attachments/assets/d7884dd2-b492-46fc-912e-52e22e00a5b8" />


### FUTURE ROADMAP ###
```
*  Multi-browser comparison (Chrome, Firefox, Brave,Safari, etc) 
*  Inclusion of Windows and Android OS
*  Inter OS comparision, e.g quantity & prevalence of cookies in Brave / Firefox running in Windows vs MacOS)
*  Advanced EDA visualizations (matplotlib/seaborn)
*  Machine learning pipelines (clustering + invasiveness prediction)
*  Database storage (SQLite)
*  Web dashboard
```

### LICENSE ###
```
MIT License
```

### Contact ###

Built by JLL<br>
Feedback and Suggestions welcome!
