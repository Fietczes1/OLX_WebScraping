import time

import bs4

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from DB_Management.Db_Injector import data_injection
#from tabulate import tabulate
#module import SMS_content_adjuster #,Send_message
#from Sending_SMS_GSM_modem_liblary import send_sms
import re

from typing import List, Dict, Union, Any

attrs = {
    'Title': "css-1wxaaza",
    'Price': "ad-price",
    'Location': "css-veheph er34gjf0",
    'Area': "css-1cd0guq",
    'URL': "css-rc5s2u"
}


# List of elements you want to extract
Elements_to_extract = ["Ads_id", "Title", "Price", "Location", "Area", "Price_per_meter2", "URL", "Validity"] #It will be input From interface
KEYS_ORDER = ["Ads_id", "Title", "Price", "Location", "Area", "Price_per_meter2", "URL", "Validity"]

#URL = "https://www.olx.pl/nieruchomosci/mieszkania/krakow/q-Mieszkanie/?search%5Bfilter_float_price:from%5D=300000"
#DB_url = "your_database.db" #"C://Users//PF_Server//PycharmProjects//OLX_WebScraping//your_database.db"
css_selector = "div[data-cy='l-card']"  # Single element with Advertisement selector
def Beatuiful_object_graber(olx_url: str) -> bs4.BeautifulSoup:
    """
    Navigates to the given URL, waits for a specific element to be visible,
    then returns a BeautifulSoup object containing the page's HTML.

    Parameters:
    olx_url (str): The URL to navigate to.

    Returns:
    BeautifulSoup: A BeautifulSoup object containing the page's HTML.
    """



    attempt = 0
    max_attempts = 10
    wait_time = 35  # Increased wait time
    response = str()

    print(f"Trying to elicit data for: {olx_url}")

    while len(response) == 0 and attempt < max_attempts:
        #It have to be here as driver.close() for last opened Window terminate driver object
        # Set up Selenium to use Chrome with the WebDriver Manager
        try:
            #service = Service(ChromeDriverManager().install())
            service = Service(r'C:\Users\PF_Server\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
            driver = webdriver.Chrome(service=service)

        except Exception as e:
            print(f"Driver initialization fail caused by error : {e}")
            continue

        try:
            # Navigate to the page
            driver.get(olx_url)

            # Wait for the specific element to be visible
            WebDriverWait(driver, wait_time).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )

            time.sleep(2)

            # Get the page source
            response = driver.page_source


        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            attempt += 1
            wait_time = wait_time + 5 * attempt
            time.sleep(20)
            # Don't forget to close the driver

        finally:
            #driver.close()#Closes the current browser window or tab, but does not end the WebDriver session. If other tabs or windows are open, they remain open, and you can switch to them with Selenium commands. However, if the closed window was the last one, it behaves similar to quit() in that the WebDriver session ends.
            driver.quit() #Closes all browser windows and ends the WebDriver session entirely. If you use driver.quit(), any subsequent calls to WebDriver will require you to instantiate a new driver, effectively restarting the entire process.

    if attempt == max_attempts:

        exit(0) # I using this method of finalysing code to didnt rise error in command line

    #response = requests.get(olx_url) #oldsolution

    # # Don't forget to close the driver
    # driver.quit()

    soup = None
    try:
        soup = BeautifulSoup(response, "html.parser")
        # Code to work with the soup object
        # ...
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return soup

def next_page_rl_graber(Soup_object: bs4.BeautifulSoup):
    Next_page_button = Soup_object.find_all("a", {"data-cy" : "pagination-forward"})
    if Next_page_button != [] and Soup_object.find("p", {"class" : "css-1oc165u er34gjf0"}) == None:
        Next_page_URL = Next_page_button[0].get("href")
        return Next_page_URL
    else:
        return False


def All_page_data_collector(page_Url: str, list_container = None) -> list:
    """
    This function Is responsible for collecting data across all page scope.

    :param page_Url: It's starting URL (this url have to consist list of searched elements)
    :return:
    """
    if list_container == None:
        list_container = []

    while page_Url:
        #Bs - obejct
        Soup_object = Beatuiful_object_graber(page_Url)

        #data.extend(OLX_Household_data_gethering(Soup_object))
        list_container.extend(extract_all_rows(Soup_object))
        #print(type(list_container))
        page_Url = next_page_rl_graber(Soup_object)
        if page_Url:
            page_Url = str("https://www.olx.pl" + next_page_rl_graber(Soup_object))
        else:
            print("Done")

    return list_container


def url_check(line: str) -> str:
    # Define the regular expression pattern to match lines starting with "d/"
    pattern = r'^/d'

    # Use re.sub to replace "d/" with "olx.pl" at the beginning of the line
    replaced_line = re.sub(pattern, 'olx.pl', line)

    # If the pattern is not matched, return the original line
    if replaced_line == line:
        return line
    else:
        return replaced_line




def extract_all_rows(soup: bs4.BeautifulSoup):
    soup = soup.find("div", attrs={"data-testid": "listing-grid"})
    # Find all the advertisement cards
    ad_cards = soup.find_all("div", {"data-cy": "l-card"})
    extracted_data = []
    for card in ad_cards:
        extracted_data.append(extract_data(card, attrs, Elements_to_extract))
    return extracted_data


def dict_to_list(data_dict: Dict[str, Any], keys_order: List[str]) -> List[Union[str, int, float, None]]:
    """
    Convert a dictionary into a list of values based on a specific order of keys.

    Parameters:
    - data_dict: The dictionary containing the data.
    - keys_order: A list of keys specifying the order in which values should be extracted from the dictionary.

    Returns:
    - A list of values extracted from the dictionary based on the specified order of keys.
    """

    return [data_dict.get(key, None) for key in keys_order]

#Function to make scrapper Universal and This function will only Generate single row of Data for item
def extract_data(card: bs4.Tag, attrs: Dict[str, str], elements: List[str]) -> Dict[str, Union[str, int, float, None]]:
    data = {}
    price_pattern = r"(\d+(?: \d+)*(?:,\d{2})*) zł"
    price_per_sqm_pattern = r"(\d{1,5}[.,]?\d{0,5}?)\s*zł\/m²"
    sqm_pattern = r"(\d+(?:,\d{2})?)\s*m²"



    if 'Ads_id' in elements:
        data['Ads_id'] = card.get("id", "")

    if 'Title' in elements:
        try:
            data['Title'] = card.find("h6", class_=attrs['Title']).text.strip()
        except AttributeError:
            data['Title'] = ""

    if 'Price' in elements:
        try:
            price_elem = card.find("p", attrs={"data-testid" : attrs['Price']})
            price_zl = re.findall(price_pattern, price_elem.text.strip())[0].replace(" ", "").replace(',', '.')
            data['Price'] = int(float(price_zl))
        except (AttributeError, IndexError):
            data['Price'] = ""

    if 'Location' in elements:
        try:
            data['Location'] = card.find("p", attrs= {'data-testid' : 'location-date'}).text.strip()
        except AttributeError:
            data['Location'] = ""

    if 'Area' in elements or 'Price_per_meter2' in elements:
        try:
            area_elem = card.find("span", class_=attrs['Area'])
            if not area_elem:
                area_elem = re.findall(r"[\d\s\.\,]+(?=m²).{10}[\d\s\.\,]+zł/m²", card.text)[0]



            if 'Price_per_meter2' in elements:
                price_per_sqm_match = re.search(price_per_sqm_pattern, area_elem.text)
                data['Price_per_meter2'] = float(price_per_sqm_match.group(1).replace(",", ".")) if price_per_sqm_match else None

            if 'Area' in elements:
                proper_str_float_construction_of_sqm_match = str()
                sqm_match = re.search(sqm_pattern, area_elem.text)
                if sqm_match is not None:
                    proper_str_float_construction_of_sqm_match = sqm_match.group(1)
                    if ',' in proper_str_float_construction_of_sqm_match:
                        proper_str_float_construction_of_sqm_match = proper_str_float_construction_of_sqm_match.replace(',','.')
                    data['Area'] = int(float(proper_str_float_construction_of_sqm_match))
                else:
                    data['Area'] = None


        except AttributeError:
            if 'Price_per_meter2' in elements:
                data['Price_per_meter2'] = None
            if 'Area' in elements:
                data['Area'] = None

    if 'URL' in elements:
        try:
            url_elem, _ = card.find_all(lambda tag: tag.has_attr('href'))
            data['URL'] = url_check(url_elem.get("href"))
        except AttributeError:
            data['URL'] = ""

    # Adding a placeholder for 'Validity' as it was not in the original function and
    # it's unclear how this should be extracted
    if 'Validity' in elements:
        data['Validity'] = None  # Replace with actual extraction logic

    print(data)

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
            title_elem = card.find("h6", class_="css-1wxaaza")
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
            location_elem = card.find("p", attrs= {'data-testid' : 'location-date'})
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
            url_elem = card.find("a", class_="css-z3gu2d")#class_="css-rc5s2u")
            url = url_check(url_elem.get("href"))

        except AttributeError:
            pass

        data.append([Advertisement_id, title, price_zl, location, square_meter, price_per_square_meter, url])

    return data


def line_by_line_data_appender(data :list) -> bool:
    try:
        #TODO
        #Check data for using function conn.executemany()
        # Code for inserting data into the database
        result = data_injection(list, DB_url)

        # ...
        return result # Indicate successful insertion
    except Exception as e:
        # Handle the exception or error here
        print("Error occurred:", str(e))
        return False  # Indicate error occurred during insertion




