
# CONCEPT #

1. [![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
2. [![Appium](https://img.shields.io/badge/Appium-2.0.0+-green)](https://appium.io/)
3. [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


A tool that collects browser-cookie data, stores it in DB/CSV, performs it in Exploratory Data Analytics(EDA) to uncover common behavioural patterns (e.g. browser-tracking/spying, advertissents, domain-stalking,etc), and applies ML pipelines, such as clustering tracker types by behvioural and performance metrices, or predicting invasive ones, by potential and actual chracteristics. 


### What is this repository for? ###

This repository aims to build a robust Python-based browser cookie-tracking analytics tool, to study the extent of invasive behaviour and potential for sinister exploitation such as surreptious data-harvesting, web-scraping et al, by browser cookies.  It is intended to build awareness on the sheer volume of website trackers and spyware users deal with on a daily basis simply by being online.  The results are compiled into reports, which are then further refined by ML pipelines categorizing tracker by cookie type, behaviour, and prediction by the extent of invasiveness, prevalance, and potential spyware/malware characteristics. 

# 1. Browser Tracker Analyzer

A privacy-focused Python tool that:

- Collects browser cookie, storage, and tracker data across sessions and sites
- Stores results in CSV or a lightweight database (SQLite)
- Performs **Exploratory Data Analysis (EDA)** to uncover behavioural patterns (e.g., persistent cross-site tracking, advertising networks, domain stalking, fingerprinting)
- Applies **machine learning pipelines** to:
  - Cluster trackers by behavioural similarity and performance metrics
  - Predict potentially invasive trackers based on characteristics (e.g., lifetime, third-party count, storage usage)

Goal: Move beyond simple detection → understand and quantify how websites actually track users over time.
### Version 1.0 ###


### 5-STEP PROJECT STRUCTURE ###

1. Configuration
```
browser-tracker-analyzer/
├── analyzer.py           # Main logic + CLI entry
├── trackers.py           # Tracker list parser + detection
├── fingerprint.py        # Fingerprint detection functions
├── report.py             # Report generation (JSON/CSV/HTML)
├── requirements.txt
├── README.md
└── tests/                # Optional: unit tests later
```

```
2. Dependencies 

Please refer to the specified file "requirements.txt" for details.
NOTE:  Adherence to the minimal version listed in the .txt guide is strongly recommended for the desired results or outcome.
```

```
3. Database configuration
```

```
4. How to run tests 
```


```
5. Deployment Instructions 
```

```
6. Contribution guidelines
```
* Writing tests
* Code review
* Other guidelines
```

### Who do I talk to? ###

* Repo owner or admin - Jacqueline L'aigle Liao 

