import sqlite3
import requests
import os
import time

DefultDbName = "magic_cards.db"
sleepVar = .25
input_values = 1, "Bard class", "AFR"
DEBUG = 1

def footer():
    print("")
    print("")
    print("")
    print("#####################################################")
def header():
    print("#####################################################")
    print("")
    print("")
    print("")

def delete_database(db_name):
    # Check if the file exists
    if os.path.exists(db_name):
        # Delete the file
        os.remove(db_name)
        if DEBUG:
            print(f"{db_name} was deleted.")
    else:
        if DEBUG:
            print(f"{db_name} does not exist.")


def makeSampleDB():
    if not os.path.exists("magic_cards.db"):
        # Connect to the database
        conn = sqlite3.connect("magic_cards.db")
        # Create a cursor
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE cards (quantity INTEGER, name TEXT, [set] TEXT, [uri] TEXT)")
        # Commit the transaction
        conn.commit()
        # Close the connection
        conn.close()
        if DEBUG:
            print("Done Making Sample DB")
    else:
        if DEBUG:
            print("magic_cards.db already exists")
    
def display(db):
    # Connect to the database
    conn = sqlite3.connect(db)
    # Create a cursor
    cursor = conn.cursor()
    # Fetch all rows from the table
    cursor.execute("SELECT * FROM cards")
    rows = cursor.fetchall()
    # Print the rows
    print(rows)
    # Close the connection
    conn.close()
    
def insert_into_database(db,quantity, name, set_code):
    # Connect to the database
    conn = sqlite3.connect(db)
    # Create a cursor
    cursor = conn.cursor()
    # Retrieve the Scryfall URL for the card
    url = ""
    url = PullScryfallURI(name, set_code)
    # Add rows to the table
    cursor.execute("INSERT INTO cards VALUES (?, ?, ?, ?)", (quantity, name, set_code, url))
    # Commit the transaction
    conn.commit()
    # Close the connection
    conn.close()



def PullScryfallURI(card_Name,set_Code):
    api_url = "https://api.scryfall.com/cards/named"

    params = {
        "fuzzy": card_Name,
        "set": set_Code
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        # Parse the JSON data in the response
        data = response.json()
        # Extract the card's Scryfall URL from the data
        card_url = data["scryfall_uri"]
        return card_url
    else:
        # Return an empty string if the request fails
        return ""
    
def format_card(card_string):
    # Split the string into parts
    parts = card_string.split()
    # Extract the quantity, name, and set code from the parts
    quantity = parts[0]
    name = ' '.join(parts[1:-1])
    set_code = parts[-1][1:-1]  # Remove the brackets from the set code
    # Return the data as a list
    return [quantity, name, set_code]

def create_input_list():
    # Define the file name
    file_name = "Input_List.txt"
    # Check if the file exists
    if not os.path.exists(file_name):
        # Create the file if it doesn't exist
        with open(file_name, "w") as f:
            f.write("")
        if DEBUG:
            print(f"{file_name} was created.")
    else:
        if DEBUG:
            print(f"{file_name} already exists.")

def read_input_list():
    # Define the file name
    file_name = "Input_list.txt"
    # Check if the file exists
    if os.path.exists(file_name):
        # Read the contents of the file
        with open(file_name, "r") as f:
            contents = f.read()
        return contents
    else:
        print(f"{file_name} does not exist.")
        return None
def delete_total_line(contents):
    # Split the contents into lines
    lines = contents.split('\n')
    # Check if the first line starts with "TOTAL"
    if lines[0].strip().startswith("TOTAL"):
        # Remove the first line if it does
        lines = lines[1:]
    # Join the lines back into a single string
    new_contents = '\n'.join(lines)
    return new_contents


def process_input_list(contents,DBname):
    # Read the contents of the file

    # Split the contents into lines
    lines = contents.split('\n')
    # Iterate over the lines
    for line in lines:
        # Skip empty lines
        if not line:
            continue
        # Format the line
        card_data = format_card(line)
        # Insert the data into the database
        insert_into_database(DBname, *card_data)
        time.sleep(sleepVar)
        if DEBUG:
            print(card_data, "Has been inputed")


def BulkEnter(DB):
    header()
    makeSampleDB() #checks to see if DB is made if not it make it
    create_input_list() #checks to see if inputlist is made if not it make it
    #reads list into memory formats and inserts into database with scryfall link
    process_input_list(delete_total_line(read_input_list()),DB)
    header()
    display(DB)
    footer()


BulkEnter(DefultDbName)






    
    
