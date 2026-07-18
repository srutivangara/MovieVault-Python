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
rating = st.feedback("stars")
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

# ---------------- SEARCH MOVIE ---------------- #

search = st.text_input("🔍 Search by Movie or Platform")

if search:
    found = False

    for movie in watchlist:
        if (search.lower() in movie["title"].lower() or search.lower() in movie["platform"].lower()):

            found = True

            st.markdown("---")
            col1, col2 = st.columns([4,1])

            with col1:
                st.subheader(movie["title"])
                st.write("📺 Platform :", movie["platform"])
                st.write("🎭 Genre :", movie["genre"])
                st.write("👁 Status :", movie["status"])
                st.write("⭐ Rating :", "⭐"*movie["rating"])
                st.write("📝 Review :", movie["review"])

            with col2:

                if st.button("🗑 Delete", key=f"delete_{movie['title']}"):
                    watchlist.remove(movie)

                    with open("movies.json","w") as file:
                        json.dump(watchlist,file,indent=4)

                    st.success("Movie Deleted Successfully!")
                    st.rerun()

                if st.button("✏ Edit", key=f"edit_{movie['title']}"):

                    new_platform = st.selectbox(
                        "Platform",
                        ["Netflix","Prime","Hotstar","Z5","Aha","SonyLiv","EtvWin"],
                        key=f"platform_{movie['title']}"
                    )

                    new_genre = st.selectbox(
                        "Genre",
                        ["Action","Comedy","Sci-Fi","Drama","Horror","Thriller"],
                        key=f"genre_{movie['title']}"
                    )

                    new_status = st.radio(
                        "Status",
                        ["Watched","Unwatched"],
                        key=f"status_{movie['title']}"
                    )

                    new_rating = st.slider(
                        "Rating",
                        1,
                        5,
                        movie["rating"],
                        key=f"rating_{movie['title']}"
                    )

                    new_review = st.text_area(
                        "Review",
                        movie["review"],
                        key=f"review_{movie['title']}"
                    )

                    if st.button("Save Changes", key=f"save_{movie['title']}"):

                        movie["platform"] = new_platform
                        movie["genre"] = new_genre
                        movie["status"] = new_status
                        movie["rating"] = new_rating
                        movie["review"] = new_review

                        with open("movies.json","w") as file:
                            json.dump(watchlist,file,indent=4)

                        st.success("Movie Updated Successfully!")
                        st.rerun()

    if not found:
        st.error("Movie NOT Found")