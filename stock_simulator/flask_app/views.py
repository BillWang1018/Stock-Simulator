from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="34.28.106.5",
            user="root",
            password="#fcu-DBS#",
            database="mysql",
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def stock_list():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Snum FROM quotations")
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('stock_list.html', members=members)
    else:
        return "Error connecting to the database."

@app.route('/stock/<int:snum>')
def stock_detail(snum):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Snum, BuyAmt, SellAmt, TStmp, Sprice FROM quotations WHERE Snum = %s", (snum,))
        stock = cursor.fetchone()
        cursor.close()
        conn.close()
        if stock:
            return render_template('stock_detail.html', stock=stock)
        else:
            return "Stock not found."
    else:
        return "Error connecting to the database."

if __name__ == '__main__':
    app.run(port=5000, debug=True)
