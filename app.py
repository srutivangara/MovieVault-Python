import streamlit as st
import json
import os

st.set_page_config(
    page_title="MovieVault",
    page_icon="🎬",
    layout="wide"
)

# ------------------- CSS ------------------- #

st.markdown("""
<style>

/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* ===========================
   APP BACKGROUND
=========================== */

.stApp{
    background: linear-gradient(
    -45deg,
    #0F172A,
    #1E1B4B,
    #312E81,
    #111827);

    background-size:400% 400%;

    animation: gradient 15s ease infinite;

    color:white;
}

@keyframes gradient{

0%{
background-position:0% 50%;
}

50%{
background-position:100% 50%;
}

100%{
background-position:0% 50%;
}

}

/* ===========================
   TITLES
=========================== */

h1{

font-size:50px;

font-weight:700;

text-align:center;

color:white;

letter-spacing:2px;

}

h2,h3{

color:#F8FAFC;

}

/* ===========================
   GLASS CARDS
=========================== */

div[data-testid="stVerticalBlock"]{

background:rgba(255,255,255,.06);

backdrop-filter:blur(12px);

padding:18px;

border-radius:20px;

border:1px solid rgba(255,255,255,.12);

margin-bottom:15px;

}

/* ===========================
   INPUTS
=========================== */

.stTextInput input{

background:#1E293B;

color:white;

border-radius:15px;

border:2px solid #7C3AED;

padding:12px;

}

.stTextArea textarea{

background:#1E293B;

color:white;

border-radius:15px;

border:2px solid #7C3AED;

}

div[data-baseweb="select"]{

border-radius:15px;

}

/* ===========================
   BUTTON
=========================== */

.stButton > button{

width:100%;

height:55px;

font-size:18px;

font-weight:bold;

border-radius:15px;

border:none;

color:white;

background:linear-gradient(
90deg,
#7C3AED,
#EC4899);

transition:.35s;

}

.stButton > button:hover{

transform:translateY(-4px);

box-shadow:0 10px 30px rgba(236,72,153,.5);

}

/* ===========================
   METRICS
=========================== */

div[data-testid="metric-container"]{

background:rgba(255,255,255,.08);

padding:18px;

border-radius:18px;

border:1px solid rgba(255,255,255,.15);

}

/* ===========================
   SUCCESS
=========================== */

.stSuccess{

border-radius:15px;

}

/* ===========================
   SCROLLBAR
=========================== */

::-webkit-scrollbar{

width:8px;

}

::-webkit-scrollbar-thumb{

background:#7C3AED;

border-radius:20px;

}

::-webkit-scrollbar-track{

background:#111827;

}

</style>
""", unsafe_allow_html=True)

st.title("🎬 MovieVault")
st.caption("Your Personal OTT Watchlist Manager")

# ------------------- File ------------------- #

FILE_NAME = "movies.json"

# ------------------- Functions ------------------- #

def load_movies():

    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, "r") as file:
            return json.load(file)

    return []


def save_movies(movies):

    with open(FILE_NAME, "w") as file:
        json.dump(movies, file, indent=4)


def average_rating(movies):

    if len(movies) == 0:
        return 0

    total = sum(movie["rating"] for movie in movies)

    return round(total / len(movies), 1)


def movie_exists(title, movies):

    for movie in movies:

        if movie["title"].lower() == title.lower():
            return True

    return False


movies = load_movies()

# ------------------- Dashboard ------------------- #

watched = len([m for m in movies if m["status"] == "Watched"])

unwatched = len(movies) - watched

avg = average_rating(movies)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("🎬 Total Movies", len(movies))

with c2:
    st.metric("✅ Watched", watched)

with c3:
    st.metric("⏳ Unwatched", unwatched)

with c4:
    st.metric("⭐ Avg Rating", avg)

st.divider()

# ------------------- Add Movie ------------------- #

st.subheader("➕ Add New Movie")

col1, col2 = st.columns(2)

with col1:

    movie_name = st.text_input("Movie Name")

    ott = st.selectbox(
        "OTT Platform",
        [
            "Netflix",
            "Prime Video",
            "Hotstar",
            "SonyLiv",
            "ZEE5",
            "Aha",
            "ETV Win"
        ]
    )

    genre = st.selectbox(
        "Genre",
        [
            "Action",
            "Comedy",
            "Drama",
            "Sci-Fi",
            "Thriller",
            "Horror",
            "Romance",
            "Adventure"
        ]
    )

with col2:

    status = st.radio(
        "Watch Status",
        ["Watched", "Unwatched"]
    )

    rating = st.feedback("stars")

    review = st.text_area("Review")

if st.button("➕ Add Movie", use_container_width=True):

    if movie_name.strip() == "":
        st.error("Movie name cannot be empty.")

    elif movie_exists(movie_name, movies):
        st.warning("Movie already exists.")

    else:

        movies.append({

            "title": movie_name,

            "platform": ott,

            "genre": genre,

            "status": status,

            "rating": rating,

            "review": review

        })

        save_movies(movies)

        st.success("Movie added successfully!")

        st.rerun()

st.divider()
# ------------------- Search & Filters ------------------- #

st.subheader("🔍 Search & Filter Movies")

search = st.text_input("Search Movie")

c1, c2, c3 = st.columns(3)

with c1:
    platform_filter = st.selectbox(
        "Platform",
        ["All"] + sorted(list(set(movie["platform"] for movie in movies)))
        if movies else ["All"]
    )

with c2:
    genre_filter = st.selectbox(
        "Genre",
        ["All"] + sorted(list(set(movie["genre"] for movie in movies)))
        if movies else ["All"]
    )

with c3:
    status_filter = st.selectbox(
        "Status",
        ["All", "Watched", "Unwatched"]
    )

# ------------------- Filter Logic ------------------- #

filtered_movies = movies.copy()

if search.strip():

    filtered_movies = sorted(
        filtered_movies,
        key=lambda x: (
            not x["title"].lower().startswith(search.lower()),
            search.lower() not in x["title"].lower(),
            x["title"].lower()
        )
    )

    filtered_movies = [
        movie for movie in filtered_movies
        if search.lower() in movie["title"].lower()
    ]

if platform_filter != "All":
    filtered_movies = [
        movie for movie in filtered_movies
        if movie["platform"] == platform_filter
    ]

if genre_filter != "All":
    filtered_movies = [
        movie for movie in filtered_movies
        if movie["genre"] == genre_filter
    ]

if status_filter != "All":
    filtered_movies = [
        movie for movie in filtered_movies
        if movie["status"] == status_filter
    ]

st.divider()

st.subheader("🎬 Movie Collection")

if len(filtered_movies) == 0:

    st.info("No movies found.")

else:

    for index, movie in enumerate(filtered_movies):

        with st.container(border=True):

            top1, top2 = st.columns([5,1])

            with top1:
                st.subheader(movie["title"])

            with top2:
                st.write("⭐" * movie["rating"])

            left, right = st.columns(2)

            with left:

                st.write(f"📺 **Platform:** {movie['platform']}")
                st.write(f"🎭 **Genre:** {movie['genre']}")

            with right:

                st.write(f"👁 **Status:** {movie['status']}")
                st.write(f"⭐ **Rating:** {movie['rating']}/5")

            st.write("📝 **Review**")

            if movie["review"].strip() == "":
                st.caption("No review added.")
            else:
                st.write(movie["review"])

            b1, b2 = st.columns(2)

            with b1:

                edit = st.button(
                    "✏ Edit",
                    key=f"edit_{index}",
                    use_container_width=True
                )

            with b2:

                delete = st.button(
                    "🗑 Delete",
                    key=f"delete_{index}",
                    use_container_width=True
                )

            # Save clicked movie for editing
            if edit:
                st.session_state["edit_index"] = movies.index(movie)

            # Delete movie
            if delete:

                movies.remove(movie)

                save_movies(movies)

                st.success("Movie deleted successfully!")

                st.rerun()
# ------------------- Edit Movie ------------------- #

if "edit_index" in st.session_state:

    idx = st.session_state["edit_index"]

    if idx < len(movies):

        st.divider()
        st.subheader("✏ Edit Movie")

        movie = movies[idx]

        title = st.text_input(
            "Movie Name",
            value=movie["title"],
            key="edit_title"
        )

        platform = st.selectbox(
            "Platform",
            [
                "Netflix",
                "Prime Video",
                "Hotstar",
                "SonyLiv",
                "ZEE5",
                "Aha",
                "ETV Win"
            ],
            index=[
                "Netflix",
                "Prime Video",
                "Hotstar",
                "SonyLiv",
                "ZEE5",
                "Aha",
                "ETV Win"
            ].index(movie["platform"]),
            key="edit_platform"
        )

        genre = st.selectbox(
            "Genre",
            [
                "Action",
                "Comedy",
                "Drama",
                "Sci-Fi",
                "Thriller",
                "Horror",
                "Romance",
                "Adventure"
            ],
            index=[
                "Action",
                "Comedy",
                "Drama",
                "Sci-Fi",
                "Thriller",
                "Horror",
                "Romance",
                "Adventure"
            ].index(movie["genre"]),
            key="edit_genre"
        )

        status = st.radio(
            "Watch Status",
            ["Watched", "Unwatched"],
            index=0 if movie["status"] == "Watched" else 1,
            key="edit_status"
        )

        rating = st.slider(
            "Rating",
            1,
            5,
            movie["rating"],
            key="edit_rating"
        )

        review = st.text_area(
            "Review",
            value=movie["review"],
            key="edit_review"
        )

        c1, c2 = st.columns(2)

        with c1:

            if st.button("💾 Save Changes", use_container_width=True):

                movies[idx]["title"] = title
                movies[idx]["platform"] = platform
                movies[idx]["genre"] = genre
                movies[idx]["status"] = status
                movies[idx]["rating"] = rating
                movies[idx]["review"] = review

                save_movies(movies)

                del st.session_state["edit_index"]

                st.success("Movie updated successfully!")

                st.rerun()

        with c2:

            if st.button("❌ Cancel", use_container_width=True):

                del st.session_state["edit_index"]

                st.rerun()

# ------------------- Footer ------------------- #

st.divider()
