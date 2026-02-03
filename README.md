
# CONCEPT #
A tool that collects browser-cookie data, stores it in DB/CSV, performs it in Exploratory Data Analytics(EDA) to uncover common behavioural patterns(e.g. browser-tracking/spying, advertissents, domain-stalking,etc), and applies ML pipelines, such as clustering tracker type by behvioural and performace metrics, or predicting invasives ones, by potential and/or actual chracteristics. 


### What is this repository for? ###

This repository aims to build a powerful, Python-based browser cookie-tracking analytics tool, to study the extent of invasive behaviour and potential of exploitation for more sinister means such as surreptiious data-harvesting or web-scraping, by browser cookies.  It is intended to build awareness on the sheer volume of website trackers and spyware we deal with on a daily basis simply by being online. The results are compiled into a report, which is then further refined by ML pipelines categorizing tracker by cookie type, behaviour, and prediction by the extent of invasiveness. 

# 1. Browser Tracker Analyzer

A privacy-focused Python tool that:

- Collects browser cookie, storage, and tracker data across sessions and sites
- Stores results in CSV or a lightweight database (SQLite)
- Performs **Exploratory Data Analysis (EDA)** to uncover behavioural patterns (e.g., persistent cross-site tracking, advertising networks, domain stalking, fingerprinting)
- Applies **machine learning pipelines** to:
  - Cluster trackers by behavioural similarity and performance metrics
  - Predict potentially invasive trackers based on characteristics (e.g., lifetime, third-party count, storage usage)

Goal: Move beyond simple detection → understand and quantify how websites actually track users over time.
### Version 0.0 - 0.1 ###

```
### How do I get set up? ###


* Database configuration
* How to run tests
* Deployment instructions
```

### Configuration ###
```
├── analyzer.py             # Main logic + CLI entry
├── trackers.py             # Tracker list parser + detection 
├── fingerprint.py          # Fingerprint detecttion functions
├── report.py               # Report generation (JSON/CSV/HTML)
├── requirements.txt
├── README.md
├── tests/                  # Unit test results
```

### Dependencies ###
```
Please refer to the specified file "requirements.txt" for details.
NOTE:  Adherence to the minimal version listed in the .txt guide is strongly recommended for the desired results or outcome.
```

### Database configuration ###


### How to run tests ###


### Deployment Instructions 


### Contribution guidelines ###
``
* Writing tests
* Code review
* Other guidelines
```

### Who do I talk to? ###

* Repo owner or admin - Jacqueline L'aigle Liao 

