import bs4
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from datetime import date
from Db_Injector import data_injection, data_injection_by_url, filter_new, connect_to_database
import re

url = "https://www.olx.pl/nieruchomosci/mieszkania/krakow/q-Mieszkanie/?search%5Bfilter_float_price:from%5D=300000"

def Beatuiful_object_graber(olx_url: str) -> bs4.BeautifulSoup:
    response = requests.get(olx_url)
    soup = None
    try:
        soup = BeautifulSoup(response.content, "html.parser")
        # Code to work with the soup object
        # ...
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return soup

def next_page_rl_graber(Soup_object: bs4.BeautifulSoup):
    Next_page_button = Soup_object.find_all("a", {"data-cy" : "pagination-forward"})
    if Next_page_button != []:
        Next_page_URL = Next_page_button[0].get("href")
        return Next_page_URL
    else:
        return False


def All_page_data_collector(page_Url: str) -> list:
    """
    This function Is responsible for collecting data across all page scope.

    :param page_Url: It's starting URL (this url have to consist list of searched elements)
    :return:
    """
    data = []

    while page_Url:
        #Bs - obejct
        Soup_object = Beatuiful_object_graber(page_Url)

        data.extend(OLX_Household_data_gethering(Soup_object))

        page_Url = next_page_rl_graber(Soup_object)
        if page_Url:
            page_Url = str("https://www.olx.pl" + next_page_rl_graber(Soup_object))
        else:
            print("Done")

    return data






def OLX_Household_data_gethering(soup: bs4.BeautifulSoup) -> list:
    """
    Gather household data from the given OLX URL.

    Args:
        olx_url (str): The OLX URL to scrape for household data.

    Returns:
        list: A list containing the gathered household data.
    """


    # Find all the advertisement cards
    ad_cards = soup.find_all("div", {"data-cy": "l-card"})

    # Initialize an empty list to store the data
    data = []
    price_pattern = r"(\d{1,3}(?: \d{3})*) zł"
    price_per_sqm_pattern = r"(\d{1,5}[.,]?\d{0,5}?)\s*zł\/m²"  # Regular expression pattern to extract price per square meter
    sqm_pattern = r"(\d+)\s*m²"  # Regular expression pattern to extract square meter

    for card in ad_cards:
        title = ""
        price_zl = ""
        location = ""
        square_meter = ""
        price_per_square_meter = ""
        url = ""
        Advertisement_id = ""
        try:
            Advertisement_id = card.get("id")
        except AttributeError:
            pass

        try:
            title_elem = card.find("h6", class_="css-16v5mdi er34gjf0")
            title = title_elem.text.strip()
        except AttributeError:
            pass

        try:
            price_elem = card.find("p", class_="css-10b0gli er34gjf0")
            price_zl = price_elem.text.strip()
            price_zl = re.findall(price_pattern, price_zl)[0]
            price_zl = price_zl.replace(" ","")
        except AttributeError:
            pass

        try:
            location_elem = card.find("p", class_="css-veheph er34gjf0")
            location = location_elem.text.strip()
        except AttributeError:
            pass

        try:
            area_elem = card.find("span", class_="css-643j0o")

            price_per_sqm_match = re.search(price_per_sqm_pattern, area_elem.text)
            if price_per_sqm_match:
                price_per_square_meter = float(price_per_sqm_match.group(1))
            else:
                price_per_square_meter = None

            # Extract square meter
            sqm_match = re.search(sqm_pattern, area_elem.text)
            if sqm_match:
                square_meter = int(sqm_match.group(1))
            else:
                square_meter = None
        except AttributeError:
            pass

        try:
            url_elem = card.find("a", class_="css-rc5s2u")
            url = url_elem.get("href")
        except AttributeError:
            pass

        data.append([Advertisement_id, title, price_zl, location, square_meter, price_per_square_meter, url])

    return data


def line_by_line_data_appender(data :list) -> bool:
    try:
        #TODO
        #Check data for using function conn.executemany()
        # Code for inserting data into the database
        data_injection(list, "your_database.db")
        # ...
        return True  # Indicate successful insertion
    except Exception as e:
        # Handle the exception or error here
        print("Error occurred:", str(e))
        return False  # Indicate error occurred during insertion



# Define the headers for the table
headers = ["Title", "Price", "Location", "Area", "Price per meter2" , "URL"]

#Data_To_store
data = All_page_data_collector(url)

# Generate the table
#printable_table = tabulate(data, headers, tablefmt="fancy_grid")

for elements in data:
    elements.append(1)
    #TODO add date.today() to implement  principles of database normalization
    data_injection_by_url(elements, 'your_database.db' )

#TODO change for automatic
filter_new(connect_to_database('your_database.db'), 1000)


# # Print the table
# print(table)
