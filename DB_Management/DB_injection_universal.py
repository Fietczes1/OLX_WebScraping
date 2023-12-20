
import sqlite3
from datetime import date, datetime
from typing import Dict, Any, List

def python_type_to_sql(python_type: type) -> str:
    """
    Convert Python data type to corresponding SQL data type.

    Parameters:
    - python_type: The Python data type.

    Returns:
    - The corresponding SQL data type as a string.
    """

    if python_type is int:
        return "INTEGER"
    elif python_type is float:
        return "REAL"
    elif python_type is str:
        return "TEXT"
    elif python_type is bool:
        return "INTEGER"  # SQLite uses INTEGER to store Boolean values
    else:
        return "BLOB"  # Default to BLOB for unsupported types


def construct_sql_queries(table_name: str, data_dict: Dict[str, Any]) -> (str, str):
    """
    Construct SQL CREATE TABLE and INSERT INTO queries based on the keys in the provided data dictionary.

    Parameters:
    - table_name: The name of the table in the database.
    - data_dict: The dictionary containing the data, with keys being column names and values being the data.

    Returns:
    - A tuple containing the CREATE TABLE and INSERT INTO queries as strings.
    """

    # Construct CREATE TABLE query
    fields = [f"{key} {python_type_to_sql(type(value))}" for key, value in data_dict.items()]
    fields_str = ",\n                    ".join(fields)

    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {fields_str},
            CONSTRAINT Duplicate_restrainer UNIQUE (Ads_id, Title, URL)
        )
    '''

    # Construct INSERT INTO query
    column_names = ", ".join(data_dict.keys())
    placeholders = ", ".join(["?"] * len(data_dict))

    insert_into_query = f'''
        INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})
    '''

    #print(create_table_query)
    #print(insert_into_query)
    return create_table_query, insert_into_query