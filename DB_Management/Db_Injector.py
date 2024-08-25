import os
import threading
import time
import sqlite3
from datetime import date, datetime
from DB_Management.DB_injection_universal import construct_sql_queries
from typing import Dict, Any, List
from EXCELL_file_management.Excell_management import add_rows_to_excell_file_openpyxl_2

import pandas as pd


#TODO elicit name form Name of Db url
Table_name = "OLX_scrapping_table"
def connect_to_database(database_path: str):

    if user_decision(database_path):

        try:
            conn = sqlite3.connect(database_path)
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None

# def DB_consistance_checker():
#     #TODO
#     print("DB_consistance_checker")

def data_injection(data: dict, connection_object=None):
    result = True  # Initialize result as True
    cursor = connection_object.cursor()
    table_name = Table_name  # get_today_table_name()

    Table_in_DB_creation_query, Query_to_insert_data = construct_sql_queries(table_name, data)

    try:

        cursor.execute(Table_in_DB_creation_query)

        # Prepare the SQL INSERT statement
        query = Query_to_insert_data

        # Execute the INSERT statement for each data row
        print("Query to Db: ", query, " data to put in query ", tuple(data.values()))
        cursor.execute(query, tuple(data.values()))#I ahve to carry values, I cpoudl do it because During Building data everything is adding in proper order according list and Query in Db is maekd according list with order as well


        # Insert data into the referenced table
        Add_Date_to_referenced_table(connection_object, data['Ads_id'])

        # Commit the changes to the database
        connection_object.commit()

    except sqlite3.Error as e:
        print("Error inserting data:", e)
        result = False  # Set result to False indicating failure

    finally:
        cursor.close()
        print("Element Correctly added")
        #connection_object.close()  # Close the database connection

    return result


# def data_injection(data: list, connection_object = None):
#     #TODO data_validation
#     cursor = connection_object.cursor()
#     table_name = Table_name #get_today_table_name()
#
#
#     #In belove example UC_Columns12 is constraint name
#     cursor.execute(f'''
#             CREATE TABLE IF NOT EXISTS {table_name} (
#                 Ads_id TEXT PRIMARY KEY,
#                 Title TEXT,
#                 Price INTEGER,
#                 Location TEXT,
#                 Area INTEGER,
#                 Price_per_meter2 INTEGER,
#                 URL TEXT,
#                 Validity INTEGER,
#                 CONSTRAINT Duplicate_restrainer UNIQUE (Ads_id, Title, URL)
#             )
#         ''')
#
#     # Commit the changes to the database
#     connection_object.commit()
#
#     # All data checks passed, data is valid
#     #data = [operation_date, operation_name, account_number, bank_category, amount, classified_marker]
#         # Prepare the SQL INSERT statement
#         query = f"INSERT INTO {table_name} (Ads_id ,Title, Price, Location, Area, Price_per_meter2, URL, Validity ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
#
#         try:
#
#             # Execute the INSERT statement for each data row
#             cursor.execute(query, data)
#
#         except sqlite3.Error as e:
#             print("Error inserting data to Main table:", e)
#             result = False # Return False indicating failure
#
#         try:
#             Add_Date_to_referenced_table(connection_object, data[0])
#
#         except sqlite3.Error as e:
#             print("Error inserting data to Referenced table : ", e)
#             result = False  # Return False indicating failure
#
#         try:
#             # Commit the changes to the database
#             connection_object.commit()
#         except sqlite3.Error as e:
#             print("Error inserting data Commit problem:", e)
#             result = False  # Return False indicating failure
#
#             #TODO adding to Db we need to make function for filtration what is down and named filter_and_send
#
#             # # Close the database connection
#             #connection_object.close()
#
#             return True  # Return True indicating successful insertion
#
#         except sqlite3.Error as e:
#             print("Error inserting data:", e)
#             result = False # Return False indicating failure
#
#
#
#     result = True
#     connection_object.close()
#     return result




def data_injection_by_url(data: list, url: str):
    """
    This is to give opportunity to USE URL to Db. To be universal
    Function inside is predicted to use, mainly in programme.

    :param data: Data to inject to DB
    :param url: URL to database
    :return: In return we get FALS is connection will not be established, or refer to data_injection(data: list, connection_object = None)
    """

    connection_data = connect_to_database(url)
    if connection_data != None:
        return data_injection(data, connection_data)
    return False

# def get_today_table_name():
#     # Get the current date
#     current_date = date.today().strftime("%Y_%m_%d")
#
#     # Create a new table name based on the current date
#     table_name = f"OLX_household_scrapping_{current_date}"
#
#     return table_name


# THIS IS REMOVED AS FilTRATION IS MOVED TO DataBase
# def duplication_checker(data: list, cursor: sqlite3.Cursor, Table: str):
#     return 1
#
#     #TODO we could do that by DbConstraint
#     # Extract the unique identifier from the data
#     #remove
#
#     unique_id = data[0]
#
#     # Check if a record with the same unique identifier already exists
#     cursor.execute(f'SELECT * FROM {Table} WHERE Ads_id = ?', (unique_id,))
#     existing_record = cursor.fetchone()
#
#     if existing_record:
#         print("Duplicated element")
#         #Add_Date_to_referenced_table()
#         return 0
#
#     else:
#         print("New element Added")
#         #TODO send SMS message
#         # Insert the new record into the database
#         return 1

def Add_Date_to_referenced_table(conn: sqlite3.Connection, Unique_id: str):
    # Create the cursor from the connection
    cursor = conn.cursor()
    current_data = date.today().isoformat()
    query = f"""CREATE TABLE IF NOT EXISTS Date_Observed (
    AdsDate TEXT,
    Ads_id TEXT PRIMARY KEY,
    FOREIGN KEY (Ads_id) REFERENCES {Table_name}(Ads_id)
);"""

    query_new_record = """INSERT INTO Date_Observed (AdsDate, Ads_id) VALUES (?, ?)"""

    #Making new table if not EXIST
    cursor.execute(query)

    print(current_data)
    print(date.today().isoformat())
    try:
        #Instering actual date to referenced table
        cursor.execute(query_new_record, (current_data, Unique_id))

    except Exception as e:
        print(f"""Error of printing to DB referenced table ocurred: {str(e)}""")

    # Commit the changes
    conn.commit()

    #TODO Finish adding Foregin key with dates to programme


def filter_new(connection: sqlite3.Connection, Price_MAX=None, Price_MIN=None, Area_MAX=None, Area_MIN=None, Price_per_meter2_MAX=None, Price_per_meter2_MIN=None ):

    cursor = connection.cursor()
    #In general to be independednt we coudl filter db about record from today date:
    Single_item_filtering_query = """SELECT OLX.*
    FROM OLX_scrapping_table AS OLX
    INNER JOIN (
        SELECT Ads_id, AdsDate
        FROM Date_Observed
        GROUP BY Ads_id
        HAVING COUNT(*) = 1
    ) AS DO ON OLX.Ads_id = DO.Ads_id
    """

    Single_item_filtering_query += f""" WHERE AdsDate = \"{datetime.today().date().strftime('%Y-%m-%d')}\""""

    # if isinstance(Price_per_meter2_MAX, int) and Price_per_meter2_MAX > 0:
    #     Single_item_filtering_query += f""" AND Price_per_meter2 < {Price_per_meter2_MAX}"""
    #
    # if isinstance(Area_MIN, int) and Area_MIN > 0:
    #     Single_item_filtering_query += f""" AND Area > {Area_MIN}"""
    #
    # if isinstance(Price_MAX, int) and Price_MAX > 0:
    #     Single_item_filtering_query += f""" AND Price < {Price_MAX}"""

    # Check and add filters for each argument
    if isinstance(Price_MAX, int) and Price_MAX > 0:
        Single_item_filtering_query += f" AND Price < {Price_MAX}"

    if isinstance(Price_MIN, int) and Price_MIN > 0:
        Single_item_filtering_query += f" AND Price > {Price_MIN}"

    if isinstance(Area_MAX, int) and Area_MAX > 0:
        Single_item_filtering_query += f" AND Area < {Area_MAX}"

    if isinstance(Area_MIN, int) and Area_MIN > 0:
        Single_item_filtering_query += f" AND Area > {Area_MIN}"

    if isinstance(Price_per_meter2_MAX, int) and Price_per_meter2_MAX > 0:
        Single_item_filtering_query += f" AND Price_per_meter2 < {Price_per_meter2_MAX}"

    if isinstance(Price_per_meter2_MIN, int) and Price_per_meter2_MIN > 0:
        Single_item_filtering_query += f" AND Price_per_meter2 > {Price_per_meter2_MIN}"

    print(Single_item_filtering_query)
    cursor.execute(Single_item_filtering_query)
    print(cursor.description)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

    add_rows_to_excell_file_openpyxl_2(r"C:\Users\PF_Server\PycharmProjects\OLX_WebScraping\General_Project_Files\Filtered_Flats.xlsx", rows, columns)

    return (rows, columns)

    #To dconsider is that this function will add record to Db and try to send it, or just build message na dthen try to send it

# # Example usage:
# if __name__ == "__main__":
#     db_connection = sqlite3.connect("C://Users//PF_Server//your_database.db")  # Replace with your database file name
#     filtered_data = filter_new(db_connection, price_limit=10000, flat_surface_down_limit=30, overall_price_limit=600000)
#
#     for row in filtered_data:
#         print(row)
#
#     db_connection.close()
def input_with_timeout(prompt, timeout):
    #timeout is in seconds
    print(prompt)
    result = [None]
    def get_input():
        result[0] = input()
    input_thread = threading.Thread(target=get_input)
    input_thread.start()
    input_thread.join(timeout)
    if input_thread.is_alive():
        print("Time is up!")
        return None
    else:
        return result[0]

def user_decision(path: str, timeout=60):
    # Check if the file and path exist
    if os.path.exists(path):
        return True
    else:

        #user_input = input_with_timeout(f"The file {path} does not exist. Do you want to create it? (Y/N): ", timeout)

        # if not user_input or user_input.strip().lower() != 'y':
        #     print("No valid input received within the timeout period or input was 'N'.")
        #     return False

        # User has responded with 'Y', create the file.
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write('')  # Write an empty string to create the file.
        print(f"File created at {path}")
        return True


