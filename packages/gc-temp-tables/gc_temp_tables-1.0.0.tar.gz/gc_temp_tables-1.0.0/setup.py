from setuptools import setup, find_packages

setup(
    name='gc_temp_tables',
    version='1.0.0',
    author='Aymone Jeanne Kouame',
    author_email='aymone.jk@gmail.com',
    description= "Python utility for creating and querying temporary tables in Google Cloud Environments.",
    long_description= """
`gc_temp_tables` lets you easily create and query temporary tables within Google Cloud environments. The user has the option to work within a session and/or use external tables. The functions in `gc_temp_tables` are below:

 * `create_bq_session()`.
 * `get_external_table_config(filename_in_bucket)`.
 * `create_temp_table(query)`
 * `query_temp_table()`
 * `delete_temp_table()`.

More information, include code snippet at: https://github.com/AymoneKouame/data-science-utilities/blob/main/README.md#1---package-gc_temp_tables

`gc_temp_tables` was originally written to be used within the All of Us Researcher Workbench environment but can be used in other Google Cloud Environments.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Example code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1.install the package if not already done
pip install gc_temp_tables 

# 2. import the module
from gc_temp_tables import gc_temp_tables as gct

# 3. create/initialize a session 
session_id = gct.create_bq_session()

# 5. create a temporay table from an external file

## 5.a Grab external table configuration
ext_config = gct.get_external_table_config(filename_in_bucket='example.parquet')

## 5.b Create table
gct.create_temp_table(f'''CREATE TEMP TABLE example_table AS (SELECT * FROM example)'''
		   , ext_table_def_dic = {example: ext_config}, session_id = session_id)

# 6. query the table and join with another table in Google Big Query
df = gct.query_temp_table(f'''
	SELECT t.*,  age
	FROM example_table
	JOIN person USING(person_id)''', session_id = session_id)

# 7. Delete unused temp tables
df = gct.delete_temp_table('example_table', session_id = session_id)

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