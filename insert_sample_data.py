import sqlite3

def insert_sample_data():
    conn = sqlite3.connect("food_wastage.db")
    cursor = conn.cursor()

    # Insert sample Providers
    cursor.executemany("""
    INSERT INTO Providers (Name, Type, Address, City, Contact)
    VALUES (?, ?, ?, ?, ?)
    """, [
        ("Green Leaf Restaurant", "Restaurant", "MG Road", "Pune", "9876543210"),
        ("Fresh Mart", "Grocery Store", "Baner", "Pune", "9123456780"),
        ("Daily Meals", "Restaurant", "Powai", "Mumbai", "9988776655"),
        ("Healthy Basket", "Supermarket", "Andheri", "Mumbai", "9001122334"),
        ("Foodies Hub", "Restaurant", "Camp", "Pune", "8001234567")
    ])

    # Insert sample Receivers
    cursor.executemany("""
    INSERT INTO Receivers (Name, Type, City, Contact)
    VALUES (?, ?, ?, ?)
    """, [
        ("Helping Hands NGO", "NGO", "Pune", "7894561230"),
        ("Community Kitchen", "Community Center", "Mumbai", "8765432109"),
        ("John Doe", "Individual", "Pune", "7001234567"),
        ("Anna Foundation", "NGO", "Mumbai", "7209876543")
    ])

    # Insert sample Food Listings
    cursor.executemany("""
    INSERT INTO Food_Listings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ("Veg Biryani", 20, "2025-08-20", 1, "Restaurant", "Pune", "Vegetarian", "Dinner"),
        ("Bread Packets", 50, "2025-08-18", 2, "Grocery Store", "Pune", "Vegan", "Breakfast"),
        ("Chicken Curry", 15, "2025-08-19", 3, "Restaurant", "Mumbai", "Non-Vegetarian", "Lunch"),
        ("Fruit Basket", 30, "2025-08-21", 4, "Supermarket", "Mumbai", "Vegan", "Snacks"),
        ("Paneer Tikka", 10, "2025-08-18", 5, "Restaurant", "Pune", "Vegetarian", "Dinner")
    ])

    # Insert sample Claims
    cursor.executemany("""
    INSERT INTO Claims (Food_ID, Receiver_ID, Status, Timestamp)
    VALUES (?, ?, ?, ?)
    """, [
        (1, 1, "Completed", "2025-08-15 12:30:00"),
        (2, 3, "Pending", "2025-08-15 13:00:00"),
        (3, 2, "Completed", "2025-08-15 14:00:00"),
        (4, 4, "Cancelled", "2025-08-15 15:00:00"),
        (5, 1, "Completed", "2025-08-15 16:00:00")
    ])

    conn.commit()
    conn.close()
    print("✅ Sample data inserted successfully!")

if __name__ == "__main__":
    insert_sample_data()
