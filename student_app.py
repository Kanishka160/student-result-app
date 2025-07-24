import sqlite3
import streamlit as st

# DB connection
conn = sqlite3.connect('students.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mark1 INTEGER,
        mark2 INTEGER,
        mark3 INTEGER
    )
''')
conn.commit()

st.title("🎓 Student Result Management App")

menu = ["Add Student", "View All", "Search", "Rank List"]
choice = st.sidebar.selectbox("Select Action", menu)

# Add student
if choice == "Add Student":
    st.subheader("➕ Add New Student")
    name = st.text_input("Enter Name")
    m1 = st.number_input("Mark 1", 0, 100)
    m2 = st.number_input("Mark 2", 0, 100)
    m3 = st.number_input("Mark 3", 0, 100)

if st.button("Add"):
    # Check if name already exists
    cursor.execute("SELECT * FROM students WHERE name=?", (name,))
    existing = cursor.fetchone()

    if existing:
        st.warning(f"{name} already exists! ❌ Please use a different name.")
    else:
        cursor.execute("INSERT INTO students (name, mark1, mark2, mark3) VALUES (?, ?, ?, ?)", (name, m1, m2, m3))
        conn.commit()
        st.success(f"{name} added successfully! ✅")


# View all
elif choice == "View All":
    st.subheader("📋 All Student Records")
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    st.dataframe(data)

# Search
elif choice == "Search":
    st.subheader("🔍 Search Student")
    search_name = st.text_input("Enter name to search")
    if st.button("Search"):
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search_name + '%',))
        results = cursor.fetchall()
        st.dataframe(results)

# Rank list
elif choice == "Rank List":
    st.subheader("🏆 Rank List")
    cursor.execute("SELECT name, (mark1+mark2+mark3) as total FROM students ORDER BY total DESC")
    data = cursor.fetchall()
    st.dataframe(data)

