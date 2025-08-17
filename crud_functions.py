import sqlite3

def add_provider(name, type_, address, city, contact):
    conn = sqlite3.connect("food_wastage.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Providers (Name, Type, Address, City, Contact) VALUES (?, ?, ?, ?, ?)",
                   (name, type_, address, city, contact))
    conn.commit()
    conn.close()

def view_providers():
    conn = sqlite3.connect("food_wastage.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Providers")
    data = cursor.fetchall()
    conn.close()
    return data

def update_provider(provider_id, name, type_, address, city, contact):
    conn = sqlite3.connect("food_wastage.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Providers
        SET Name=?, Type=?, Address=?, City=?, Contact=?
        WHERE Provider_ID=?
    """, (name, type_, address, city, contact, provider_id))
    conn.commit()
    conn.close()

def delete_provider(provider_id):
    conn = sqlite3.connect("food_wastage.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Providers WHERE Provider_ID=?", (provider_id,))
    conn.commit()
    conn.close()
