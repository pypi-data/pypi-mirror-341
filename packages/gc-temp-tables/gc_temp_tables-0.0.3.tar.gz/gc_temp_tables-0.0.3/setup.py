from setuptools import setup, find_packages

setup(
    name='gc_temp_tables',
    version='0.0.3',
    author='Aymone Jeanne Kouame',
    author_email='aymone.jk@gmail.com',
    description= "Python utility for data storage in Google Cloud Environments.",
    long_description= """
gc_temp_tables lets you easily create and query temporary tables within Google Cloud environments. The user has the option to do this within a session or not. The user can also call an external table. The typical steps are:

 * Optional: initiate a session, using `create_bq_session()`.

 * Optional: if using an external table (must be located in the Google Cloud bucket), get the external table configurations using `get_external_table_config(filename_in_bucket, bucket_dir).

 * Create a temporary table using `create_temp_table(query)`. The query must follow the format '''CREATE TEMP TABLE temp_table AS () '''. 
Options to add a session and/or an external table.

 * Query a temporary table using `query_temp_table()`.

 * Delete un-needed temporary table using `query_temp_table(f'DROP TABLE {table_to_drop}')`.

gc_temp_tables was originally written to be used within the All of Us Researcher Workbench environment but can be used in other Google Cloud Environments.

```
#install the package if not already done
##pip install gc_temp_tables 

#import
from gc_temp_tables import gc_temp_tables as gct

#create/initialize a session 
session_id = gct.create_bq_session()
```
""",

    long_description_content_type="text/markdown",
    url = 'https://github.com/AymoneKouame/data-science-utilities/gc_temp_tables/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    python_requires='>=3.6',
)