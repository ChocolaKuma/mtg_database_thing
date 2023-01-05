import sqlite3

# Connect to the database
conn = sqlite3.connect("magic_cards.db")

# Create a cursor
cursor = conn.cursor()

# Fetch all rows from the table
cursor.execute("SELECT * FROM cards")
rows = cursor.fetchall()

# Print the rows
print(rows)

# Close the connection
conn.close()
