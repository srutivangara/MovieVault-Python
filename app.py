import streamlit as st
import json
import os 

st.set_page_config(
    page_title="MovieVault",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬MovieVault")
st.write("Welcome to my OTT watchlist Manager!")
movie_name = st.text_input("Movie Name")          # Text
ott = st.selectbox("OTT Platform", ["Netflix", "Prime", "Hotstar","Z5","Aha","SonyLiv","EtvWin"])
genre = st.selectbox("Genre", ["Action", "Comedy", "Sci-Fi","Drama","Horror","Thriller"])
status = st.radio("Watch Status",["Watched","Unwatched"])
rating = st.slider("Rating",1,5)
review = st.text_area("Review") 
#-----Loading Existing Movies------#
if os.path.exists("movies.json"):
    with open("movies.json", "r") as file:
        watchlist = json.load(file)
else:
    watchlist = []

if st.button("➕Add Movie"):
    movie={
        "title":movie_name,
        "platform": ott,
        "genre":genre,
        "status": status,
        "rating" : rating,
        "review" : review
    }
    watchlist.append(movie)

    with open("movies.json", "w") as file:
        json.dump(watchlist, file, indent=4)

    st.success("Movie added successfully!")
for movie in watchlist:
    st.write(f"🎬{movie['title']}")
    st.write(f"📺{movie['platform']}")
    st.write(f"🎭{movie['genre']}")
    st.write(f"👀{movie['status']}")
    st.write(f"⭐{movie['rating']}")
    st.write(f"📝{movie['review']}")
    st.divider()
search = st.text_input("Enter movie name: ")
def movie_search(watchlist,movie):
    for movie in watchlist:
        st.write(f"🎬{movie['title']}")
        st.write(f"📺{movie['platform']}")
        st.write(f"🎭{movie['genre']}")
        st.write(f"👀{movie['status']}")
        st.write(f"⭐{movie['rating']}")
        st.write(f"📝{movie['review']}")
        st.divider()
if search:
    if search.lower() in movie['title'].lower():
        movie_search(movie['title'])
    else:
        st.write("Movie NOT found")