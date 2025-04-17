# Author: Aymone Kouame

# system modules
import os
import subprocess
import sys

from google.cloud import bigquery
client = bigquery.Client()


def create_bq_session():
    job_config = bigquery.QueryJobConfig(create_session = True) 
    query_job = client.query("""SELECT 1""", job_config = job_config)
    session_id = query_job.session_info.session_id
    print(f'''Session initiated. Session ID = {session_id}''')
          
    return session_id

def get_external_table_config(filename_in_bucket, bucket_dir = None, bucket =  None):
    
    if bucket == None:  bucket = os.getenv('WORKSPACE_BUCKET')
    if bucket_dir == None:  bucket_dir = ''
    ext = filename_in_bucket.split('.')[1].upper()
    external_table_config = bigquery.ExternalConfig(ext)
    external_table_config.source_uris = f'{bucket}/{bucket_dir}/{filename_in_bucket}'.replace('//','/').replace('gs:/','gs://')
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