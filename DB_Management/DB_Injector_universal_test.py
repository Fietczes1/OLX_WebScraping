from DB_Management.DB_injection_universal import construct_sql_queries

example_dict = {
    'Ads_id': 'AD123456',
    'Title': 'Spacious Apartment',
    'Price': 7500,
    'Location': 'Warsaw',
    'Area': 120,
    'Price_per_meter2': 1250,
    'URL': 'https://example.com/ad/AD123456',
    'Validity': True
}

def test_construct_sql_queries():
    assert construct_sql_queries("Nowa_Tabela", example_dict) == None