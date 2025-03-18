import streamlit as st
import pandas as pd
import json
import os
import time
import random
import requests
from datetime import datetime
from streamlit_lottie import st_lottie
# import plotly.express as px
# import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Personal Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub_header {
        font-size: 1.8rem !important;
        color: #3882F6;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #ECFDF5;
        border-left: 5px solid #108981;
        border-radius: 0.375rem;
    } 
    .warning-message {
        padding: 1rem;
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        border-radius: 0.375rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to load Lottie animation
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Initialize session state variables
if "library" not in st.session_state:
    st.session_state.library = []
if "search_results" not in st.session_state:
    st.session_state.search_results = [] 
if "book_added" not in st.session_state:
    st.session_state.book_added = False 
if "book_removed" not in st.session_state:
    st.session_state.book_removed = False
if "current_view" not in st.session_state:
    st.session_state.current_view = "library"

# Load library
def load_library():
    try:
        if os.path.exists("library.json"):
            with open("library.json", "r") as file:
                st.session_state.library = json.load(file)
    except Exception as e:
        st.error(f"Error loading library: {e}")

# Save library
def save_library():
    try:
        with open("library.json", "w") as file:
            json.dump(st.session_state.library, file)
    except Exception as e:
        st.error(f"Error saving library: {e}")

# Add a book to the library
def add_book(title, author, publication_year, genre, read_status):
    book = {
        "title": title,
        "author": author,
        "publication_year": publication_year,
        "genre": genre,
        "read_status": read_status,
        "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }                 
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)  # Animation delay

# Remove book function
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True

# Sidebar navigation
st.sidebar.markdown("<h1 style='text-align: center;'>Navigation</h1>", unsafe_allow_html=True)

nav_options = st.sidebar.radio(
    "Choose an option",
    ["View Library", "Add Book", "Search Books", "Library Statistics"]
)

if nav_options == "View Library":
    st.session_state.current_view = "library"
elif nav_options == "Add Book":
    st.session_state.current_view = "add"
elif nav_options == "Search Books":
    st.session_state.current_view = "search"
elif nav_options == "Library Statistics":
    st.session_state.current_view = "stats"

st.markdown("<h1 class='main-header'>Personal Library Manager</h1>", unsafe_allow_html=True)

# Add book section
if st.session_state.current_view == "add":
    st.markdown("<h2 class='sub_header'>Add a New Book 📚</h2>", unsafe_allow_html=True)    

    with st.form(key="add_book_form"):
        title = st.text_input("Book Title", max_chars=100)
        author = st.text_input("Author", max_chars=100)
        publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, step=1, value=2023)
        genre = st.selectbox("Genre", [
            "Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance"
        ])
        read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True)
        read_bool = read_status == "Read"

        submit_button = st.form_submit_button(label="Add Book")

        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_bool)
            st.markdown("<div class='success-message'>📖 Book added successfully!</div>", unsafe_allow_html=True)
            st.balloons()
            st.session_state.book_added = False

# View Library Section
elif st.session_state.current_view == "library":
    st.markdown("<h2 class='sub_header'>Your Library 📚</h2>", unsafe_allow_html=True)

    if not st.session_state.library:
        st.markdown("<div class='warning-message'>Your library is empty. Add some books to get started!</div>", unsafe_allow_html=True)
    else:
        for i, book in enumerate(st.session_state.library):
            st.write(f"📖 **{book['title']}** by *{book['author']}* ({book['publication_year']}) - {book['genre']}")
            if st.button(f"Remove {book['title']}", key=f"remove_{i}"):
                remove_book(i)
                st.rerun()

# If book is removed, show success message
if st.session_state.book_removed:
    st.markdown("<div class='success-message'>📖 Book removed successfully!</div>", unsafe_allow_html=True)
    st.session_state.book_removed = False

# Search Books Section
elif st.session_state.current_view == "search":
    st.markdown("<h2 class='sub_header'>🔎 Search Books</h2>", unsafe_allow_html=True)

# Library Statistics Section
elif st.session_state.current_view == "stats":
    st.markdown("<h2 class='sub_header'>📊 Library Statistics</h2>", unsafe_allow_html=True)

# Load Library
load_library()
