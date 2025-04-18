"""
Author: Aymone Jeanne Kouame
Date Released: 04/16/2025
Last Updated: 04/17/2025  
"""

import os
import subprocess
import sys

from google.cloud import bigquery
client = bigquery.Client()

def README():

    print("""
gc_temp_tables lets you easily create and query temporary tables within Google Cloud environments. 
The user has the option to do this within a session or not. The user can also call an external table. 
The typical steps are:

    - Optional: initiate a session, using `create_bq_session()`.

    - Optional: if using an external table (must be located in the Google Cloud bucket), 
    get the external table configurations using `get_external_table_config(filename_in_bucket, bucket_dir).

    - Create a temporary table using `create_temp_table(query)`. 
     The query must follow the format '''CREATE TEMP TABLE temp_table AS () '''. 
     Options to add a session_id and/or an external table.

    - Query a temporary table using `query_temp_table()`. The query can include a table in the BigQuery dataset.

    - Delete un-needed temporary table using `query_temp_table()`.

gc_temp_tables was originally written to be used within the All of Us Researcher Workbench environment but can be used in other Google Cloud Environments.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Code example ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# (1) Install the package if not already done
pip install gc_temp_tables 

# (2) Import functions
from gc_temp_tables import gc_temp_tables as gct

# (3) Create/initialize a session (or reuse a previous session)
session_id = gct.create_bq_session()

# (4) Create a temporary table using a file in the bucket

## 4.a get the table configuration. The default bucket is the Workspace bucket and the default directory is the root.
ext_config = gct.get_external_table_config('file_in_bucket.parquet')

## 4.b create the temp table. Multiple temporary table statements can be included in one query.
gct.create_temp_table('''CREATE TEMP TABLE temp_table AS (SELECT * FROM bucket_table)'''
                        , ext_table_def_dic = {'bucket_table': ext_config}, session_id = session_id
                     )

# (5) Query the temporary table
df = gct.query_temp_table('''
                    SELECT t.*
                    FROM temp_table t
                    JOIN cb_search_person USING(person_id)
                    WHERE has_ehr_data = 1
                    ''')
                    
# (5) Delete the temporary table
gct.delete_temp_table(temp_table = 'temp_table')

""")

def create_bq_session():
    job_config = bigquery.QueryJobConfig(create_session = True) 
    query_job = client.query("""SELECT 1""", job_config = job_config)
    session_id = query_job.session_info.session_id
    print(f'''Session initiated. Session ID = {session_id}''')
          
    return session_id

def get_external_table_config(filename_in_bucket, bucket_directory = None, bucket =  None):
    
    if bucket == None:  bucket = os.getenv('WORKSPACE_BUCKET')
    if bucket_directory == None:  bucket_directory = ''
    ext = filename_in_bucket.split('.')[1].upper()
    external_table_config = bigquery.ExternalConfig(ext)
    external_table_config.source_uris = f'{bucket}/{bucket_directory}/{filename_in_bucket}'.replace('//','/').replace('gs:/','gs://')
    external_table_config.autodetect = True #[bigquery.SchemaField('person_id', 'INTEGER') ]
    external_table_config.options.skip_leading_rows = 1
    
    return external_table_config

def create_temp_table(query, ext_table_def_dic = {}, session_id = None, dataset = os.getenv('WORKSPACE_CDR')):
    
    if session_id == None:
        job_config = bigquery.QueryJobConfig(default_dataset=dataset, table_definitions = ext_table_def_dic)
    
    else:
        job_config = bigquery.QueryJobConfig(default_dataset=dataset
                                             , connection_properties=[bigquery.ConnectionProperty("session_id", session_id)]
                                             , table_definitions = ext_table_def_dic)
        
    query_job = client.query(query, job_config = job_config)  # API request
    results = query_job.result()
    
    t = query_job.created
    print(f'Temp table(s) created on {t}.')    
    return results

def query_temp_table(query, ext_table_def_dic = {}, session_id = None, dataset = os.getenv('WORKSPACE_CDR')):
    
    if session_id == None:
        job_config = bigquery.QueryJobConfig(default_dataset=dataset, table_definitions = ext_table_def_dic)

    else:
        job_config = bigquery.QueryJobConfig(default_dataset=dataset
                                             , connection_properties=[bigquery.ConnectionProperty("session_id", session_id)]
                                             , table_definitions = ext_table_def_dic)
        
    query_job = client.query(query, job_config = job_config)  # API request
    df = query_job.result().to_dataframe()

    return df

def delete_temp_table(temp_table, ext_table_def_dic = {}, session_id = None, dataset = os.getenv('WORKSPACE_CDR')):
    
    if session_id == None:
        job_config = bigquery.QueryJobConfig(default_dataset=dataset, table_definitions = ext_table_def_dic)

    else:
        job_config = bigquery.QueryJobConfig(default_dataset=dataset
                                             , connection_properties=[bigquery.ConnectionProperty("session_id", session_id)]
                                             , table_definitions = ext_table_def_dic)
        
    query_job = client.query(f'''DROP TABLE {temp_table}''', job_config = job_config)  # API request
    df = query_job.result().to_dataframe()
    print(f'''Temp table {temp_table} deleted.''')

    return df