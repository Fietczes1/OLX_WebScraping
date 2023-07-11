
import sqlite3
from datetime import date

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

def data_injection(data: list, connection_object = None):
    #TODO data_validation
    cursor = connection_object.cursor()
    table_name = get_today_table_name()

    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                Ads_id TEXT,
                Title TEXT,
                Price INTEGER,
                Location TEXT,
                Area INTEGER,
                Price_per_meter2 INTEGER,
                URL TEXT,
                Validity INTEGER
            )
        ''')

    # Commit the changes to the database
    connection_object.commit()

    # All data checks passed, data is valid
    #data = [operation_date, operation_name, account_number, bank_category, amount, classified_marker]
    if duplication_checker(data, cursor, table_name):
        # Prepare the SQL INSERT statement
        query = f"INSERT INTO {table_name} (Ads_id ,Title, Price, Location, Area, Price_per_meter2, URL, Validity ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

        try:

            # Execute the INSERT statement for each data row
            cursor.execute(query, data)

            # Commit the changes to the database
            connection_object.commit()

            # # Close the database connection
            # connection_object.close()

            return True  # Return True indicating successful insertion

        except sqlite3.Error as e:
            print("Error inserting data:", e)
            return False  # Return False indicating failure

    else:

        return True


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
    # Extract the unique identifier from the data
    unique_id = data[0]

    # Check if a record with the same unique identifier already exists
    cursor.execute(f'SELECT * FROM {Table} WHERE Ads_id = ?', (unique_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        print("Duplicated element")
        Add_Date_to_referenced_table()
        return 0

    else:
        print("New element Added")
        # Insert the new record into the database
        return 1

def Add_Date_to_referenced_table(conector: sqlite3.Cursor, table_name: str):
    query = f"""CREATE TABLE Orders (
    AdsDate TEXT PRIMARY KEY,
    Ads_id TEXT,
    FOREIGN KEY (Ads_id) REFERENCES {table_name}(Ads_id)
);"""

    #TODO adding Foregin key with dates to programme
    pass
