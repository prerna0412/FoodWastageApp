import sqlite3

def create_tables():
    conn = sqlite3.connect("food_wastage.db")
    cursor = conn.cursor()

    # Providers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Providers (
        Provider_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Type TEXT,
        Address TEXT,
        City TEXT,
        Contact TEXT
    )
    """)

    # Receivers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Receivers (
        Receiver_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Type TEXT,
        City TEXT,
        Contact TEXT
    )
    """)

    # Food Listings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Food_Listings (
        Food_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Food_Name TEXT,
        Quantity INTEGER,
        Expiry_Date TEXT,
        Provider_ID INTEGER,
        Provider_Type TEXT,
        Location TEXT,
        Food_Type TEXT,
        Meal_Type TEXT
    )
    """)

    # Claims Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Claims (
        Claim_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Food_ID INTEGER,
        Receiver_ID INTEGER,
        Status TEXT,
        Timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
