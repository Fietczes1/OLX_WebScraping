

def SMS_content_adjuster(Item_tuple: tuple):
    if len(Item_tuple) != 8:
        return "Invalid data length"

    id, title, price, location_date, flat_area, price_per_m2, url, index = Item_tuple

    formatted_text = f"""
    --------------------
    ID: {id}
    Title: {title}
    Price: {price} PLN
    Location and Date: {location_date}
    Flat Area: {flat_area}
    Price per m^2: {price_per_m2} PLN/m^2
    URL: {url}
    --------------------
    """
    return formatted_text

    # Test the function

