import sqlite3

DATABASE = "user.db"  # Ensure this path is correct

def delete_existing_tables():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Fetch all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("⚠️ No tables found in the database.")
        else:
            print("✅ Found tables:", [table[0] for table in tables])
            
            # Drop each table
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
                print(f"🗑️ Deleted table: {table[0]}")
            conn.commit()
            print("✅ All tables deleted successfully!")
        
        conn.close()
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    delete_existing_tables()
