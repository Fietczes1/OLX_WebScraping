import time

import sys
import os

# Get the current script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Move one folder up in the directory structure
parent_directory = os.path.abspath(os.path.join(script_directory, os.pardir))

# Add the parent directory to sys.path
sys.path.insert(0, parent_directory)

from DB_Management.Db_Injector import data_injection_by_url, filter_new, connect_to_database
from SMS_Module.SMS_module import SMS_content_adjuster, add_line_to_string
from SMS_Module.SMS_primivtive import send_sms
from Scrapping_Houses import *
import argparse


def Argument_Parser():
    #ARGUMENT PRASING PART OF CODE TO ALLOW USAGE in CMD
    # Create an ArgumentParser
    parser = argparse.ArgumentParser(description="Web Scraping Script")

    # Add named arguments with default values set to None
    parser.add_argument("--URL", type=str, default=None, help="URL to scrape data from")
    parser.add_argument("--DB_url", type=str, default=None, help="URL or path to the database")
    parser.add_argument("--Element_to_extract", nargs='+', type=str, default=None, help="List of elements to extract")
    # Define a command-line argument for the dictionary
    parser.add_argument("--Limitation_Dict", nargs='+')
    args = parser.parse_args()

    # Convert the list from --my_dict into a dictionary
    Limitation_Dict = {args.Limitation_Dict[i]: int(args.Limitation_Dict[i + 1]) for i in range(0, len(args.Limitation_Dict), 2)}

    # Parse the command-line arguments
    return args, Limitation_Dict


    # # Print the arguments for verification
    # print("URL:", URL)
    # print("DB_url:", DB_url)
    # print("Elements_to_extract:", Elements_to_extract)

# sys.argv = [
#     "script_name.py",
#     "--URL",  r'https://www.olx.pl/oferty/q-Silnik-Bafang-BBS02/?search%5Bfilter_float_price:from%5D=500&search%5Bfilter_float_price:to%5D=1000',
#     "--DB_url", r'C:\Users\njvtwk\PycharmProjects\WebScrappingOLX\Bafang.db',
#     "--Element_to_extract", "Ads_id", "Title", "Price", "Location", "URL", "Validity",
#     "--Limitation_Dict", "Price_MAX", "1200", "Price_MIN", "600"
# ]

sys.argv = [
    r"C:/Users/Lenovo/PycharmProjects/OLX_WebScraping/General_Project_Files/Main_file.py",
    "--URL", "https://www.olx.pl/nieruchomosci/mieszkania/krakow/q-Mieszkanie/?search%5Bfilter_float_price:from%5D=300000",
    "--DB_url", r"C:/Users/Lenovo/PycharmProjects/OLX_WebScraping/DataBases/your_database.db",
    "--Element_to_extract", "Price", "Area", "Price_per_meter2",
    "--Limitation_Dict", "Price_MAX", "600000", "Area_MIN", "30", "Price_per_meter2_MAX", "11500", "Price_per_meter2_MIN", "8000"
]


if __name__ == "__main__":



    args, Limitation_Dict = Argument_Parser()

    # Access the named arguments
    if args.URL != None:
        URL = args.URL
    if args.DB_url != None:
        DB_url = args.DB_url
    if args.Element_to_extract != None:
        Elements_to_extract = args.Element_to_extract
    if Limitation_Dict:
        my_dict = Limitation_Dict
    else:
        my_dict = {}


    # Define the headers for the table
    headers = ["Title", "Price", "Location", "Area", "Price per meter2" , "URL"]

    #Data_To_store
    data = All_page_data_collector(URL)

    # Generate the table
    #printable_table = tabulate(data, headers, tablefmt="fancy_grid")

    for elements in data:
        elements['Validity'] = 1
        #TODO add date.today() to implement  principles of database normalization

        data_injection_by_url(elements, DB_url)

    #TODO change for automatic filter addition
    list_new_items = filter_new(connect_to_database(DB_url), **my_dict) #new  items according restriction

    if len(list_new_items) < 6:

        for index, item in enumerate(list_new_items):
            print(str(index + 1) + ". " + SMS_content_adjuster(item))
            send_sms('+48721776456', str(index + 1) + ". " + SMS_content_adjuster(item))
            time.sleep(5)
            send_sms('+48509520947', str(index + 1) + ". " + SMS_content_adjuster(item))

    else:
        message_text = str()
        for index, item in enumerate(list_new_items):
            message_text = add_line_to_string(str(index + 1), item[6],  message_text)
            if (index + 1) % 10 == 0 or index == len(list_new_items) - 1:
                print("text to send is: " + message_text)
                send_sms('+48721776456', message_text)
                time.sleep(5)
                send_sms('+48509520947', message_text)
                message_text = ""
    # # Print the table
    # print(table)