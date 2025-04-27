import sqlite3
import pandas as pd
import io
from flask import Flask, send_file



def download_data():
    # Connect to your SQLite database
    conn = sqlite3.connect('your_database.db')  # Update with your DB name
    df = pd.read_sql_query("SELECT * FROM your_table", conn)  # Replace with your table name
    conn.close()

    # Save DataFrame to in-memory buffer
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(
        io.BytesIO(buffer.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='data.csv'
    )