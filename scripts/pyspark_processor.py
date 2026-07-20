# Copyright (c) 2026. Jac LL
# All Rights Reserved. 
# Unauthorized use or distribution is prohibited.

from pyspark.sql import SparkSession
import pandas as pd


#collate csv masterlist from src scripts to prepare for processing

def process_with_pyspark(data_path):
    spark = SparkSession.builder.appName("CookieAnalysis").getOrCreate()
    df = spark.read.csv(data_path, header=True, inferSchema=True)

    #Example processing
    
    aggregated = df.groupby("domain").count()
    return aggregated.toPandas()      #Convert to pandas for Streamlit
