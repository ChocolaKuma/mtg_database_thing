from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def display_cards():
    # Open a connection to the database
    conn = sqlite3.connect('magic_cards.db')
    # Create a cursor
    cursor = conn.cursor()
    # Select all rows from the cards table
    cursor.execute("SELECT * FROM cards")
    # Fetch the rows
    rows = cursor.fetchall()
    # Close the connection
    conn.close()

    # Build the HTML table
    table = '<table>\n'
    table += '    <tr>\n'
    table += '        <th>Quantity</th>\n'
    table += '        <th>Name</th>\n'
    table += '        <th>Set</th>\n'
    table += '        <th>URL</th>\n'
    table += '    </tr>\n'
    for row in rows:
        table += '    <tr>\n'
        table += f'        <td>{row[0]}</td>\n'
        table += f'        <td>{row[1]}</td>\n'
        table += f'        <td>{row[2]}</td>\n'
        table += f'        <td><a href="{row[3]}">{row[3]}</a></td>\n'
        table += '    </tr>\n'
    table += '</table>'

    # Return the HTML table as the response
    return table

if __name__ == '__main__':
    app.run()
