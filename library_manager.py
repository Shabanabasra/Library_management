import streamlit as st
import pandas as pd
import json
import os
import time
import requests
from datetime import datetime
from streamlit_lottie import st_lottie
import plotly.express as px
import plotly.graph_objects as go

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

# Function to load Lottie animation
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load library from JSON file
def load_library():
    if os.path.exists("library.json"):
        with open("library.json", "r") as file:
            st.session_state.library = json.load(file)

# Save library to JSON file
def save_library():
    with open("library.json", "w") as file:
        json.dump(st.session_state.library, file)

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

# Remove a book
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        return True
    return False

# Search books
def search_books(search_term, search_by):
    search_term = search_term.lower()
    results = [book for book in st.session_state.library if search_term in book[search_by].lower()]
    st.session_state.search_results = results

# Get library statistics
def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read_status"])
    
    genres = {}
    authors = {}
    decades = {}

    for book in st.session_state.library:
        genres[book["genre"]] = genres.get(book["genre"], 0) + 1
        authors[book["author"]] = authors.get(book["author"], 0) + 1
        decade = (book["publication_year"] // 10) * 10
        decades[decade] = decades.get(decade, 0) + 1

    return {
        "total_books": total_books,
        "read_books": read_books,
        "genres": genres,
        "authors": authors,
        "decades": decades
    }

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

# View Library Section
if st.session_state.current_view == "library":
    st.markdown("<h2 class='sub_header'>Your Library 📚</h2>", unsafe_allow_html=True)

    if not st.session_state.library:
        st.markdown("<div class='warning-message'>Your library is empty. Add some books to get started!</div>", unsafe_allow_html=True)
    else:
        for i, book in enumerate(st.session_state.library):
            st.write(f"📖 **{book['title']}** by *{book['author']}* ({book['publication_year']}) - {book['genre']}")
            if st.button(f"Remove {book['title']}", key=f"remove_{i}"):
                remove_book(i)
                st.rerun()

# Add Book Section
elif st.session_state.current_view == "add":
    st.markdown("<h2 class='sub_header'>Add a New Book 📚</h2>", unsafe_allow_html=True)
    
    with st.form(key="add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, step=1)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance"])
        read_status = st.radio("Read Status", ["Read", "Unread"])
        read_bool = read_status == "Read"
        submit_button = st.form_submit_button(label="Add Book")

        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_bool)
            st.success("Book added successfully!")
            st.rerun()

# Library Statistics Section
elif st.session_state.current_view == "stats":
    st.markdown("<h2 class='sub_header'>Library Statistics 📊</h2>", unsafe_allow_html=True)
    stats = get_library_stats()
    st.write(f"📚 Total Books: {stats['total_books']}")
    st.write(f"✅ Books Read: {stats['read_books']}")

    # Visualization - Pie Chart for Read vs Unread Books
    fig = go.Figure(data=[go.Pie(labels=["Read", "Unread"], values=[stats['read_books'], stats['total_books'] - stats['read_books']])])
    st.plotly_chart(fig, use_container_width=True)

# Load Library
load_library()
