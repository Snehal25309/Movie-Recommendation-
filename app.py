import os
import gdown
import joblib
import base64

FILE_ID = "1G1N7k2U9wS9DnVlA-krJw2zVRhZl4tFi"
OUTPUT = "similarity.joblib"

if not os.path.exists(OUTPUT):
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, OUTPUT, quiet=False)

similarity = joblib.load(OUTPUT)

import pandas as pd
import streamlit as st
import pickle

st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎥",
    layout="wide"
)
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()
img = get_base64("background.jpg")
st.markdown(f"""
<style>

.stApp {{
    background-image: url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

[data-testid="stHeader"]{{
    background: rgba(0,0,0,0);
}}

.main > div {{
    background: rgba(0,0,0,0.65);
    padding:20px;
    border-radius:15px;
}}

h1,h2,h3,h4,h5,h6,p,label,span{{
    color:white !important;
}}

</style>
""", unsafe_allow_html=True)

df = pd.read_csv('cleaned_data.csv')
similarities = joblib.load(open("similarity.joblib",'rb'))

movies = df['title'].tolist()



st.title("🎬 Movie Recommendation System")
st.markdown("### Discover movies similar to your favorites!")

st.divider()


def get_name_by_index(i):
    if i < len(df) and i>0:
        return df.loc[i,'title']
    else:
        return''

def get_index_from_name(name):
    clean_user_name = name.strip().lower().replace(' ', '').replace('-', '')
    
    match = df[df['title'].str.lower().str.replace(' ', '').str.replace('-', '') == clean_user_name]
    
    if not match.empty:
        return match.index[0]
    return -1

# -------------------------------

left, right = st.columns([2, 1])

with left:
    name = st.selectbox(
        "🎥 Select a Movie",
        movies,
        index=None,
        placeholder="Choose a movie..."
    )

with right:
    st.metric("🎬 Total Movies", len(movies))

st.divider()

# -------------------------------

if st.button("Recommend"):
    index = get_index_from_name(name)
    if index == -1:
        st.write("Movie not found. Please check the spelling and try again.")
    else:
        st.write(f"Recommendations for '{name}' will be displayed here.")
        st.write(f"Movie index is { index }")
        similarity_indexes = list(enumerate(similarities[index]))
        similarity_indexes = sorted(similarity_indexes, key=lambda x: x[1], reverse=True)
        
        cols = st.columns(2)
        for i in range(1, 6):

    # Get recommended movie index
            movie_index = similarity_indexes[i][0]

    # Get movie title
            movie_name = get_name_by_index(movie_index)

            with cols[(i - 1) % 2]:
                with st.container(border=True):
                    st.write(f"### 🎬 {movie_name}")
                    st.caption(f"Recommendation #{i}")

            st.balloons()
st.divider()


st.caption("Made by Snehal Kolekar with ❤️ using Python, Pandas, Pickle & Streamlit")
