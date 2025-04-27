import sqlite3

DATABASE = "user.db"  # Ensure this path is correct

def check_spending_table():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Check if the spending table exists; if not, create it
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='spending';")
        table_exists = cursor.fetchone()

        # if not table_exists:
        #     print("❌ The 'spending' table does not exist. Creating it now...")
        #     cursor.execute("""
        #         CREATE TABLE spending (
        #             id INTEGER PRIMARY KEY AUTOINCREMENT,
        #             category TEXT NOT NULL,
        #             amount REAL NOT NULL,
        #             date TEXT NOT NULL
        #         );
        #     """)
        #     conn.commit()
        #     print("✅ Table 'spending' created successfully!")

        # Define the row to delete
        # user_id = 1

        # # Execute DELETE query
        # cursor.execute("DELETE FROM spending WHERE user_id = ?", (user_id,))
        # conn.commit()

        # print("✅ Row deleted successfully!")


        # Define sample data
        # data_to_insert = [
        #     (1, "food", 77, "2025-3-01"),
        #     (1, "food", 150, "2025-3-02"),
        #     (1, "transport", 50, "2025-3-03"),
        #     (1, "shopping", 200, "2025-3-04"),
        # ]

        # # Insert multiple rows in one query
        # cursor.executemany("INSERT INTO spending (user_id, category, amount, date) VALUES (?, ?, ?, ?)", data_to_insert)
        # conn.commit()

        # Fetch all records from the spending table
        cursor.execute("SELECT * FROM spending;")
        rows = cursor.fetchall()

        if not rows:
            print("⚠️ The 'spending' table is empty.")
        else:
            print("\n✅ Spending Table Data:")
            for row in rows:
                print(row)

        conn.close()
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    check_spending_table()



