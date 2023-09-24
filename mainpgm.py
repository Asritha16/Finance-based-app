# Import Flask and SQLite3 modules
from flask import Flask, render_template, request
import sqlite3

# Create an instance of Flask app
app = Flask(__name__)

# Create a connection to the database file
conn = sqlite3.connect('finance.db')

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# Create a table named transactions with five columns: id, type, amount, and date,usage
cur.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    ID INTEGER PRIMARY KEY,
    Type TEXT,
    Amount REAL,
    DATE TEXT,
    usage TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

# Define a route for the home page
@app.route('/')
def index():
    # Open a connection to the database file
    conn = sqlite3.connect('finance.db')
    cur = conn.cursor()

    # Select all rows from the transactions table and store them in a list
    cur.execute('SELECT * FROM transactions')
    transactions = cur.fetchall()

    # Calculate the total income and expenses by summing up the amount column based on the type column
    cur.execute('SELECT SUM(Amount) FROM transactions WHERE type = "Income"')
    total_income = cur.fetchone()[0]
    cur.execute('SELECT SUM(Amount) FROM transactions WHERE type = "Expense"')
    total_expense = cur.fetchone()[0]
    cur.execute('SELECT SUM(Amount) FROM transactions WHERE type= "Savings"')
    total_savings = cur.fetchone()[0]

    if total_expense==None or total_income==None:
        total_expense=0
        total_savings=0
        var = total_expense + total_savings
    balance = total_income - total_expense
    #balance = total_income + (total_expense - total_savings)  
    # Close the connection
    conn.close()

    # Render the index.html template and pass the transactions, total_income, and total_expense variables to it
    return render_template('index.html', transactions=transactions, total_income=total_income, total_expense=total_expense,total_savings=total_savings,balance=balance)

# Define a route for adding a new transaction
@app.route('/add', methods=['GET', 'POST'])
def add():
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the values from the form fields
        type = request.form['type']
        amount = request.form['amount']
        date = request.form['date']
        usage = request.form['usage']
        

        # Open a connection to the database file
        conn = sqlite3.connect('finance.db')
        cur = conn.cursor()

        # Insert a new row into the transactions table with the values from the form fields
        cur.execute('INSERT INTO transactions (Type, Amount, DATE, usage)  VALUES (?, ?, ?, ?)', (type, amount, date, usage))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Redirect to the home page
        return Flask.redirect(self = Flask, location ='/', code = 302)

    # If the request method is GET, render the add.html template
    else:
        return render_template('add.html')

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port="8080")
