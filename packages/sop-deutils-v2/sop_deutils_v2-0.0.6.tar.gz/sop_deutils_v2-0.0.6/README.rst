Yes4All SOP Utils Packages
==========================

This is a utils package served for SOP Data Analytics team at **Yes4All**. It contains various modules to work with **PostgreSQL, MinIO, Trino, Google API, Airflow, Telegram…**

--------------

Contents Overview
-----------------

.. contents::
   :depth: 3
   :local:

Install package
~~~~~~~~~~~~~~~

.. code-block:: bash

   $ pip install --upgrade sop-deutils

--------------

Modules usage
~~~~~~~~~~~~~

Airflow
^^^^^^^

**Use case:** When having a new scheduled task file on Airflow.

**Functional:**

Auto naming DAG ID and alerting failed DAG to Telegram:

- Sample code of base config Airflow ``dag`` file:

.. code-block:: python

    from airflow import DAG
    from airflow.decorators import task
    from sop_deutils.y4a_airflow import auto_dag_id, telegram_alert

    default_args = {
        "retries":  20,			# number times to retry when the task is failed
        "retry_delay": timedelta(minutes=7),			# time delay among retries
        "start_date": datetime(2023, 7, 14, 0, 0, 0),			# date that the DAG start to run 
        "owner": 'duikha',			# account name of DAG owner
        "on_failure_callback": telegram_alert,			# this contains function to alert to Telegram when the DAG/task is failed
        "execution_timeout": timedelta(hours=4),			# limit time the DAG run
    }

    dag = DAG(
        dag_id=auto_dag_id(),			# this contains function to name the DAG based on the file directory
        description='Sample DAG',			# description about the DAG
        schedule_interval="1 6 * * *",              # schedule for the DAG run
        default_args=default_args,			# default arguments contains dictionary of predefined params above
        catchup=False,			# If True, the DAG will backfill tasks from the start_date to current date
    )

    with dag:
        @task(owner='linhvu')       # account name of task owner. if not specified, the owner is the same as the DAG owner
        def function_1():
            ...

        @task(owner='trieuna')      # account name of task owner. if not specified, the owner is the same as the DAG owner
        def function_2():
            ...

        function_1() >> function_2()

-  List of account name can be found `here <https://docs.google.com/document/d/1jMouKkrJsqcGlxkgB1aJldGI-Osr3PYt3K1bwUM3I5c/edit?usp=sharing>`__.

--------------

GoogleSheet
^^^^^^^^^^^

**Use case:** When interacting with Google Sheet.

**Functional:**

2.1 initialize
''''''''''''''

Firstly, import GoogleSheet utils module class. If want to use personal credentials, provide the dictionary of credentials as value of parameter ``user_creds``.

.. code-block:: python

    from sop_deutils.gg_api.y4a_sheet import GGSheetUtils

    sheet_utils = GGSheetUtils(
        user_creds=None,
    )

2.2 ``create_spread_sheet``
'''''''''''''''''''''''''''

To create a new spread sheet, using ``create_spread_sheet`` method, it has the following parameters:

- ``sheet_name`` (required): Name of the sheet to create. **(str)**

- ``folder_id`` (optional): ID of the folder contains spreadsheet. The default value is ``None``. **(str)**

- ``share_to`` (optional): List of email to share the spreadsheet. The default value is ``[]``. **(list)**

The method will return the created spreadsheet id.

.. code-block:: python

    spread_sheet_id = sheet_utils.create_spread_sheet(
        sheet_name='your-sheet-name',
        folder_id='your-folder-id',
        share_to=['longnc@yes4all.com'],
    )

    print(spread_sheet_id)

Output:

.. code-block:: bash

    1vTjZOcRfd5eiF5Qo8DCha29Vdt0zvYP11XPbq54eCMg

2.3 ``list_all_work_sheets``
''''''''''''''''''''''''''''

To get all available worksheet of spreadsheet, using ``list_all_work_sheets`` method, it has the following parameter:

- ``sheet_id`` (required): Spreadsheet id. **(str)**

The method will return list all worksheets of spreadsheet.

.. code-block:: python

    ws_list = sheet_utils.list_all_work_sheets(
        sheet_id='your-sheet-id',
    )

    print(ws_list)

Output:

.. code-block:: bash

    ['Sheet1']


2.4 ``delete_work_sheet``
'''''''''''''''''''''''''

To delete specific worksheet of spreadsheet, using ``delete_work_sheet`` method, it has the following parameters:

- ``sheet_id`` (required): Spreadsheet id. **(str)**

- ``sheet_name`` (optional): Worksheet name. The default value is ``'Sheet1'``. **(str)**

.. code-block:: python

    sheet_utils.delete_work_sheet(
        sheet_id='your-sheet-id',
        sheet_name='your-sheet-name',
    )

2.5 ``clear_work_sheet``
''''''''''''''''''''''''

To clear all data of specific worksheet of spreadsheet, using ``clear_work_sheet`` method, it has the following parameters:

- ``sheet_id`` (required): Spreadsheet id. **(str)**

- ``sheet_name`` (optional): Worksheet name. The default value is ``'Sheet1'``. **(str)**

- ``delete_cells`` (optional): Whether to delete all cells. The default value is ``False``. **(bool)**

.. code-block:: python

    sheet_utils.clear_work_sheet(
        sheet_id='your-sheet-id',
        sheet_name='your-sheet-name',
    )

2.6 ``get_data``
''''''''''''''''

To get data from the given sheet, using ``get_data`` method, it has the following parameters:

- ``sheet_id`` (required): Spreadsheet id. **(str)**

- ``sheet_name`` (optional): Worksheet name. The default value is ``'Sheet1'``. **(str)**

- ``range_from`` (optional): The begining of the range of data from sheet to get. The default value is ``None``. If ``None``, the range from will be the first cell of the sheet. **(str)**

- ``range_to`` (optional): The end of the range of data from sheet to get. The default value is ``None``. If ``None``, the range to will be the last cell of the sheet. **(str)**

- ``columns_first_row`` (optional): Whether to convert the first row to columns. The default value is ``False``. **(bool)**

- ``auto_format_columns`` (optional): Whether format columns name of dataframe (lowercase, replace special characters with underscore...). The default value is ``False``. **(bool)**

The method will return the dataframe contains data from sheet.

.. code-block:: python

    df = sheet_utils.get_data(
        sheet_id='your-sheet-id',
        columns_first_row=True,
    )

    print(df)

Output:

.. code-block:: bash

    | Column1 Header | Column2 Header | Column3 Header |
    | ---------------| ---------------| ---------------|
    | Row1 Value1    | Row1 Value2    | Row1 Value3    |
    | Row2 Value1    | Row2 Value2    | Row2 Value3    |
    | Row3 Value1    | Row3 Value2    | Row3 Value3    |

2.7 ``insert_data``
'''''''''''''''''''

To insert data to the given sheet, using ``insert_data`` method, it has the following parameters:

- ``data`` (required): Dataframe containing data to insert. **(pd.DataFrame)**

- ``sheet_id`` (required): Spreadsheet ID. **(str)**

- ``sheet_name`` (optional): Worksheet name. The default value is ``'Sheet1'``. **(str)**

- ``from_row_index`` (optional): The index of the row from which to begin inserting. The default value is ``1``. **(int)**

- ``insert_column_names`` (optional): Whether to insert column names. The default value is ``False``. **(bool)**

- ``parse_input`` (optional): Whether to parse input values as if the user typed them into the UI. The default value is ``True``. **(bool)**

- ``pre_process`` (optional): Whether to process input based on the pre-defined function of DA. The default value is ``True``. **(bool)**

.. code-block:: python

    sheet_utils.insert_data(
        data=df,
        sheet_id='your-sheet-id',
        from_row_index=2,
        insert_column_names=False,
    )

2.8 ``update_data``
'''''''''''''''''''

To update data of the given sheet, using the ``update_data`` method, it has the following parameters:

- ``data`` (required): Dataframe containing data to update. **(pd.DataFrame)**

- ``sheet_id`` (required): Spreadsheet ID. **(str)**

- ``sheet_name`` (optional): Worksheet name. The default value is ``'Sheet1'``. **(str)**

- ``range_from`` (optional): The beginning of the range of data to update. The default value is ``'A1'``. **(str)**

- ``parse_input`` (optional): Whether to parse input values as if the user typed them into the UI. The default value is ``True``. **(bool)**

- ``pre_process`` (optional): Whether to process input based on the pre-defined function of DA. The default value is ``True``. **(bool)**

.. code-block:: python

    sheet_utils.update_data(
        data=new_df,
        sheet_id='your-sheet-id',
        range_from='A4',
    )

2.9 ``remove_data``
'''''''''''''''''''

To remove data from a specific range of the given sheet, using the ``remove_data`` method, it has the following parameters:

- ``sheet_id`` (required): Spreadsheet ID. **(str)**

- ``sheet_name`` (optional): Worksheet name. The default value is ``'Sheet1'``. **(str)**

- ``list_range`` (optional): List of data ranges to remove. The default value is ``['A1:Z1', 'A4:Z4']``. **(list)**

.. code-block:: python

    sheet_utils.remove_data(
        sheet_id='your-sheet-id',
        list_range=[
            'A2:D5',
            'E5:G6',
        ],
    )

2.10 ``add_work_sheet``
''''''''''''''''''''''''''

To add new worksheet from the given spreadsheet, using ``add_work_sheet`` method, it has the following parameters:

- ``title`` (required): Title of the new worksheet. **(str)**

- ``sheet_id`` (required): Spreadsheet id. **(str)**

- ``num_rows`` (optional): Number rows of the new worksheet. The default value is ``1000``. **(int)**

- ``num_cols`` (optional): Number columns of the new worksheet. The default value is ``26``. **(int)**

The method will return worksheet object that is compatible with **gspread** library. (This worksheet object will has the same attributes and methods as the **gspread** worksheet object)

.. code-block:: python

    ws = sheet_utils.add_work_sheet(
        title='New Work Sheet',
        sheet_id='your-sheet-id',
    )

2.11 ``get_spread_sheet_id``
''''''''''''''''''''''''''''''''

To get the spreadsheet id from the given spreadsheet title, using ``get_spread_sheet_id`` method, it has the following parameters:

- ``title`` (required): Title of the spreadsheet. **(str)**

- ``folder_id`` (optional): The id of folder that contains the spreadsheet. The default value is ``None``. **(str)**

The method will return the spreadsheet id.

.. code-block:: python

    sheet_id = sheet_utils.get_spread_sheet_id(
        title='Your Sheet Title',
    )

    print(sheet_id)

Output:

.. code-block:: bash

    'your-sheet-id'

2.12 ``open_spread_sheet_by_title``
''''''''''''''''''''''''''''''''''''''

To open the spreadsheet from the given spreadsheet title, using ``open_spread_sheet_by_title`` method, it has the following parameters:

- ``title`` (required): Title of the spreadsheet. **(str)**

- ``folder_id`` (optional): The id of folder that contains the spreadsheet. The default value is ``None``. **(str)**

The method will return spreadsheet object that is compatible with **gspread** library. (This spreadsheet object will has the same attributes and methods as the **gspread** spreadsheet object)

.. code-block:: python

    ss = sheet_utils.open_spread_sheet_by_title(
        title='Your Sheet Title',
    )

2.13 ``open_spread_sheet``
''''''''''''''''''''''''''''''''''''''

To open the spreadsheet from the given spreadsheet id, using ``open_spread_sheet`` method, it has the following parameters:

- ``sheet_id`` (required): ID of the spreadsheet. **(str)**

The method will return spreadsheet object that is compatible with **gspread** library. (This spreadsheet object will has the same attributes and methods as the **gspread** spreadsheet object)

.. code-block:: python

    ss = sheet_utils.open_spread_sheet(
        sheet_id='your-sheet-id',
    )

2.14 ``gspread_load_data``
''''''''''''''''''''''''''''''''''''''

To load data to the given sheet, using ``gspread_load_data`` method. This method is integrated with GSpread load data function that provides the high efficiency and convenience, it can be used as the alternative of two methods ``insert_data`` and ``update_data``, it has the following parameters:

- ``data`` (required): Dataframe containing data to load. **(pd.DataFrame)**

- ``sheet_id`` (required): Spreadsheet ID. **(str)**

- ``sheet_name`` (optional): Worksheet name. The default value is ``'Sheet1'``. **(str)**

- ``from_row`` (optional): Row at which to start loading the DataFrame. The default value is ``1``. **(int)**

- ``from_col`` (optional): Column at which to start loading the DataFrame. The default value is ``1``. **(int)**

- ``include_index`` (optional): Whether to include the DataFrame's index as an additional column. The default value is ``False``. **(bool)**

- ``include_column`` (optional): Whether to add a header row or rows before data with column names (if include_index is True, the index's name(s) will be used as its columns' headers). The default value is ``True``. **(bool)**

- ``resize_worksheet`` (optional): If True, changes the worksheet's size to match the shape of the provided DataFrame, if False, worksheet will only be resized as necessary to contain the DataFrame contents. The default value is ``False``. **(bool)**

- ``allow_formulas`` (optional): Whether to interprets ``=foo`` as a formula in cell values; otherwise all text beginning with ``=`` is escaped to avoid its interpretation as a formula. The default value is ``True``. **(bool)**

- ``string_escaping`` (optional): Determines when string values are escaped as text literals (by adding an initial ``'`` character) in requests to Sheets API, 3 parameter values are accepted: ('default': only escape strings starting with a literal ``'`` character. 'off': escape nothing; cell values starting with a ``'`` will be interpreted by sheets as an escape character followed by a text literal. 'full': escape all string values), the escaping done when allow_formulas=False (escaping string values beginning with ``=``) is unaffected by this parameter's value. The default value is ``'default'``. **(str)**

.. code-block:: python

    sheet_utils.gspread_load_data(
        data=df,
        sheet_id='your-sheet-id',
        sheet_name='Sheet1',
        from_row=3,
        from_col=4,
        include_index=True,
        include_column=True,
    )

2.15 ``protect_work_sheet``
''''''''''''''''''''''''''''''''''''''

To protect data of the given sheet, using ``protect_work_sheet`` method, it has the following parameters:

- ``spreadsheet_id`` (required): Spreadsheet ID. **(str)**

- ``worksheet_name`` (required): Worksheet name. **(str)**

- ``editors`` (optional): Dictionary of emails of user and group that can edit the sheet. The default value is ``{"users": [], "groups": []}``. **(dict)**

- ``start_col_index`` (optional): The zero-based index of start column to protect. The default value is ``None``. **(int)**

- ``end_col_index`` (optional): The zero-based index of end column to protect (not included). The default value is ``None``. **(int)**

- ``start_row_index`` (optional): The zero-based index of start row to protect. The default value is ``None``. **(int)**

- ``end_row_index`` (optional): The zero-based index of end row to protect (not included). The default value is ``None``. **(int)**

.. code-block:: python

    sheet_utils.protect_work_sheet(
        spreadsheet_id='your-sheet-id',
        worksheet_name='Sheet1',
        editors={
            "users": ['longnc@yes4all.com'],
            "groups": ['groupjkobiec@yes4all.com'],
        },
        start_col_index=0,
        end_col_index=3,
        start_row_index=0,
        end_row_index=10,
        # (example: A1:C10)
    )


2.16 ``duplicate_sheet``
''''''''''''''''''''''''''''''''''''''

To duplicate worksheet, using ``duplicate_sheet`` method, it has the following parameters:

- ``sheet_id`` (required): Spreadsheet ID. **(str)**

- ``source_sheet_id`` (required): Worksheet ID - gid. **(int)**

- ``new_sheet_name`` (required): The name of new sheet. **(str)**

- ``format_only`` (optional): Only duplicate the format of worksheet. The default value is ``False``. **(bool)**

.. code-block:: python

    work_sheet = sheet_utils.duplicate_sheet(
        sheet_id="your-sheet-id",
        source_sheet_id=1234567890,
        new_sheet_name="duplicate sheet",
        format_only=True
    )

--------------

MinIO
^^^^^

MinIO is an object storage, it is API compatible with the Amazon S3 cloud storage service. MinIO can be used as a **datalake** to store unstructured data (photos, videos, log files, backups, and container images) and structured data.

**Use case:** when need to store raw data or get raw data from datalake. Notes that the stored data extension must be ``.parquet`` .

**Notes about how to determine the** ``file_path`` **parameter in minIO when using this module:**

.. figure::
   https://lh3.googleusercontent.com/drive-viewer/AEYmBYTnHBUSHkf9nTE9TuXWpEh12YMfUvHp2If3pJnjiRlmw6kdhqPrrprI-zMmdgM4O5pvSR8q1u5m5-XNRCo4Mc4rKJ-J=s1600
   :alt: minIO file path

..

   For example, if the directory to the data file in minIO is as above, then the ``file_path`` is ``"/scraping/amazon_vendor/avc_bulk_buy_request/2023/9/24/batch_1695525619"`` (after removing bucket name, data storage mode, and data file extension).

**Functional:**

3.1 initialize
''''''''''''''

Firstly, import minIO utils module class.

.. code:: python

   from sop_deutils.datalake.y4a_minio import MinioUtils

   minio_utils = MinioUtils()

3.2 ``data_exist``
''''''''''''''''''

To check whether data exists in a storage directory, using the ``data_exist`` method, it has the following parameters:

- ``mode`` (required): The data storage mode. The value must be either ``'prod'`` or ``'stag'``. **(str)**

- ``file_path`` (required): The data directory to check. **(str)**

- ``bucket_name`` (optional): The name of the bucket to check. The default value is ``'sop-bucket'``. **(str)**

The method will return ``True`` if data exists; otherwise, it returns ``False``.

.. code-block:: python

    minio_utils.data_exist(
        mode='stag',
        file_path='your-data-path',
    )

Output:

.. code-block:: bash

    True

3.3 ``get_data_value_exist``
''''''''''''''''''''''''''''

To get the distinct values of a specified column of data in a data directory, using the ``get_data_value_exist`` method, it has the following parameters:

- ``mode`` (required): The data storage mode. The value must be either ``'prod'`` or ``'stag'``. **(str)**

- ``file_path`` (required): The data directory to get distinct values. **(str)**

- ``column_key`` (required): The column name to get distinct values. **(str)**

- ``bucket_name`` (optional): The name of the bucket to get distinct values. The default value is ``'sop-bucket'``. **(str)**

The method will return a list of distinct values.

.. code-block:: python

    minio_utils.get_data_value_exist(
        mode='stag',
        file_path='your-data-path',
        column_key='your-chosen-column',
    )

Output:

.. code-block:: bash

    ['value_1', 'value_2']

3.4 ``load_data``
'''''''''''''''''

To load data from a dataframe to storage, using the ``load_data`` method, it has the following parameters:

- ``data`` (required): Dataframe containing data to load. **(pd.DataFrame)**

- ``mode`` (required): The data storage mode. The value must be either ``'prod'`` or ``'stag'``. **(str)**

- ``file_path`` (required): The directory to load the data. **(str)**

- ``bucket_name`` (optional): The name of the bucket to load the data. The default value is ``'sop-bucket'``. **(str)**

.. code-block:: python

    minio_utils.load_data(
        data=df,
        mode='stag',
        file_path='your-data-path',
    )

3.5 ``get_data``
''''''''''''''''

To get data from a single file of a storage directory, using the ``get_data`` method, it has the following parameters:

- ``mode`` (required): The data storage mode. The value must be either ``'prod'`` or ``'stag'``. **(str)**

- ``file_path`` (required): The data directory to get data. **(str)**

- ``bucket_name`` (optional): The name of the bucket to get data. The default value is ``'sop-bucket'``. **(str)**

The method will return a dataframe containing the data to get.

.. code-block:: python

    df = minio_utils.get_data(
        mode='stag',
        file_path='your-data-path',
    )

    print(df)

Output:

.. code-block:: bash

    | Column1 Header | Column2 Header | Column3 Header |
    | ---------------| ---------------| ---------------|
    | Row1 Value1    | Row1 Value2    | Row1 Value3    |
    | Row2 Value1    | Row2 Value2    | Row2 Value3    |
    | Row3 Value1    | Row3 Value2    | Row3 Value3    |

3.6 ``get_data_wildcard``
'''''''''''''''''''''''''

To get data from multiple files in storage directories, using the ``get_data_wildcard`` method, it has the following parameters:

- ``mode`` (required): The data storage mode. The value must be either ``'prod'`` or ``'stag'``. **(str)**

- ``file_path`` (required): The parent data directory to get the data. **(str)**

- ``bucket_name`` (optional): The name of the bucket to get data. The default value is ``'sop-bucket'``. **(str)**

The method will return a dataframe containing the data to get.

.. code-block:: python

    df = minio_utils.get_data_wildcard(
        mode='stag',
        file_path='your-parent-data-path',
    )

    print(df)

Output:

.. code-block:: bash

    | Column1 Header | Column2 Header | Column3 Header |
    | ---------------| ---------------| ---------------|
    | Row1 Value1    | Row1 Value2    | Row1 Value3    |
    | Row2 Value1    | Row2 Value2    | Row2 Value3    |
    | Row3 Value1    | Row3 Value2    | Row3 Value3    |

--------------

PostgreSQL
^^^^^^^^^^

**Use case:** when interacting with Postgres database.

**Functional:**

4.1 initialize
''''''''''''''

Firstly, import PostgreSQL utils module class. This class has four parameters:

- ``account_name``: The shortcode of client account name to connect to PostgreSQL. The value can be used as DA member name. The default value is ``None``. If not provide, must use params ``pg_account`` and ``pg_password``. List of account name can be found `here <https://docs.google.com/document/d/1jMouKkrJsqcGlxkgB1aJldGI-Osr3PYt3K1bwUM3I5c/edit?usp=sharing>`__. **(str)**
- ``pg_name``: PostgreSQL db name to connect. Accepted values are ``'raw_master'``, ``'raw_repl'``, ``'serving_master'``, ``'serving_repl'``. **(str)**
- ``pg_account``: The client account to connect to PostgreSQL. The default value is ``None``. **(str)**
- ``pg_password``: The client password to connect to PostgreSQL. The default value is ``None``. **(str)**

.. code-block:: python

    from sop_deutils.sql.y4a_postgresql import PostgreSQLUtils

    pg_utils = PostgreSQLUtils(
        pg_name='serving_master',
        account_name='user1',
    )

    # or

    pg_utils = PostgreSQLUtils(
        pg_name='serving_master',
        pg_account='y4a_sop_user1',
        pg_password='password-of-user1',
    )

4.2 ``read_sql_file``
'''''''''''''''''''''

To get the SQL query from an SQL file, using the ``read_sql_file`` method, it has the following parameter:

- ``sql_file_path`` (required): The located path of the SQL file. **(str)**

The method will return the string representation of the SQL query.

.. code-block:: python

    sql = pg_utils.read_sql_file(
        sql_file_path='your-path/select_all.sql',
    )

    print(sql)

Output:

.. code-block:: bash

    SELECT * FROM your_schema.your_table

4.3 ``insert_data``
'''''''''''''''''''

To insert data into a PostgreSQL table, using the ``insert_data`` method, it has the following parameters:

- ``data`` (required): A dataframe containing the data to insert. **(pd.DataFrame)**

- ``schema`` (required): The schema containing the table to insert. **(str)**

- ``table`` (required): The name of the table to insert the data into. **(str)**

- ``ignore_errors`` (optional): Whether to ignore errors when inserting data. The default value is ``False``. **(bool)**

- ``commit_every`` (optional): The number of rows of data to commit each time. The default value is ``5000``. **(int)**

- ``db_pool_conn`` (optional): The connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

.. code-block:: python

    pg_utils.insert_data(
        data=your_df,
        schema='your-schema',
        table='your-table',
    )

4.4 ``bulk_insert_data``
''''''''''''''''''''''''

To insert a large amount of data into a PostgreSQL table and need high performance, using the ``bulk_insert_data`` method, it has the following parameters:

- ``data`` (required): A dataframe containing the data to insert. **(pd.DataFrame)**

- ``schema`` (required): The schema containing the table to insert. **(str)**

- ``table`` (required): The name of the table to insert the data into. **(str)**

- ``commit_every`` (optional): The number of rows of data to commit each time. The default value is ``5000``. **(int)**

- ``db_pool_conn`` (optional): The connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

.. code-block:: python

    pg_utils.bulk_insert_data(
        data=your_df,
        schema='your-schema',
        table='your-table',
    )

4.5 ``upsert_data``
'''''''''''''''''''

To upsert data in a PostgreSQL table, using the ``upsert_data`` method, it has the following parameters:

- ``data`` (required): A dataframe containing the data to upsert. Note that if the dataframe contains duplicated rows, they will be dropped. **(pd.DataFrame)**

- ``schema`` (required): The schema containing the table to upsert. **(str)**

- ``table`` (required): The name of the table to upsert the data into. **(str)**

- ``where_conditions`` (optional): A string of a query that uses conditions to update. The default value is ``None``. **(str)**

- ``ignore_existence`` (optional): Whether to insert only new transactions and ignore existing transactions. The default value is ``False``. **(bool)**

- ``commit_every`` (optional): The number of rows of data to commit each time. The default value is ``5000``. **(int)**

- ``db_pool_conn`` (optional): The connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

.. code-block:: python

    pg_utils.upsert_data(
        data=your_df,
        schema='your-schema',
        table='your-table',
    )

4.6 ``bulk_upsert_data``
''''''''''''''''''''''''

To upsert large data to a PostgreSQL table and need high performance, using the ``bulk_upsert_data`` method, it has the following parameters:

- ``data`` (required): A DataFrame containing data to upsert. If the DataFrame contains duplicated rows, they will be dropped. **(pd.DataFrame)**

- ``schema`` (required): The schema containing the table to upsert. **(str)**

- ``table`` (required): The name of the table to upsert the data into. **(str)**

- ``where_conditions`` (optional): A string of a query that uses conditions to update. The default value is ``None``. **(str)**

- ``ignore_existence`` (optional): Whether to insert only new transactions and ignore existing transactions. The default value is ``False``. **(bool)**

- ``commit_every`` (optional): The number of rows of data to commit each time. The default value is ``5000``. **(int)**

- ``db_pool_conn`` (optional): The connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

.. code-block:: python

    pg_utils.bulk_upsert_data(
        data=your_df,
        schema='your-schema',
        table='your-table',
    )

4.7 ``update_table``
''''''''''''''''''''

To update new data of specific columns in a table based on primary keys, using the ``update_table`` method, it has the following parameters:

- ``data`` (required): A DataFrame containing data to update, including primary keys and columns to update. **(pd.DataFrame)**

- ``schema`` (required): The schema containing the table to update data. **(str)**

- ``table`` (required): The table to update data. **(str)**

- ``columns`` (required): A list of column names to update data. **(list)**

- ``commit_every`` (optional): The number of rows of data to commit each time. The default value is ``5000``. **(int)**

- ``db_pool_conn`` (optional): A connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

.. code-block:: python

    pg_utils.update_table(
        data=your_df,
        schema='your-schema',
        table='your-table',
        columns=['col1', 'col2'],
    )

4.8 ``get_data``
''''''''''''''''

To get data from a PostgreSQL database using a SQL query, use the ``get_data`` method. This method has the following parameters:

- ``sql`` (required): SQL query to get data. **(str)**

- ``db_pool_conn`` (optional): A connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

The method will return a dataframe that contains data extracted by the given SQL query.

Here's how to use the ``get_data`` method in Python:

.. code-block:: python

    df = pg_utils.get_data(
        sql='your-query',
    )

    print(df)

Output:

.. code-block:: bash

    | Column1 Header | Column2 Header | Column3 Header |
    | ---------------| ---------------| ---------------|
    | Row1 Value1    | Row1 Value2    | Row1 Value3    |
    | Row2 Value1    | Row2 Value2    | Row2 Value3    |
    | Row3 Value1    | Row3 Value2    | Row3 Value3    |

4.9 ``select_distinct``
'''''''''''''''''''''''

To retrieve the distinct values of a specified column in a PostgreSQL table, use the ``select_distinct`` method, it has the following parameters:

- ``col`` (required): Column name to get the distinct data.. **(str)**

- ``schema`` (required): Schema contains table to get data. **(str)**

- ``table`` (required): Table to get data. **(str)**

- ``db_pool_conn`` (optional): A connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

The method will return a list of distinct values from the specified column.

.. code-block:: python

    distinct_values = pg_utils.select_distinct(
        col='chosen-column',
        schema='your-schema',
        table='your-table',
    )

    print(distinct_values)

Output:

.. code-block:: bash

    ['val1', 'val2', 'val3']

4.10 ``show_columns``
'''''''''''''''''''''

To retrieve a list of column names for a specific PostgreSQL table, use the ``show_columns`` method. It has the following parameters:

- ``schema`` (required): The schema that contains the table from which to retrieve columns. **(str)**

- ``table`` (required): The name of the table from which to retrieve columns. **(str)**

- ``db_pool_conn`` (optional): A connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

The method will return a list of column names for the specified table.

.. code-block:: python

    col_names = pg_utils.show_columns(
        schema='your-schema',
        table='your-table',
    )

    print(col_names)

Output:

.. code-block:: bash

    ['col1', 'col2', 'col3']

4.11 ``execute``
''''''''''''''''

To execute a given SQL query, use the ``execute`` method. It has the following parameters:

- ``sql`` (required): The SQL query to execute. **(str)**

- ``fetch_output`` (optional): Whether to fetch the results of the query. The default value is ``False``. **(bool)**

- ``db_pool_conn`` (optional): A connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

The method will return a list of query output if ``fetch_output`` is ``True``, otherwise ``None``.

.. code-block:: python

    sql = """
        UPDATE
            sales_order_avc_di o,
            (
                SELECT
                    DISTINCT po_name, 
                    asin,
                    CASE
                        WHEN o.status LIKE '%cancel%' AND a.status IS NULL THEN ''
                        WHEN o.status LIKE '%cancel%' THEN CONCAT(a.status,' ',cancel_date) 
                        ELSE o.status END po_asin_amazon_status
                FROM
                    sales_order_avc_order_status o
                    LEFT JOIN
                        sales_order_avc_order_asin_status a USING (updated_at, po_name)
                WHERE updated_at > DATE_SUB(NOW(), INTERVAL 1 DAY)
            ) s
        SET
            o.po_asin_amazon_status = s.po_asin_amazon_status
        WHERE
            o.po_name = s.po_name
            AND o.asin = s.asin
    """

    pg_utils.execute(
        sql=sql,
    )

4.12 ``add_column``
'''''''''''''''''''

To add a new column to a specific PostgreSQL table, use the ``add_column`` method. It has the following parameters:

- ``schema`` (required): The schema containing the table to create the column. **(str)**

- ``table`` (required): The name of the table to create the column. **(str)**

- ``column_name`` (optional): The name of the column to create (available when creating a single column). The default value is ``None``. **(str)**

- ``dtype`` (optional): The data type of the column to create (available when creating a single column). The default value is ``None``. **(str)**

- ``multiple_columns`` (optional): A dictionary containing column names as keys and their corresponding data types as values (available when creating multiple columns). The default value is an empty dictionary. **(dict)**

- ``db_pool_conn`` (optional): A connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

.. code-block:: python

    pg_utils.add_column(
        schema='your-schema',
        table='your-table',
        multiple_columns={
            'col1': 'int',
            'col2': 'varchar(50)',
        },
    )

4.13 ``create_table``
'''''''''''''''''''''

To create a new table in a PostgreSQL database, use the ``create_table`` method. It has the following parameters:

- ``schema`` (required): The schema containing the table to create. **(str)**

- ``table`` (required): The name of the table to create. **(str)**

- ``columns_with_dtype`` (required): A dictionary containing column names as keys and their corresponding data types as values. **(dict)**

- ``columns_primary_key`` (optional): A list of columns to set as primary keys. The default value is ``[]``. **(list)**

- ``columns_not_null`` (optional): A list of columns to set as "not null" constraints. The default value is ``[]``. **(list)**

- ``columns_with_default`` (optional): A dictionary containing column names as keys and their default values as values. The default value is an empty dictionary. **(dict)**

- ``db_pool_conn`` (optional): A connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

Notes that table will be automatically granted privileges following the rules after creating.

.. code-block:: python

    pg_utils.create_table(
        schema='your-schema',
        table='your-new-table',
        columns_with_dtype={
            'col1': 'int',
            'col2': 'varchar(50)',
            'col3': 'varchar(10)',
        },
        columns_primary_key=[
            'col1',
        ],
        columns_not_null=[
            'col2',
        ],
        columns_with_default={
            'col3': 'USA',
        },
    )

4.14 ``auto_grant``
''''''''''''''''''''

To grant table privileges to users in PostgreSQL, use the ``auto_grant`` method. It has the following parameters:

- ``schema`` (required): The schema containing the table to grant. **(str)**

- ``list_tables`` (required): A list of tables name to grant. **(list)**

- ``list_users`` (optional): A list of users to grant access. The default value is ``None``. If ``None``, the table will be granted for all the predefined users. **(list)**

- ``privileges`` (optional): A list of privileges to grant. The default value is ``['SELECT']``. Accepted values in the privileges list are: ``'SELECT'``, ``'INSERT'``, ``'UPDATE'``, ``'DELETE'``, ``'TRUNCATE'``, ``'REFERENCES'``, ``'TRIGGER'``. **(list)**

- ``all_privileges`` (optional): Whether to grant all privileges. The default value is ``False``. **(bool)**

.. code-block:: python

    pg_utils.auto_grant(
        schema='your-schema',
        list_tables=['your-new-table'],
        list_users=[
            'linhvk',
            'trieuna',
        ],
        privileges=[
            'SELECT',
            'INSERT',
            'UPDATE',
        ],
    )

4.15 ``truncate_table``
'''''''''''''''''''''''

To remove all the data from a PostgreSQL table, use the ``truncate_table`` method. It has the following parameters:

- ``schema`` (required): The schema containing the table to truncate. **(str)**

- ``table`` (required): The table name to truncate. **(str)**

- ``reset_identity`` (optional): Whether to reset the identity of the table. The default value is ``False``. **(bool)**

- ``db_pool_conn`` (optional): A connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

.. code-block:: python

    pg_utils.truncate_table(
        schema='your-schema',
        table='your-table',
    )

4.16 ``table_exists``
'''''''''''''''''''''

To check if the PostgreSQL table exists in the database, use the ``table_exists`` method. It has the following parameters:

- ``schema`` (required): The schema containing the table to check. **(str)**

- ``table`` (required): The table name to check. **(str)**

- ``db_pool_conn`` (optional): A connection pool to connect to the database. The default value is ``None``. If the value is ``None``, a new connection will be created and automatically closed after being used. **(callable)**

The method will return ``True`` if the table exists and ``False`` if it does not.

.. code-block:: python

    pg_utils.table_exists(
        schema='your-schema',
        table='your-exists-table',
    )

Output:

.. code-block:: bash

    True

4.17 ``coalesce``
'''''''''''''''''''''''

To coalesce missing values in a DataFrame based on a specified order of columns, use the ``coalesce`` method. It has the following parameters:

- ``data`` (required): The input DataFrame. **(pd.DataFrame)**

- ``columns_order`` (required): The order of columns for coalescing. **(list)**

The method will return a series representing the coalesced column.

.. code-block:: python

    df = pd.DataFrame(
        {
            'col1': [1, 2, None, 4, None],
            'col2': [None, 20, 30, None, 50],
            'col3': [10, 20, 30, 40, 50],
        }
    )

    df['coalesce'] = pg_utils.coalesce(
        data=df,
        columns_order=['col1', 'col2', 'col3'],
    )

    print(df[['coalesce']])

Output:

.. code-block:: bash

    | coalesce       |
    | ---------------|
    | 1.0            |
    | 2.0            |
    | 30.0           |
    | 4.0            |
    | 50.0           |

4.18 ``create_table_from_df``
'''''''''''''''''''''''''''''''

To create a new table in a PostgreSQL database which has predefined attributes based on Pandas dataframe, use the ``create_table_from_df`` method. It has the following parameters:

- ``data`` (required): Reference dataframe for table creation. **(pd.DataFrame)**

- ``schema`` (required): The schema containing the table to create. **(str)**

- ``table`` (required): The name of the table to create. **(str)**

Notes that table will be automatically granted privileges following the rules after creating.

.. code-block:: python

    df = pd.DataFrame(
        {
            'col1': [1, 2, None, 4, None],
            'col2': [None, 20, 30, None, 50],
            'col3': [10, 20, 30, 40, 50],
        }
    )

    pg_utils.create_table_from_df(
        data=df,
        schema='your-schema',
        table='your-new-table',
    )

--------------

Telegram
^^^^^^^^

**Use case:** When need to send messages to Telegram by using bot

**Functional:**

5.1 ``send_message``
'''''''''''''''''''''''''

To send messages to Telegram, using ``send_message`` method, it has the following parameters:

- ``text`` (required): Message to send. **(str)**

- ``bot_token`` (optional): Token of the bot which send the message. The default value is ``None``. If the value is ``None``, the bot ``sleep at 9pm`` will be used to send messages. **(str)**

- ``chat_id`` (optional): ID of group chat where the message is sent. The default value is ``None``. If the value is ``None``, the group chat ``Airflow Status Alert`` will be used. **(str)**

- ``parse_mode`` (optional): Sending mode, the accepted value is ``Markdown`` or ``HTML``. The default value is ``Markdown``. **(str)**

.. code-block:: python

    from sop_deutils.y4a_telegram import send_message

    send_message(
        text='Hello liuliukiki'
    )

5.2 ``send_data``
'''''''''''''''''''''''''

To send data to Telegram, using ``send_data`` method, it has the following parameters:

- ``data`` (required): Data to send. **(pd.DataFrame)**

- ``title`` (optional): The title of the message. The default value is ``None``. **(str)**

- ``bot_token`` (optional): Token of the bot which send the data. The default value is ``None``. If the value is ``None``, the bot ``sleep at 9pm`` will be used to send data. **(str)**

- ``chat_id`` (optional): ID of group chat where the data is sent. The default value is ``None``. If the value is ``None``, the group chat ``Airflow Status Alert`` will be used. **(str)**

- ``parse_mode`` (optional): Sending mode, the accepted value is ``Markdown`` or ``HTML``. The default value is ``Markdown``. **(str)**

.. code-block:: python

    from sop_deutils.y4a_telegram import send_data

    send_data(
        data=my_df,
        title='Sample Data',
    )

--------------

GoogleChat
^^^^^^^^^^

**Use case:** When need to send messages to Google Chat space by using bot

**Functional:**

6.1 ``send_message``
'''''''''''''''''''''''''

To send messages to chat space of Google, using ``send_message`` method, it has the following parameters:

- ``webhook_url`` (required): Url of the webhook that is registered in the chat space. `How to create webhook <https://developers.google.com/chat/how-tos/webhooks#create_a_webhook>`__. **(str)**

- ``message`` (required): The content to send to the chat space. **(str)**

.. code-block:: python

    from sop_deutils.gg_api.y4a_chat import send_message

    send_message(
        webhook_url=f'https://chat.googleapis.com/v1/spaces/{SPACE_ID}/messages?key={KEY}&token={TOKEN}'
        message='Hello liuliukiki',
    )

6.2 ``send_data``
'''''''''''''''''''''''''

To send data to chat space of Google, using ``send_data`` method, it has the following parameters:

- ``webhook_url`` (required): Url of the webhook that is registered in the chat space. `How to create webhook <https://developers.google.com/chat/how-tos/webhooks#create_a_webhook>`__. **(str)**

- ``data`` (required): Data to send. **(pd.DataFrame)**

- ``title`` (optional): The title of the message. The default value is ``None``. **(str)**

.. code-block:: python

    from sop_deutils.gg_api.y4a_chat import send_data

    send_data(
        webhook_url=f'https://chat.googleapis.com/v1/spaces/{SPACE_ID}/messages?key={KEY}&token={TOKEN}'
        data=my_df,
        title='Sample Data',
    )

6.3 ``send_image_widget``
'''''''''''''''''''''''''

To send image with widget to chat space of Google, using ``send_image_widget`` method, it has the following parameters:

- ``webhook_url`` (required): Url of the webhook that is registered in the chat space. `How to create webhook <https://developers.google.com/chat/how-tos/webhooks#create_a_webhook>`__. **(str)**

- ``image_url`` (required): The url of the image. **(str)**

.. code-block:: python

    from sop_deutils.gg_api.y4a_chat import send_image_widget

    send_image_widget(
        webhook_url=f'https://chat.googleapis.com/v1/spaces/{SPACE_ID}/messages?key={KEY}&token={TOKEN}'
        image_url='https://example.com/path/to/image.jpg',
    )

--------------

GoogleMail
^^^^^^^^^^

**Use case:** when need to send email to group of people.

**Functional:**

7.1 initialize
''''''''''''''

Firstly, import GGMail utils module class. This class has two parameters:

- ``sender_email``: The email of sender. The default value is ``None``. If not provide, the email of DA team will be used. **(str)**
- ``sender_password``: The password email of sender. The default value is ``None``. If not provide, the email of DA team will be used. **(str)**

.. code-block:: python

    from sop_deutils.gg_api.y4a_mail import GGMailUtils

    mail_utils = GGMailUtils() # This utils will use email of DA team

    # or

    mail_utils = GGMailUtils(
        sender_email='user@domain.abc',
        sender_password='something',
    )

7.2 ``send_mail``
'''''''''''''''''''''

To send plain text email, using the ``send_mail`` method, it has the following parameter:

- ``receiver_email`` (required): List of people to receive email. **(list)**

- ``content`` (required): The content of email. **(str)**

- ``cc_email`` (optional): List of people to receive CC. The default value is ``None``. **(list)**

- ``subject`` (optional): The subject of email. The default value is ``None``. **(str)**

.. code-block:: python

    mail_utils.send_mail(
        receiver_email=['user1@domain.abc', 'user2@domain.abc'],
        content='j ai biec',
    )

7.3 ``send_mail_w_attachments``
'''''''''''''''''''''''''''''''''''

To send email with attachments, using the ``send_mail_w_attachments`` method, it has the following parameters:

- ``receiver_email`` (required): List of people to receive email. **(list)**

- ``content`` (required): The content of email. **(str)**

- ``attachment_path`` (required): List of file path to attach. **(list)**

- ``cc_email`` (optional): List of people to receive CC. The default value is ``None``. **(list)**

- ``subject`` (optional): The subject of email. The default value is ``None``. **(str)**

.. code-block:: python

    mail_utils.send_mail_w_attachments(
        receiver_email=['user1@domain.abc', 'user2@domain.abc'],
        content='j ai biec',
        attachment_path=['parent_dir/file1.xlsx', 'parent_dir/file2.xlsx'],
    )

7.4 ``send_mail_w_pandas_df``
''''''''''''''''''''''''''''''''''

To send email with pandas dataframe as Excel file to group of people, using the ``send_mail_w_pandas_df`` method, it has the following parameters:

- ``receiver_email`` (required): List of people to receive email. **(list)**

- ``content`` (required): The content of email. **(str)**

- ``data_list`` (required): List of dataframe to attach. **(list)**

- ``file_name`` (required): List of file name respectively to list of dataframe. Notes that each file name must contain ``.xlsx``.  **(list)**

- ``cc_email`` (optional): List of people to receive CC. The default value is ``None``. **(list)**

- ``subject`` (optional): The subject of email. The default value is ``None``. **(str)**

.. code-block:: python

    df1 = pd.DataFrame([1, 2, 3], columns=['d1'])
    df2 = pd.DataFrame([4, 5, 6], columns=['d2'])

    mail_utils.send_mail_w_pandas_df(
        receiver_email=['user1@domain.abc', 'user2@domain.abc'],
        content='j ai biec',
        data_list=[df1, df2],
        file_name=['data1.xlsx', 'data2.xlsx'],
    )

--------------

Trino
^^^^^

Trino is a distributed SQL query engine designed to query large datasets across various data sources.

**Use case:** when need to move data between various data system like Apache Iceberg, PostgreSQL, MySQL..

**Functional:**

8.1 initialize
''''''''''''''

Firstly, import Trino utils module class. This class has four parameters:

- ``account_name``: The shortcode of client account name to connect to Trino. The default value is ``sop_dev``. **(str)**
- ``trino_host``: The host of trino. The default value is ``sop-trino.yes4all.internal``. **(str)**
- ``trino_account``: The client account to connect to Trino if not use the default account name. The default value is ``''``. **(str)**
- ``trino_password``: The client password to connect to Trino if not use the default account name. The default value is ``''``. **(str)**

.. code:: python

   from sop_deutils.sql.y4a_trino import TrinoUtils

   trino_utils = TrinoUtils()

8.2 ``get_data``
''''''''''''''''''

To get data from specific data system, using the ``get_data`` method, it has the following parameters:

- ``sql`` (required): SQL query to get data. **(str)**

The method will return a dataframe

.. code-block:: python

    df = trino_utils.get_data(
        sql="select * from catalog.schema.table",
    )

    print(df)

Output:

.. code-block:: bash

    | Column1 Header | Column2 Header | Column3 Header |
    | ---------------| ---------------| ---------------|
    | Row1 Value1    | Row1 Value2    | Row1 Value3    |
    | Row2 Value1    | Row2 Value2    | Row2 Value3    |
    | Row3 Value1    | Row3 Value2    | Row3 Value3    |

8.3 ``execute``
''''''''''''''''''''''''''''

To execute the given SQL query, using the ``execute`` method, it has the following parameters:

- ``sql`` (required): SQL query to execute. **(str)**

.. code-block:: python

    trino_utils.execute(
        sql="alter table catalog.schema.table set ..."
    )

8.4 ``iceberg_insert_data``
'''''''''''''''''''''''''''''''''''

To insert data from dataframe to Iceberg table, using the ``iceberg_insert_data`` method, it has the following parameters:

- ``data`` (required): Dataframe containing data to insert. **(pd.DataFrame)**

- ``schema`` (required): The destination schema. **(str)**

- ``table`` (required): The destination table. **(str)**

.. code-block:: python

    trino_utils.iceberg_insert_data(
        data=df,
        schema='my_schema',
        table='my_table',
    )

8.5 ``iceberg_upsert_data``
''''''''''''''''''''''''''''''''''''''

To upsert data from dataframe to Iceberg table, using the ``iceberg_upsert_data`` method, it has the following parameters:

- ``data`` (required): Dataframe containing data to insert. **(pd.DataFrame)**

- ``schema`` (required): The destination schema. **(str)**

- ``table`` (required): The destination table. **(str)**

- ``on_columns`` (required): List of columns to set match condition for update. **(list)**

- ``columns_to_update`` (optional): list of columns to update values based on ``on_columns`` param. The default value is ``None``, that all the columns will be updated. **(list)**

The method will return a dataframe containing the data to get.

.. code-block:: python

    trino_utils.iceberg_upsert_data(
        data=df,
        schema='my_schema',
        table='my_table',
        on_columns=['key_column_1', 'key_column_2'],
    )

--------------

GoogleDrive
^^^^^^^^^^^^

**Use case:** When need to upload file to Google Drive

**Functional:**

9.1 ``upload_file_to_gdrive``
''''''''''''''''''''''''''''''

To upload file to google drive, using ``upload_file_to_gdrive`` method, it has the following parameters:

- ``folder_name`` (required): The name of the folder where you will upload the file, It will be created if it does not exist. **(str)**

- ``parent_directory_id`` (required): Id of the folder containing folder_name in Google Drive. **(str)**

- ``path_name`` (required): The directory of file you want to upload. **(str)**

- ``file_name`` (required): The file name you want to upload (image.png, file.pdf, ...). **(str)**

- ``cred_file`` (optional): The service account credentials. **(dict)**

.. code-block:: python

    from sop_deutils.gg_api.y4a_drive import upload_file_to_gdrive

    upload_file_to_gdrive(
        folder_name = "Image Folder", 
        parent_directory_id = "1M1RD2JyzQLBv_lG4G************", 
        path_name="C:/Users/username/Documents/", 
        file_name="file_upload.pdf"
    )

--------------

Power BI Dashboard 
^^^^^^^^^^^^^^^^^^

**Use case:** when need to screenshot or get pdf file of Power BI dashboard.

**Functional:**

10.1 initialize
'''''''''''''''

Firstly, import DashboardService module class. This class has six parameters:

- ``acc_name``: The username of Power BI account. **(str)**
- ``acc_password``: The password email of Power BI account. **(str)**
- ``parent_directory_id``: The id of folder the file will be upload to get link. **(str)**
- ``executable_path``: The executable path of chromium PlayWright. If not provide, the default value will be used. **(str)**
- ``path_file``: The path where to put and get file in server when upload. The default value is ``/tmp/`` **(str)**
- ``creds_ggdrive``: The credentials of service account. If not provide, the default account of DA team will be used. **(dict)**

.. code-block:: python

    from y4a_project_demo.sop_deutils.y4a_dashboard import DashboardService

    dash_service = DashboardService(
        acc_name="username",
        acc_password="password",
        parent_directory_id = "1oX93BlXXlCwFhHCcSx*********"
    )

10.2 ``get_pdf_dashboard_get_link``
'''''''''''''''''''''''''''''''''''

To get pdf file of Power BI Dashboard, using the ``get_pdf_dashboard_get_link`` method, it has the following parameter:

- ``dashboard_url`` (required): The url of dashboard want to get pdf. **(str)**

- ``is_only_current_page`` (optional): The default is True. Get all tabs of dashboard or just get only current tab. **(bool)**

.. code-block:: python

    dash_service.get_pdf_dashboard_get_link(
        dashboard_url="https://app.powerbi.com/groups/me/apps/....."
    )

10.3 ``screenshot_dashboard_get_image_link``
''''''''''''''''''''''''''''''''''''''''''''

To screenshot of Power BI Dashboard, using the ``screenshot_dashboard_get_image_link`` method, it has the following parameters:

- ``dashboard_embed_url`` (required): The embed url of dashboard want to screenshot. File - Embed report - Website or portal - Copy the embed link. **(str)**

- ``height`` (required): The height of screen capture. **(float)**

- ``width`` (required): The width of screen capture. **(float)**

.. code-block:: python

    dash_service.screenshot_dashboard_get_image_link(
        dashboard_embed_url="https://app.powerbi.com/reportEmbed?reportId=.....", 
        height=1000, 
        width=1000
    )

--------------

All in one (DAConfig)
^^^^^^^^^^^^^^^^^^^^^

**Use case:** So far, there are a lot of platforms that needs to access frequently, in order not to import lots of modules, users can inherit all of above modules as simplest way.

**Functional:**

Firstly, import ``DAConfig`` class. This class has the following parameter:

- ``account_name``: The client account name to access platforms. The value can be used as DA member name. List of account name can be found `here <https://docs.google.com/document/d/1jMouKkrJsqcGlxkgB1aJldGI-Osr3PYt3K1bwUM3I5c/edit?usp=sharing>`__. **(str)**

.. code-block:: python

    from sop_deutils.base.y4a_da_cfg import DAConfig

    da_cfg = DAConfig(
        account_name='your-account-name'
    )

This class will have its attributes as all above modules (PostgreSQL, MinIO, Google API, Airflow, Telegram) that users don’t need to import and config to connect individually to each platform, each platform attributes will have the its own methods that listed above. List of attributes are:

- ``minio_utils``

- ``pg_raw_r_utils`` (connected to PostgreSQL raw read - repl)

- ``pg_raw_w_utils`` (connected to PostgreSQL raw write - master)

- ``pg_serving_r_utils`` (connected to PostgreSQL serving read - repl)

- ``pg_serving_w_utils`` (connected to PostgreSQL serving write - master)

- ``sheet_utils``

.. code-block:: python

    print(da_cfg.minio_utils)
    print(da_cfg.pg_raw_r_utils)
    print(da_cfg.pg_raw_w_utils)
    print(da_cfg.pg_serving_r_utils)
    print(da_cfg.pg_serving_w_utils)
    print(da_cfg.sheet_utils)

Output:

.. code-block:: bash

    <sop_deutils.datalake.y4a_minio.MinioUtils object at 0x7fe6e704d6f0>
    <sop_deutils.sql.y4a_postgresql.PostgreSQLUtils object at 0x7fe6e704d9f0>
    <sop_deutils.sql.y4a_postgresql.PostgreSQLUtils object at 0x7fe6e704dae0>
    <sop_deutils.sql.y4a_postgresql.PostgreSQLUtils object at 0x7fe6e704e170>
    <sop_deutils.sql.y4a_postgresql.PostgreSQLUtils object at 0x7fe6e704e0b0>
    <sop_deutils.gg_api.y4a_sheet.GGSheetUtils object at 0x7fe72c65e1d0>

--------------

Workflow example
~~~~~~~~~~~~~~~~

.. code-block:: python

    from datetime import datetime, timedelta
    from airflow import DAG
    from airflow.decorators import task
    import pandas as pd
    from sop_deutils.y4a_airflow import auto_dag_id, telegram_alert
    from sop_deutils.base.y4a_da_cfg import DAConfig

    owner = 'linhvu'

    cfg = DAConfig(owner)

    default_args = {
        "retries":  20,			# number times to retry when the task is failed
        "retry_delay": timedelta(minutes=7),			# time delay among retries
        "start_date": datetime(2023, 7, 14, 0, 0, 0),			# date that the DAG start to run 
        "owner": owner,			# account name of DAG owner
        "on_failure_callback": telegram_alert,			# this contains function to alert to Telegram when the DAG/task is failed
        "execution_timeout": timedelta(hours=4),			# limit time the DAG run
    }
    dag = DAG(
        dag_id=auto_dag_id(),			# this contains function to name the DAG based on the file directory
        description='Sample DAG',			# description about the DAG
        schedule_interval="1 6 * * *",              # schedule for the DAG run
        default_args=default_args,			# default arguments contains dictionary of predefined params above
        catchup=False,			# If True, the DAG will backfill tasks from the start_date to current date
    )

    with dag:
        @task
        def create_spreadsheet():
            spread_sheet_id = cfg.sheet_utils.create_spread_sheet(
                sheet_name='test_sheet_231020',
                share_to=['longnc@yes4all.com'],
            )

            return spread_sheet_id
        
        @task
        def insert_data_spreadsheet(spread_sheet_id):
            df = pd.DataFrame(
                [[1, 2, 3, 4]]*20,
                columns=['col1', 'col2', 'col3', 'col4']
            )

            cfg.sheet_utils.insert_data(
                data=df,
                sheet_id=spread_sheet_id,
                from_row_index=1,
                insert_column_names=True,
            )
        
        @task
        def process_data_spreadsheet(spread_sheet_id):
            cfg.sheet_utils.remove_data(
                sheet_id=spread_sheet_id,
                list_range=[
                    'A3:D3',
                    'A15:D15',
                ],
            )
        
        @task
        def etl_from_sheet_to_db(spread_sheet_id):
            df_from_sheet = cfg.sheet_utils.get_data(
                sheet_id=spread_sheet_id,
                columns_first_row=True,
            )

            df_from_sheet['total'] = df_from_sheet['col1'] + df_from_sheet['col2']\
                + df_from_sheet['col3'] + df_from_sheet['col4']
            df_from_sheet.dropna(inplace=True)
            for col in df_from_sheet.columns:
                df_from_sheet[col] = df_from_sheet[col].astype('int')
            
            cfg.pg_serving_w_utils.create_table(
                schema='y4a_sop_analyst',
                table='test_231020',
                columns_with_dtype={
                    'col1': 'int',
                    'col2': 'int',
                    'col3': 'int',
                    'col4': 'int',
                    'total': 'int',
                },
            )

            cfg.pg_serving_w_utils.insert_data(
                data=df_from_sheet,
                schema='y4a_sop_analyst',
                table='test_231020',
            )
        
        @task
        def execute_query():
            df_from_db = cfg.pg_serving_r_utils.get_data(
                sql='SELECT * FROM y4a_sop_analyst.test_231020',
            )
            print(df_from_db)

            cfg.pg_serving_w_utils.execute(
                sql='TRUNCATE TABLE y4a_sop_analyst.test_231020',
            )

        spread_sheet_id = create_spreadsheet()

        insert_data_spreadsheet(spread_sheet_id) \
            >> process_data_spreadsheet(spread_sheet_id) \
                >>  etl_from_sheet_to_db(spread_sheet_id) \
                    >> execute_query()

--------------

   provided by ``liuliukiki``
