import streamlit as st
import sqlite3
import pandas as pd
from database_setup import create_tables
from crud_functions import add_provider, view_providers, update_provider, delete_provider

# ---------- INITIAL SETUP ----------
create_tables()
st.set_page_config(page_title="Local Food Wastage Management", layout="wide", page_icon="🍽️")

# ---------- FUNCTIONS ----------
def run_query(query):
    conn = sqlite3.connect("food_wastage.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ---------- SIDEBAR MENU ----------
st.sidebar.title("🍽️ Food Wastage Management")
menu = ["🏠 Home", "📂 Manage Providers", "📊 Analytics Dashboard", "ℹ️ About"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- HOME ----------
if choice == "🏠 Home":
    st.title("Local Food Wastage Management System")
    st.markdown("""
    ### 🌟 Project Overview
    This platform connects **restaurants & individuals** with surplus food to **NGOs & people in need**.  
    The aim is to **reduce food waste** and **fight hunger**.

    **Key Features:**
    - Add, View, Update, and Delete provider records.
    - Real-time analytics to track food donations.
    - Simple, user-friendly interface for quick adoption.
    """)

    # Quick Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("🥗 Total Providers", run_query("SELECT COUNT(*) FROM Providers").iloc[0, 0])
    col2.metric("📦 Total Food Listings", run_query("SELECT COUNT(*) FROM Food_Listings").iloc[0, 0])
    col3.metric("🏙️ Cities Covered", run_query("SELECT COUNT(DISTINCT City) FROM Providers").iloc[0, 0])

# ---------- MANAGE PROVIDERS ----------
elif choice == "📂 Manage Providers":
    st.header("Manage Provider Data")
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Add", "📋 View", "✏️ Update", "🗑️ Delete"])

    with tab1:
        st.subheader("Add New Provider")
        name = st.text_input("Name")
        type_ = st.text_input("Type")
        address = st.text_input("Address")
        city = st.text_input("City")
        contact = st.text_input("Contact")
        if st.button("Add Provider"):
            add_provider(name, type_, address, city, contact)
            st.success("✅ Provider added successfully!")

    with tab2:
        st.subheader("All Providers")
        st.dataframe(view_providers())

    with tab3:
        st.subheader("Update Provider")
        pid = st.number_input("Provider ID", min_value=1)
        name = st.text_input("New Name")
        type_ = st.text_input("New Type")
        address = st.text_input("New Address")
        city = st.text_input("New City")
        contact = st.text_input("New Contact")
        if st.button("Update Provider"):
            update_provider(pid, name, type_, address, city, contact)
            st.success("✅ Provider updated successfully!")

    with tab4:
        st.subheader("Delete Provider")
        pid = st.number_input("Provider ID to Delete", min_value=1, key="del")
        if st.button("Delete Provider"):
            delete_provider(pid)
            st.success("🗑️ Provider deleted successfully!")

# ---------- ANALYTICS ----------
elif choice == "📊 Analytics Dashboard":
    st.header("📊 Food Wastage Analytics")

    # ---------- SUMMARY CARDS ----------
    col1, col2, col3 = st.columns(3)

    total_food = run_query("SELECT IFNULL(SUM(Quantity),0) as Total_Food FROM Food_Listings").iloc[0, 0]
    completed_claims = run_query("SELECT COUNT(*) as Completed FROM Claims WHERE Status='Completed'").iloc[0, 0]
    top_city = run_query("""SELECT Location 
                            FROM Food_Listings 
                            GROUP BY Location 
                            ORDER BY SUM(Quantity) DESC LIMIT 1""")

    col1.metric("🥗 Total Food Donated", f"{total_food}")
    col2.metric("✅ Completed Claims", f"{completed_claims}")
    if not top_city.empty:
        col3.metric("🏙️ Top City for Donations", top_city.iloc[0, 0])
    else:
        col3.metric("🏙️ Top City for Donations", "N/A")

    st.markdown("---")  # Divider line

    # ---------- ALL QUERIES ----------
    queries = {
        # Providers & Receivers
        "1. Providers & Receivers per City":
            """SELECT P.City, COUNT(DISTINCT P.Provider_ID) as Providers, COUNT(DISTINCT R.Receiver_ID) as Receivers
               FROM Providers P LEFT JOIN Receivers R ON P.City = R.City
               GROUP BY P.City""",

        "2. Provider Type Contributions":
            """SELECT Type, COUNT(*) as Total_Providers
               FROM Providers
               GROUP BY Type
               ORDER BY Total_Providers DESC""",

        "3. Provider Contact Info (by City)":
            """SELECT Name, City, Contact
               FROM Providers
               ORDER BY City""",

        "4. Top Receivers by Claims":
            """SELECT R.Name, COUNT(C.Claim_ID) as Total_Claims
               FROM Receivers R JOIN Claims C ON R.Receiver_ID = C.Receiver_ID
               GROUP BY R.Name
               ORDER BY Total_Claims DESC LIMIT 10""",

        # Food Listings & Availability
        "5. Total Quantity of Food Available":
            """SELECT SUM(Quantity) as Total_Food
               FROM Food_Listings""",

        "6. City with Most Food Listings":
            """SELECT Location, COUNT(*) as Listings
               FROM Food_Listings
               GROUP BY Location
               ORDER BY Listings DESC LIMIT 1""",

        "7. Most Common Food Types":
            """SELECT Food_Type, COUNT(*) as Count
               FROM Food_Listings
               GROUP BY Food_Type
               ORDER BY Count DESC""",

        # Claims & Distribution
        "8. Claims per Food Item":
            """SELECT F.Food_Name, COUNT(C.Claim_ID) as Total_Claims
               FROM Food_Listings F JOIN Claims C ON F.Food_ID = C.Food_ID
               GROUP BY F.Food_Name
               ORDER BY Total_Claims DESC""",

        "9. Provider with Most Successful Claims":
            """SELECT P.Name, COUNT(C.Claim_ID) as Successful_Claims
               FROM Providers P
               JOIN Food_Listings F ON P.Provider_ID = F.Provider_ID
               JOIN Claims C ON F.Food_ID = C.Food_ID
               WHERE C.Status = 'Completed'
               GROUP BY P.Name
               ORDER BY Successful_Claims DESC LIMIT 1""",

        "10. Claim Status Distribution":
            """SELECT Status, COUNT(*) as Count
               FROM Claims
               GROUP BY Status""",

        # Analysis & Insights
        "11. Average Quantity Claimed per Receiver":
            """SELECT R.Name, AVG(F.Quantity) as Avg_Quantity
               FROM Receivers R
               JOIN Claims C ON R.Receiver_ID = C.Receiver_ID
               JOIN Food_Listings F ON C.Food_ID = F.Food_ID
               GROUP BY R.Name""",

        "12. Most Claimed Meal Type":
            """SELECT Meal_Type, COUNT(*) as Claims
               FROM Food_Listings F JOIN Claims C ON F.Food_ID = C.Food_ID
               GROUP BY Meal_Type
               ORDER BY Claims DESC LIMIT 1""",

        "13. Total Food Donated by Each Provider":
            """SELECT P.Name, SUM(F.Quantity) as Total_Donated
               FROM Providers P
               JOIN Food_Listings F ON P.Provider_ID = F.Provider_ID
               GROUP BY P.Name
               ORDER BY Total_Donated DESC""",

        # Extra Insights
        "14. Top 5 Cities with Highest Food Donations":
            """SELECT Location, SUM(Quantity) as Total_Quantity
               FROM Food_Listings
               GROUP BY Location
               ORDER BY Total_Quantity DESC LIMIT 5""",

        "15. Food Items Near Expiry (next 3 days)":
            """SELECT Food_Name, Expiry_Date, Quantity
               FROM Food_Listings
               WHERE date(Expiry_Date) <= date('now','+3 day')
               ORDER BY Expiry_Date ASC"""
    }

    # Display all queries with charts
    for title, sql in queries.items():
        st.subheader(title)
        df = run_query(sql)
        if df.empty:
            st.info("No data available yet for this query.")
        else:
            st.dataframe(df)
            # Auto chart for numeric data
            if df.shape[1] > 1 and df.dtypes[1] in ["int64", "float64"]:
                st.bar_chart(df.set_index(df.columns[0]))


    # Loop through and display queries
    for title, sql in queries.items():
        st.subheader(title)
        df = run_query(sql)
        if df.empty:
            st.info("No data available yet for this query.")
        else:
            st.dataframe(df)
            # Show chart if data is numeric
            if df.shape[1] > 1 and df.dtypes[1] in ["int64", "float64"]:
                st.bar_chart(df.set_index(df.columns[0]))


# ---------- ABOUT ----------
elif choice == "ℹ️ About":
    st.title("About This Project")
    
    st.markdown("**Developer:** Prerna Utage")
    st.markdown("**Tech Stack:** Python, Streamlit, SQLite, Pandas")
    st.markdown("**Purpose:** Reduce food wastage and connect donors to those in need.")
    st.markdown("**Status:** Fully Functional ✅")

