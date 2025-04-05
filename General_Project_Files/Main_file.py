import pprint

import time
#GUI implementation
import multiprocessing
import atexit


import sys
import os

#29.01.2025
import logging
# Setup logging


LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "process_log.txt")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',handlers=[logging.FileHandler(LOG_FILE),
        logging.StreamHandler()], force = True)

loggerhandler = logging.getLogger()

# Function to log ALL uncaught exceptions
def log_unhandled_exceptions(exc_type, exc_value, exc_traceback):
    logging.error("Unhandled Exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = log_unhandled_exceptions

print(loggerhandler.handlers)



import site_grabber_and_AI_API # as it use logger implemented above

if site_grabber_and_AI_API.site_content_grabber.logger == loggerhandler:
    logging.info(f"logger number in both is the same {id(site_grabber_and_AI_API.site_content_grabber.logger)}")
else:
    logging.info(f"Main File logger {id(loggerhandler)}, AI logger is {id(site_grabber_and_AI_API.site_content_grabber.logger)}")

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
from GUI_for_live_management.GUI_Main import main as gui_main
from GUI_for_live_management.ObservableListClass import ObservableList
import argparse
from EXCELL_file_management.Excell_management import add_rows_to_excell_file_openpyxl_2



#GUI implementation
def start_gui(update_queue, stop_event):
    gui_main(update_queue, stop_event)

def list_changed(data):
    """ Places each dictionary from the data list into the queue.
    Waits for the queue to empty before sending the next item. """
    # Ensure data is iterable, treating a single dictionary as a list with one dictionary
    if isinstance(data, dict):
        data = [data]  # Convert a single dictionary into a list of one dictionary

    for item_number, item in enumerate(data, start=1):
        # Wait for the queue to empty before proceeding to the next item
        while not update_queue.empty():
            #print("Waiting for queue to empty...")
            time.sleep(0.1)  # Sleep and check again
        try:
            copy_of_item = item.copy()
            copy_of_item.update(lefted_elements=len(data) - item_number)
            update_queue.put(copy_of_item, timeout=2)  # Try to put item into the queue
            print(f"Item '{item['Title']}' put into the queue.")
        except multiprocessing.queues.Full:
            print("Queue is full, waiting...")
            time.sleep(0.2)  # Wait and try again




    #print(f"List changed: {data}")

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

# sys.argv = [
#     r"C:/Users/Lenovo/PycharmProjects/OLX_WebScraping/General_Project_Files/Main_file.py",
#     "--URL", "https://www.olx.pl/nieruchomosci/mieszkania/krakow/q-Mieszkanie/?search%5Bfilter_float_price:from%5D=300000",
#     "--DB_url",  "C:/Users/PF_Server/PycharmProjects/OLX_WebScraping/your_database.db", #r"C:/Users/Lenovo/PycharmProjects/OLX_WebScraping/DataBases/your_database.db",
#     "--Element_to_extract", "Price", "Area", "Price_per_meter2",
#     "--Limitation_Dict", "Price_MAX", "600000", "Area_MIN", "30", "Price_per_meter2_MAX", "11500", "Price_per_meter2_MIN", "8000"
# ]

# sys.argv = [
#     "C:/Users/PF_Server/PycharmProjects/OLX_WebScraping/General_Project_Files/Main_file.py",
#     "--URL", "https://www.olx.pl/nieruchomosci/mieszkania/krakow/?search%5Bdistrict_id%5D=463&search%5Bfilter_float_price:from%5D=300000",
#     "--DB_url",  "C:/Users/PF_Server/PycharmProjects/OLX_WebScraping/Database_Mistrzejowice.db",
#     "--Element_to_extract", "Price", "Area", "Price_per_meter2",
#     "--Limitation_Dict", "Price_MAX", "1000000", "Area_MAX", "60", "Area_MIN", "35", "Price_per_meter2_MAX", "20000", "Price_per_meter2_MIN", "11000"
# ]

# sys.argv = [
#     "C:/Users/PF_Server/PycharmProjects/OLX_WebScraping/General_Project_Files/Main_file.py",
#     "--URL", "https://www.olx.pl/nieruchomosci/mieszkania/krakow/?search[district_id]=281&search[filter_float_price:from]=300000",
#     "--DB_url",  "C://Users//PF_Server//PycharmProjects//OLX_WebScraping//Database_Wzgorza_Krzeslawickie.db",
#     "--Element_to_extract", "Price", "Area", "Price_per_meter2",
#     "--Limitation_Dict", "Price_MAX", "1000000", "Area_MAX", "60", "Area_MIN", "35", "Price_per_meter2_MAX", "20000", "Price_per_meter2_MIN", "11000"
# ]

# sys.argv = [
#     "C:/Users/PF_Server/PycharmProjects/OLX_WebScraping/General_Project_Files/Main_file.py",
#     "--URL", "https://www.olx.pl/nieruchomosci/mieszkania/krakow/q-Mieszkanie/?search%5Bfilter_float_price%3Afrom%5D=300000",
#     "--DB_url",  "C://Users//PF_Server//PycharmProjects//OLX_WebScraping//your_database.db",
#     "--Element_to_extract", "Price", "Area", "Price_per_meter2",
#     "--Limitation_Dict", "Price_MAX", "1000000", "Area_MAX", "60", "Area_MIN", "35", "Price_per_meter2_MAX", "20000", "Price_per_meter2_MIN", "11000"
# ]

# sys.argv = [
#     "C:/Users/PF_Server/PycharmProjects/OLX_WebScraping/General_Project_Files/Main_file.py",
#     "--URL", "https://www.olx.pl/nieruchomosci/mieszkania/wegrzce_128037/?search%5Bfilter_float_price:from%5D=300000&search%5Bfilter_float_price:to%5D=600000",
#     "--DB_url",  "C://Users//PF_Server//PycharmProjects//OLX_WebScraping//Wegrzyce.db",
#     "--Element_to_extract", "Price", "Area", "Price_per_meter2",
#     "--Limitation_Dict", "Price_MAX", "600000", "Area_MAX", "60", "Area_MIN", "35", "Price_per_meter2_MAX", "15000", "Price_per_meter2_MIN", "11000"
# ]

print(sys.argv)



connection_data = None # Container for global Database conenction object

def close_db_connection():
    if connection_data:
        connection_data.close()
        print("Database connection closed.")


def filter_adequate_elements(url_s_list: list):
    result_list =list()
    model = site_grabber_and_AI_API.project_configuration()
    if url_s_list:
        for link in url_s_list:

            description_from_site = site_grabber_and_AI_API.content_getter(link)
            response = site_grabber_and_AI_API.query_sending(model, description_from_site, site_grabber_and_AI_API.prompt)
            if hasattr(response, 'text') and isinstance(response.text, str):
                result_list.append(response.text.strip())
            else:
                raise ValueError(f"Invalid response format from API for link: {link}")

    return result_list

if __name__ == "__main__":

    args, Limitation_Dict = Argument_Parser()

    # Access the named arguments
    if args.URL != None:
        URL = args.URL
        print(URL)
    if args.DB_url != None:
        DB_url = args.DB_url
        print(DB_url)
    if args.Element_to_extract != None:
        Elements_to_extract = args.Element_to_extract
        print(Elements_to_extract)
    if Limitation_Dict:
        my_dict = Limitation_Dict
        print(my_dict)
    else:
        my_dict = {}

    # Define the headers for the table
    headers = ["Title", "Price", "Location", "Area", "Price per meter2" , "URL"]

    #GUI implementation
    update_queue = multiprocessing.Queue()
    stop_event = multiprocessing.Event()  # Event to signal termination
    # Start the GUI process if needed
    gui_process = multiprocessing.Process(target=start_gui, args=(update_queue, stop_event))
    gui_process.start()

    logging.info(f"Main Process started with PID : {os.getpid()}")
    logging.info(f"GUI Process started with PID noted from Main: {gui_process.pid}")

    #Data_To_store
    data = ObservableList()
    data.register_callback(list_changed)
    All_page_data_collector(URL, data)

    # Generate the table
    #printable_table = tabulate(data, headers, tablefmt="fancy_grid")

    connection_data = connect_to_database(DB_url)

    # Register the cleanup function to be called at program exit

    atexit.register(close_db_connection)

    if connection_data != None:


        for elements in data:
            elements['Validity'] = 1
            #TODO add date.today() to implement  principles of database normalization

            data_injection(elements, connection_data)



        #TODO change for automatic filter addition
        try:
            list_new_items, filtered_items_collumns = filter_new(connection_data, **my_dict) #new  items according restriction
            print(list_new_items)
            #input("Code is paused after filtering")
        except connection_data.OperationalError as e:
            print(f"An error occurred: {e}")
            list_new_items = None
        finally:
            connection_data.close()  # Close the database connection

        #AI: Main transition
        if list_new_items:
            list_for_AI = [item[filtered_items_collumns.index("URL")] for item in list_new_items] #it takes only URL adressess to gather  data.

            try:
                adequacy_list = filter_adequate_elements(list_for_AI)

                AI_filtered_list = [item_dict for index, item_dict in enumerate(list_new_items) if adequacy_list[index].upper() == "TAK"]
                pprint.pp(list_new_items)
                pprint.pp(adequacy_list)
                pprint.pp(zip(list_new_items, adequacy_list))
                pprint.pp(AI_filtered_list)
                list_new_items = AI_filtered_list
            except ValueError as e:
                print(f"An error occurred: {e}")
                send_sms('+48721776456', "AI request was resulting with FAIL")


        #input("Press enter when analyzed...")

        if list_new_items != None:

            if len(list_new_items) < 6 :

                for index, item in enumerate(list_new_items):
                    print(str(index + 1) + ". " + SMS_content_adjuster(dict(zip(filtered_items_collumns, item))))
                    send_sms('+48721776456', str(index + 1) + ". " + SMS_content_adjuster(dict(zip(filtered_items_collumns, item))))
                    time.sleep(5)
                    send_sms('+48509520947', str(index + 1) + ". " + SMS_content_adjuster(dict(zip(filtered_items_collumns, item))))

            else:
                message_text = str()
                for index, item in enumerate(list_new_items):
                    items_in_dict = dict(zip(filtered_items_collumns, item))
                    message_text = add_line_to_string(str(index + 1), items_in_dict['URL'],  message_text)
                    if (index + 1) % 10 == 0 or index == len(list_new_items) - 1:
                        print("text to send is: " + message_text)
                        send_sms('+48721776456', message_text)
                        time.sleep(5)
                        send_sms('+48509520947', message_text)
                        message_text = ""
            # # Print the table
            # print(table)
            add_rows_to_excell_file_openpyxl_2(
                r"C:\Users\PF_Server\PycharmProjects\OLX_WebScraping\General_Project_Files\Filtered_Flats.xlsx", list_new_items,
                filtered_items_collumns)

    stop_event.set()  # Signal GUI to stop
    #gui_process.terminate() #that could shout down GUI without closing connected GUI in example pipe or queue #It's to brutal and could leave some junks like python porcess opened
    gui_process.join(timeout=2)  # Give it time to close gracefully
    update_queue.close()  # Close the queue to prevent further use
    update_queue.join_thread()  # Ensure the background thread handling the queue is terminated
    exit()