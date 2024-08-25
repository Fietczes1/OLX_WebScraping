

def SMS_content_adjuster(Item_tuple: dict):
    if len(Item_tuple) != 8:
        return "Invalid data length"

    id, title, price, location_date, flat_area, price_per_m2, url, index = (
        Item_tuple["Ads_id"],
        Item_tuple["Title"],
        Item_tuple["Price"],
        Item_tuple["Location"],
        Item_tuple["Area"],
        Item_tuple["Price_per_meter2"],
        Item_tuple["URL"],
        Item_tuple["Validity"]
    )

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


def add_line_to_string(index: str, text, existing_string ):
    if existing_string:
        existing_string += "\n"
    existing_string += f"{index}. {text}"
    print("Existing string is: \n" + existing_string)
    return existing_string
