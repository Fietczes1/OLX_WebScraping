import sqlite3
# Add the project root directory to sys.path
import os
import sys
# Add the General_Project_Files directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'General_Project_Files')))


from EXCELL_file_management.Excell_management import Add_rows_to_excell_file, add_rows_to_excell_file_openpyxl, \
    test_function, add_rows_to_excell_file_openpyxl_2

from DB_Management.Db_Injector import data_injection_by_url, Add_Date_to_referenced_table, filter_new
from General_Project_Files.Main_file import Argument_Parser

conn = sqlite3.connect('../your_database.db')  # Creates a connection object
cursor = conn.cursor()  # Creates a cursor object


def test_data_validation():
    pass

def test_data_injection():
    valid_data = ['828229765', 'Mieszkanie idealne pod inwestycje!', '389000', 'Kraków, Krowodrza - Odświeżono dnia 22 czerwca 2023', 63, 12.0, 'https://www.otodom.pl/pl/oferta/mieszkanie-idealne-pod-inwestycje-ID4lRx2.html', 1]
    valid_data_1 = ['828229765', 'Funkcjonalne 3 pokojowe mieszkanie w super lokalizacji - OLSZA', '480000',
     'Kraków, Prądnik Czerwony - Odświeżono dnia 29 czerwca 2023', 60, 17.0,
     '/d/oferta/funkcjonalne-3-pokojowe-mieszkanie-w-super-lokalizacji-olsza-CID3-IDUUCJT.html', 1]
    valid_data_2 = {'Advertisement_id': '857633909', 'title': 'PIĘKNE Mieszkanie z Widokiem ul.Strzelców 74 m2 - 3 Pokoje - 12 PIĘTRO', 'price_zl': '1060000', 'location': 'Kraków, Prądnik Czerwony - Odświeżono Dzisiaj o 07:56', 'price_per_square_meter': 14324.32, 'square_meter': 74, 'url': '/d/oferta/piekne-mieszkanie-z-widokiem-ul-strzelcow-74-m2-3-pokoje-12-pietro-CID3-IDV2xKZ.html', 'Validity': 1}

    assert data_injection_by_url(valid_data_2, "your_database.db") == True
    Proce_per_square_NONE = ['Funkcjonalne 3 pokojowe mieszkanie w super lokalizacji - OLSZA', '480000',
     'Kraków, Prądnik Czerwony - Odświeżono dnia 29 czerwca 2023', 60, None,
     '/d/oferta/funkcjonalne-3-pokojowe-mieszkanie-w-super-lokalizacji-olsza-CID3-IDUUCJT.html', 1]
    assert data_injection_by_url(valid_data_2, "your_database.db") == True

def test_Add_Date_to_referenced_table():

    #assert cursor.execute('INSERT INTO Date_Observed (AdsDate, Ads_id) VALUES (?, ?)', ("2023-06-21", "828229765"))

    assert Add_Date_to_referenced_table(conn,  "828229765") == True

def test_filter_new():
    assert filter_new(conn, 10000) == True
    assert filter_new(conn, 10000, 30) == True
    assert filter_new(conn, Price_per_meter2_MAX= 10000, Area_MIN= 30) == True
    #assert filter_new(conn_mock, )

# def test_Argument_Parser():
#     sys.argv = [
#         "script_name.py",
#         "--URL",  r'https://www.olx.pl/oferty/q-Silnik-Bafang-BBS02/?search%5Bfilter_float_price:from%5D=500&search%5Bfilter_float_price:to%5D=1000',
#         "--DB_url", r'C:\Users\njvtwk\PycharmProjects\WebScrappingOLX\Bafang.db',
#         "--Element_to_extract", "Ads_id", "Title", "Price", "Location", "URL", "Validity",
#         "--Limitation_Dict", "Price_MAX", "1200", "Price_MIN", "600"
#     ]
#     assert Argument_Parser() ==

def test_add_rows_to_excell_file_openpyxl_2():
    data_2 = [('914232192', 'Nowa Huta | 2 POK. | Piwnica', '', 46, 13478.82, 'https://www.otodom.pl/pl/oferta/nowa-huta-2-pok-piwnica-ID4qioo.html', 1, 630000), ('917431779', '✅2 pokoje✅Gotowe do wprowadzenia✅Ruczaj', '', 42, 16376.06, 'https://www.otodom.pl/pl/oferta/2-pokojegotowe-do-wprowadzeniaruczaj-ID4qhL5.html', 1, 695000), ('918657749', '3 pokojowe nowoczesne przy pętli Krowodrza Górka', '', 38, 18571.43, 'https://www.otodom.pl/pl/oferta/3-pokojowe-nowoczesne-przy-petli-krowodrza-gorka-ID4qBKi.html', 1, 715000), ('922585397', 'Funkcjonalne 3 pokoje z jasną kuchnią Bieńczyce', '', 48, 14354.17, 'https://www.otodom.pl/pl/oferta/funkcjonalne-3-pokoje-z-jasna-kuchnia-bienczyce-ID4qnR9.html', 1, 689000), ('923439511', '✅ Nowe Wykończone 2 pokoje + Garderoba | Bagry', '', 37, 18861.36, 'https://www.otodom.pl/pl/oferta/nowe-wykonczone-2-pokoje-garderoba-bagry-ID4qVVN.html', 1, 699945), ('923471075', '2 pokoje, osobna kuchnia + duży balkon i piwnica', '', 41, 16317.07, 'https://www.otodom.pl/pl/oferta/2-pokoje-osobna-kuchnia-duzy-balkon-i-piwnica-ID4qX6E.html', 1, 669000), ('923491028', '2-3pok | Zielona spokojna okolica | pod Krakowem', '', 51, 13056.09, 'https://www.otodom.pl/pl/oferta/2-3pok-zielona-spokojna-okolica-pod-krakowem-ID4qUox.html', 1, 675000), ('923524488', 'przytulne 2 pokojowe|garaż|wyposażone|Bronowice', '', 43, 17051.22, 'https://www.otodom.pl/pl/oferta/przytulne-2-pokojowe-garaz-wyposazone-bronowice-ID4qVPH.html', 1, 739000), ('923564068', 'Taras 60m2 | Kameralne budownictwo | 3 Pokoje 55m2', '', 55, 14953.15, 'https://www.otodom.pl/pl/oferta/taras-60m2-kameralne-budownictwo-3-pokoje-55m2-ID4qXHM.html', 1, 829900), ('923702454', 'Przestronne 2-pokoj. blisko centrum, opcja 3 pokoi', '', 51, 13942.68, 'https://www.otodom.pl/pl/oferta/przestronne-2-pokoj-blisko-centrum-opcja-3-pokoi-ID4qY9Q.html', 1, 720000), ('923737436', '2 pokoje, ul. Morcinka / Nowa Huta, balkon / II pietro', '', 45, 14578.34, 'olx.pl/oferta/2-pokoje-ul-morcinka-nowa-huta-balkon-ii-pietro-CID3-ID10wUiU.html', 1, 669000), ('923745896', 'Przytulne 2-pokojowe mieszkanie na bliskim Ruczaju', '', 49, 15204.08, 'https://www.otodom.pl/pl/oferta/przytulne-2-pokojowe-mieszkanie-na-bliskim-ruczaju-ID4qYfJ.html', 1, 745000), ('923767324', 'Wykończone dwa 2 pokojowe mieszkania', '', 38, 18688.31, 'https://www.otodom.pl/pl/oferta/wykonczone-dwa-2-pokojowe-mieszkania-ID4qYj2.html', 1, 719500), ('923790003', 'Mieszkanie wolne od zaraz, bez pośrednika', '', 50, 15800, 'https://www.otodom.pl/pl/oferta/mieszkanie-wolne-od-zaraz-bez-posrednika-ID4pTrZ.html', 1, 790000), ('923824451', '3 pokoje/49m2/balkon/ul.Dębskiego/2018r', '', 49, 13469.39, 'https://www.otodom.pl/pl/oferta/3-pokoje-49m2-balkon-ul-debskiego-2018r-ID4qQ2i.html', 1, 660000), ('923848885', 'Mieszkanie na sprzedaż', '', 39, 15384.62, 'olx.pl/oferta/mieszkanie-na-sprzedaz-CID3-ID10vnit.html', 1, 600000), ('923883817', 'Mieszkanie na Ruczaju na sprzedaż', '', 41, 16585.37, 'olx.pl/oferta/mieszkanie-na-ruczaju-na-sprzedaz-CID3-ID10vvnT.html', 1, 680000), ('923898169', '2 pokoje, z dużym balkonem z widokiem na zielenień | ul. Klonowica', '', 50, 15800, 'olx.pl/oferta/2-pokoje-z-duzym-balkonem-z-widokiem-na-zielenien-ul-klonowica-CID3-ID10vA7n.html', 1, 790000), ('923925407', 'Ładne 3-pokojowe mieszkanie gotowe do wprowadzenia', '', 56, 17767.86, 'olx.pl/oferta/ladne-3-pokojowe-mieszkanie-gotowe-do-wprowadzenia-CID3-ID10vHcH.html', 1, 995000), ('923939429', 'Mieszkanie do częściowego remontu Krowodrza Górka', '', 51, 13267.75, 'https://www.otodom.pl/pl/oferta/mieszkanie-do-czesciowego-remontu-krowodrza-gorka-ID4qYEM.html', 1, 683289), ('923947894', 'Kraków Piaszczysta SLOW CITY nowe mieszkanie 40m2', '', 39, 15605.3, 'https://www.otodom.pl/pl/oferta/krakow-piaszczysta-slow-city-nowe-mieszkanie-40m2-ID4qYGf.html', 1, 623900), ('923950127', 'Prądnik Biały / ul. Chełmońskiego 106b/ garaż !', '', 43, 15093.02, 'https://www.otodom.pl/pl/oferta/pradnik-bialy-ul-chelmonskiego-106b-garaz-ID4qYGz.html', 1, 649000)]
    collumns_2 = ['Ads_id', 'Title', 'Location', 'Area', 'Price_per_meter2', 'URL', 'Validity', 'Price']
    assert add_rows_to_excell_file_openpyxl_2(r"C:\Users\PF_Server\PycharmProjects\OLX_WebScraping\General_Project_Files\Filtered_Flats.xlsx", data_2, collumns_2) == None
def test_test_function():
    assert test_function() == "OK"