import sqlite3

from DB_Management.Db_Injector import data_injection_by_url, Add_Date_to_referenced_table, filter_new

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


