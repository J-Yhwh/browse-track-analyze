
# BROWSER TRACKER ANALYZER - CONCEPT 

__A privacy focused tool for understanding how websites track users across browsers and operating systems.__ 

### Goal
To understand, and visualize how browsers handle user tracking, raising awareness about digital privacy in real-world environments. 

### Key Highlights
- **Cross-platform consistency**: Extracts cookies from Safari(MacOS), Brave(MacOS & Windows), Microsoft Edge(Windows), and iOS browser simulation via Playwright. 
- **Privacy & Compliance Focus**:  Captures detailed cookie metadata(domain, name, value, path, secure, httpOnly, expiry, etc) - highly relevant to data protection, tracking transparency, and regulatory compliance. 
- **Clean Architecture**: Modular scripts, raw data output, and planned interactive dashboard.
- **Real-world skills**: Automation, data-scraping, cross-OS comparison, EDA, and privacy-conscious development. 

### Tech Stack 
- **Language**:  Python 3
- **Core Libraries**:  Pandas, Pathlib, Playwright, SQLite3
- **Visualisation (Upcoming)**: Streamlit + Matplotlib / Seaborn
- **Future Enhancements**:  Machine Learning for tracker pattern analysis and risk scoring 

### TECH STACK ###
1. [![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
2. [![Playwright](https://img.shields.io/badge/Playwright-1.48+-green)](https://playwright.dev/)
3. [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
4. ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
5. ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

---
### FEATURES
- Cross-platform cookie extraction (Brave, Safari, MS Edge, etc)
- Raw data export to CSV
- Breakdown of cookie and domain details, including security
- Streamlit dashboards for amalgamation of results for  comparison
- **Planning**: ML pipelines for tracker clustering and invasiveness prediction
__________________________________________________________________________________________________________________________________________________

### PROJECT STRUCTURE & CONFIGURATION ###

```
- 'src/'       - Core analysis logic
- 'notebook/'  - Jupyter notebooks for EDA reports and experiments
- 'scripts/'   - Standalone utilities for data extraction,fingerprinting, reporting
- 'data/'      - Sample outputs

browse-track-analyze/
├── src/
│   ├── analyzer.py           # Core Python scripts
├── notebook/                 # Jupyter notebook of detailed analysis
│   ├── eda.ipynb
├── scripts                   # standalone utility scripts
│   ├── fingerprint.py        # Fingerprint detection functions
    └── report.py             # Report generation (JSON/CSV/HTML)
    └── extract_cookies_brave_macos.py
    └── extract_cookies_brave_windowsOS.py 
    └── extract_cookies_brave_ios_emulate.py
    └── extract_cookies_safari_ios_emulate.py
    └── extract_cookies_safari_macos.py
    └── extract_cookies_IE_windowsOS.py
    └── test.py                # confirms all relevant project libraries & dependencies
    └── compare_cookies.py     # (optional) future merge script 
├── data/
│   ├── brave_cookies_raw.csv           #CSV report from 'scripts/extract_cookies_brave_windowsOS.py'
│   └── brave_ios_emulated_cookies.csv  #CSV report from 'scripts/extract_cookies_brave_ios_emulate.py'
│   └── brave_macos_cookies.csv         #CSV report from 'scripts/extract_cookies_brave_macos.py'
│   └── edge_cookies_raw.csv            #CSV report from 'scripts/extract_cookies_IE_windowsOS.py'
│   └── safari_cookies_full.csv         #CSV report from 'scripts/extract_cookies_safari_macos.py'
│   └── safari_ios_emulated_cookies.csv #CSV report from 'scripts/extract_cookies_safari_ios_emulate.py
├── app.py                    # Streamlit library - combines all CSV files in ```data/``` into dashboard for high-level presentation 
├── requirements.txt
├── README.md
```

### REQUIREMENTS AND DEPENDENCIES ###
See requirements.txt for full list.
**Key dependencies: CSV(SQLite), Pandas, Playwright, Streamlit** <br><br>
NOTE:  Adherence to the minimal versions listed for each dependency in 'requirement.txt' is highly recommended
for the desired results or outcome.

### DIRECTIONS: 
1. Install the required libraries and dependencies specified in requirements.txt (above) on your local machine. 
2. Surf the web on the different browsers specified (Brave(MacOS)/Brave(Windows)/MsEdge/Safari/iOS), within a **1-day timeframe** for each and **every** browser, on standard settings.
3. Download/branch ```browse-track-analyze``` onto your local machine/directory, and run the relevant scripts in Bash to extract cookies from the different browsers. The extracted .csv databases will be stored in the ```FILEPATH/browse-track-analyze/data``` folder of your local directory.


## Installation:
```
bash 
pip install -r  requirements.txt
playwright install  --with-deps
```

### QUICK START ###
```
bash
## Run MacOS Brave cookie extraction
FILEPATH/python3  scripts/extract_cookies_brave_macos.py

## Run MacOS Safari cookie extraction
FILEPATH/python3  scripts/extract_cookies_safari_macos.py 

## Run iOS emulation cookie extraction
FILEPATH/python3  scripts/extracts/ios/emulation.py

## Run Windows OS Brave cookie extraction
FILEPATH\python scripts\extract_cookies_brave_windowsOS.py

## Run Windows OS Microsoft Edge cookie extraction
FILEPATH\python scripts\extract_cookies_IE_windowsOS.py

## Create EDA notebook for deeper visual presentation of cookie behaviour analytics (optional)
bash pip3 install jupyter  (if not in system)
Jupyter Notebook
```

### Core Tools (src)
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

## Sample Outputs

**Brave on Windows - Powershell**
![Brave Windows raw Cookies](screenshots/brave_windows_success.png)

**Brave on MacOS - Terminal**
![Brave MacOS raw Cookies](screenshots/Terminal_Success_Brave.png)

**Safari on MacOS - Terminal**
![Safari MacOS raw Cookies](screenshots/Terminal_Success_Safari.png)

### UPDATES - VER. JUL 2026 ###

*  Created Streamlit dashboard with the addiion of Polars for consolidated, yet concise, summary and analysis of the amalgamated data
*  Dashboard includes inter-OS comparison, e.g quantity & prevalence of cookies in Brave vs Safari vs Explorer at al, running in Windows vs MacOS)
*  Advanced EDA visualizations (matplotlib/seaborn)
*  Machine learning pipelines (clustering + invasiveness prediction)

### FUTURE ROADMAP (LONG-TERM) ###
```
*  Addition of other browsers for scraping (Chrome, Firefox, Opera, etc)
*  Inclusion of Android OS
```

### LICENSE ###
```
MIT License
```

### Contact ###

Built by JLL<br>
**All images and screenshots in this repository are copyrighted.**<br>
Please **do not** download, copy, or use them without written permission.

