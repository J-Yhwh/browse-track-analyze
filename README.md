
# CONCEPT #

A tool that collects browser-cookie data, stores it in DB/CSV, performs it in Exploratory Data Analytics(EDA) to uncover common behavioural patterns (e.g. browser-tracking/spying, advertisements, domain-stalking,etc), and applies ML pipelines, such as clustering tracker types by prevalance, behavourial metrices, or predicting invasive ones, by potential and actual characteristics. 

This repository aims to build a robust Python-based browser cookie-tracking analytics tool, to study the extent of invasive behaviour and potential for sinister exploitation such as surreptitious data-harvesting, web-scraping et al, by browser cookies.  It is intended to build awareness on the sheer volume of website trackers and spyware users deal with daily simply by being online.  The results are compiled into reports, which are then further refined by ML pipelines categorizing tracker by cookie type, behaviour, and prediction by the extent of invasiveness, prevalence, and potential spyware or malware characteristics. 

### TOOLS ###

1. [![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
2. [![Playwright](https://img.shields.io/badge/Playwright-1.48+-green)](https://playwright.dev/)
3. [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



# Browser Tracker Analyzer

A privacy-focused Python tool that:

- Collects browser cookie, storage, and tracker data across sessions and sites
- Stores results in CSV or a lightweight database (SQLite)
- Performs **Exploratory Data Analysis (EDA)** to uncover behavioural patterns (e.g., persistent cross-site tracking, advertising networks, domain stalking, fingerprinting)
- Applies **machine learning pipelines** to:
  - Cluster trackers by behavioural similarity and performance metrics
  - Predict potentially invasive trackers based on characteristics (e.g., lifetime, third-party count, storage usage)

Goal: Move beyond simple detection → understand and quantify how websites actually track users over time.


### Version 1.0 ###

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
    └── extract_cookies_macos.py
    └── extract_cookies_ios_emulation.py
    └── compare_cookies.py     # (optional) future merge script
├── data/
│   ├── brave_macos_cookies.csv
│   └── brave_ios_cookies.csv
├── requirements.txt
├── README.md
```

### REQUIREMENTS AND DEPENDENCIES ###


See requirements.txt for full list.
Key dependencies: Playwright, pandas, csv
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
python3  scripts/extract_cookies_macos.py 

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
*  Multi-browser comparison (Chrome, Firefox, Brave)
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
