# 🍽️ Local Food Wastage Management System

## 📌 Project Overview
Food wastage is a serious issue where surplus food is discarded while many people struggle with hunger.  
This project connects **restaurants/individuals** who have surplus food with **NGOs/individuals** in need,  
using a **Streamlit web app + SQL database**.

✅ The system allows:
- Providers to list surplus food.
- Receivers to claim food.
- Real-time analytics on donations, claims, and wastage trends.

---

## 🛠️ Tech Stack
- **Python**
- **SQLite (SQL Database)**
- **Pandas**
- **Streamlit (Web App Framework)**

---

## 🎯 Features
### 🔹 CRUD Operations
- Add, View, Update, Delete **Providers**

### 🔹 Analytics Dashboard
- 📊 15+ SQL queries with auto-generated charts:
  - Providers & Receivers per city
  - Most common provider types
  - Food availability & demand trends
  - Claims distribution & success rates
  - Food items near expiry

### 🔹 Professional UI
- Sidebar navigation  
- Summary cards (Total Food Donated, Completed Claims, Top City)  
- Tabbed CRUD interface  
- About Page with project info  

---

## 📊 Sample Dashboard Preview
👉 *(Insert a screenshot of your app here after running it)*  

---

## 📂 Project Structure
FoodWastageApp/
├── app.py # Main Streamlit app
├── database_setup.py # Creates database & tables
├── crud_functions.py # CRUD operations
├── insert_sample_data.py # Inserts demo data
├── food_wastage.db # SQLite database (auto-created)
└── README.md # Project documentation


---

## 🚀 How to Run the Project

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/FoodWastageApp.git
   cd FoodWastageApp

2.  Install dependencies
    pip install streamlit pandas

3.  Create database tables
    python database_setup.py

4.  Insert sample data
    python insert_sample_data.py

5.  Run the Streamlit app
    streamlit run app.py

📈 Impact

Reduces food wastage by connecting surplus food providers with those in need.

Provides data insights to improve food distribution.

Contributes to SDG Goal 12: Responsible Consumption and Production.

👩‍💻 Developer

Name: Prerna Utage

Tech Stack: Python, Streamlit, SQLite, Pandas

Status: Fully Functional ✅

