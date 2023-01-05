from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__, template_folder='templates')


def get_data_from_database():
    # Connect to the database
    conn = sqlite3.connect("magic_cards.db")
    # Create a cursor
    cursor = conn.cursor()
    # Fetch all rows from the table
    cursor.execute("SELECT * FROM cards")
    rows = cursor.fetchall()
    # Close the connection
    conn.close()
    return rows

@app.route('/')
def display_data():
    rows = get_data_from_database()
    return render_template("table.html", rows=rows)

if __name__ == '__main__':
    app.run()
