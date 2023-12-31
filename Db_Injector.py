
import sqlite3
from datetime import date, datetime

Table_name = "OLX_scrapping_table"
def connect_to_database(database_path: str):
    try:
        conn = sqlite3.connect(database_path)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def DB_consistance_checker():
    #TODO
    print("DB_consistance_checker")

def data_injection(data: list, connection_object=None):
    result = True  # Initialize result as True

    try:
        cursor = connection_object.cursor()
        table_name = Table_name  # get_today_table_name()

        cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    Ads_id TEXT PRIMARY KEY,
                    Title TEXT,
                    Price INTEGER,
                    Location TEXT,
                    Area INTEGER,
                    Price_per_meter2 INTEGER,
                    URL TEXT,
                    Validity INTEGER,
                    CONSTRAINT Duplicate_restrainer UNIQUE (Ads_id, Title, URL)
                )
            ''')

        # Prepare the SQL INSERT statement
        query = f"INSERT INTO {table_name} (Ads_id, Title, Price, Location, Area, Price_per_meter2, URL, Validity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

        # Execute the INSERT statement for each data row
        cursor.execute(query, data)

        # Insert data into the referenced table
        Add_Date_to_referenced_table(connection_object, data[0])

        # Commit the changes to the database
        connection_object.commit()

    except sqlite3.Error as e:
        print("Error inserting data:", e)
        result = False  # Set result to False indicating failure

    finally:
        connection_object.close()  # Close the database connection

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




def data_injection_by_url(data: list, url):
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

def get_today_table_name():
    # Get the current date
    current_date = date.today().strftime("%Y_%m_%d")

    # Create a new table name based on the current date
    table_name = f"OLX_household_scrapping_{current_date}"

    return table_name

def duplication_checker(data: list, cursor: sqlite3.Cursor, Table: str):
    return 1

    #TODO we could do that by DbConstraint
    # Extract the unique identifier from the data
    #remove

    unique_id = data[0]

    # Check if a record with the same unique identifier already exists
    cursor.execute(f'SELECT * FROM {Table} WHERE Ads_id = ?', (unique_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        print("Duplicated element")
        #Add_Date_to_referenced_table()
        return 0

    else:
        print("New element Added")
        #TODO send SMS message
        # Insert the new record into the database
        return 1

def Add_Date_to_referenced_table(conn: sqlite3.Connection, Unique_id: str):
    # Create the cursor from the connection
    cursor = conn.cursor()

    query = f"""CREATE TABLE IF NOT EXISTS Date_Observed (
    AdsDate TEXT,
    Ads_id TEXT PRIMARY KEY,
    FOREIGN KEY (Ads_id) REFERENCES {Table_name}(Ads_id)
);"""

    query_new_record = """INSERT INTO Date_Observed (AdsDate, Ads_id) VALUES (?, ?)"""

    #Making new table if not EXIST
    cursor.execute(query)

    try:
        #Instering actual date to referenced table
        cursor.execute(query_new_record, (date.today().isoformat(), Unique_id))

    except Exception as e:
        print(f"""Error of printing to DB ocurred: {str(e)}""")

    # Commit the changes
    conn.commit()

    #TODO Finish adding Foregin key with dates to programme

def filter_new(connection: sqlite3.Connection, price_limit = None, flat_surface_down_limit = None, overall_price_limit = None):

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

    if isinstance(price_limit, int) and price_limit > 0:
        Single_item_filtering_query += f""" AND Price_per_meter2 < {price_limit}"""

    if isinstance(flat_surface_down_limit, int) and flat_surface_down_limit > 0:
        Single_item_filtering_query += f""" AND Area > {flat_surface_down_limit}"""

    if isinstance(overall_price_limit, int) and overall_price_limit > 0:
        Single_item_filtering_query += f""" AND Price < {overall_price_limit}"""
    
    cursor.execute(Single_item_filtering_query)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    return rows

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