import pytest
import re
from General_Project_Files.Scrapping_Houses import url_check

# Global patterns as mentioned in the code
pattern = r'^d/'  # Assuming this pattern was intended to match lines starting with "d/"
pattern_dot_com = r'^(www\.)?([a-zA-Z0-9\-]+\.(com|org|net|edu|gov|mil|[a-z]{2,3}))'


# Pytest test cases
@pytest.mark.parametrize("input_line, expected_output", [
    ("d/example", "olx.pl/example"),  # Test replacing "d/" with "olx.pl"
    ("www.example.com", "https://www.example.com"),  # Test adding "https://"
    ("example.com", "https://example.com"),  # Test adding "https://"
    ("olx.pl/oferta/mieszkanie-44-42m-duzy-ogrodek-120m-krakow-CID3-ID13WgfA.html",
     "https://olx.pl/oferta/mieszkanie-44-42m-duzy-ogrodek-120m-krakow-CID3-ID13WgfA.html"),  # Test no change needed
    ("example", "example"),  # Test input not matching any pattern
])
def test_url_check(input_line, expected_output):
    assert url_check(input_line) == expected_output
