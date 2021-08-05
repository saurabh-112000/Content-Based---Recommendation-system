import moviepage
import tvpage
import streamlit as st


pgs = {
    "Movies": moviepage,
    "TV Shows": tvpage
}


st.title("Netflix Movie/Tv Show Recommendation System")
st.sidebar.title('Choose from content')
selection = st.sidebar.radio("Go to", list(pgs.keys()))
page = pgs[selection]
page.final()


