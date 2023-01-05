##scryfall access

import requests

card_name = "Shivan Dragon"
set_code = "SLC"

api_url = "https://api.scryfall.com/cards/named"

params = {
    "fuzzy": card_name,
    "set": set_code
}

response = requests.get(api_url, params=params)

if response.status_code == 200:
    # Parse the JSON data in the response
    data = response.json()
    # Extract the card's Scryfall URL from the data
    card_url = data["scryfall_uri"]
    print(card_url)
else:
    print("Error: Could not retrieve card data from Scryfall API.")
