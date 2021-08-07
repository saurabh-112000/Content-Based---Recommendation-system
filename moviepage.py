import pandas as pd
import streamlit as st
import pickle
import requests
from PIL import Image
import sklearn
import PIL
from sklearn.feature_extraction.text import TfidfVectorizer

def final():
    im1 = Image.open("Not_found.jpg")
    empty_poster_set = set(('https://image.tmdb.org/t/p/w500/None', 'https://image.tmdb.org/t/p/w500/'))

    def get_poster(reqid, code):
        response = requests.get("https://api.themoviedb.org/3/find/{}?api_key=<yourapikey>&language=en-US&external_source=imdb_id".format(reqid))
        data = response.json()
        result = data
        getvalues = lambda key, inputData: [subVal[key] for subVal in inputData if key in subVal]
        if code == 0:
            temp = getvalues("poster_path", result["tv_results"])
        else:
            temp = getvalues("poster_path", result["movie_results"])
        # if len(temp) == 0:
        # return im1
        # else:
        tempstr = ''.join(map(str, temp))
        final_path = "https://image.tmdb.org/t/p/w500/" + tempstr
        return final_path

    def recommend(name,dur):
        code = 1
        data = data_frame[data_frame['type'] == "Movie"]
        data.reset_index(drop=True, inplace=True)
        if dur == 'Any':
            tfidfvec = TfidfVectorizer()
            temp = tfidfvec.fit_transform((data["tags"]))
            from sklearn.metrics.pairwise import cosine_similarity
            cos_sim = cosine_similarity(temp, temp)
        else:
            data = data[data['duration_as_int'] < dur]
            data.reset_index(drop=True, inplace=True)
            lst = data_frame[data_frame['title'] == name]
            data = data.append(lst, ignore_index=True)
            data.reset_index(drop=True, inplace=True)
            tfidfvec = TfidfVectorizer()
            temp = tfidfvec.fit_transform((data["tags"]))
            from sklearn.metrics.pairwise import cosine_similarity
            cos_sim = cosine_similarity(temp, temp)

        index = data[data['title'] == name].index[0]
        dist = cos_sim[index]
        rec_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:11]
        rec_output_title = []
        rec_output_actor_1 = []
        rec_output_actor_2 = []
        rec_output_actor_3 = []
        rec_output_dir = []
        rec_output_dur = []
        rec_output_description = []
        rec_output_poster = []
        for i in rec_list:
            i_d = data.iloc[i[0]].imdb_id
            reqid = 'tt' + str(i_d)
            rec_output_title.append(data.iloc[i[0]].title)
            rec_output_actor_1.append(data.iloc[i[0]].actor_one)
            rec_output_actor_2.append(data.iloc[i[0]].actor_two)
            rec_output_actor_3.append(data.iloc[i[0]].actor_three)
            rec_output_dir.append(data.iloc[i[0]].Director)
            rec_output_dur.append(data.iloc[i[0]].Duration)
            rec_output_description.append(data.iloc[i[0]].Description)
            rec_output_poster.append(get_poster(reqid, code))

        return rec_output_title, rec_output_actor_1, rec_output_actor_2, rec_output_actor_3, rec_output_dir, rec_output_dur, rec_output_description, rec_output_poster


    data_base = pickle.load(open('database.pkl', 'rb'))
    data_frame = pd.DataFrame(data_base)

    movie_dur_options = [90, 120, 150, 'Any']
    st.subheader("Recommendations for Movies")
    temp_dur_movie = st.select_slider("Choose duration limit (hrs)", options=movie_dur_options)
    user_input = st.selectbox('Enter the title', data_frame['title'].values)

    if st.button('Recommend'):
        output_title,output_ac1,output_ac2,output_ac3,output_dir,output_dur,output_descrip,posters = recommend(user_input,temp_dur_movie)
        indices = [index for index, element in enumerate(posters) if element in empty_poster_set]
        for i in indices:
            posters[i] = im1

        st.subheader(output_title[0])
        st.write("__Cast :__", output_ac1[0], ",", output_ac2[0], ",", output_ac3[0])
        st.write("__Director :__", output_dir[0])
        st.write("__Duration :__", output_dur[0])
        st.write("__Description :__", output_descrip[0])
        st.markdown("##")
        st.image(posters[0], width=200)
        st.markdown("###")

        st.subheader(output_title[1])
        st.write("__Cast :__", output_ac1[1], ",", output_ac2[1], ",", output_ac3[1])
        st.write("__Director :__", output_dir[1])
        st.write("__Duration :__", output_dur[1])
        st.write("__Description :__", output_descrip[1])
        st.markdown("##")
        st.image(posters[1], width=200)
        st.markdown("###")

        st.subheader(output_title[2])
        st.write("__Cast :__", output_ac1[2], ",", output_ac2[2], ",", output_ac3[2])
        st.write("__Director :__", output_dir[2])
        st.write("__Duration :__", output_dur[2])
        st.write("__Description :__", output_descrip[2])
        st.markdown("##")
        st.image(posters[2], width=200)
        st.markdown("###")

        st.subheader(output_title[3])
        st.write("__Cast :__", output_ac1[3], ",", output_ac2[3], ",", output_ac3[3])
        st.write("__Director :__", output_dir[3])
        st.write("__Duration :__", output_dur[3])
        st.write("__Description :__", output_descrip[3])
        st.markdown("##")
        st.image(posters[3], width=200)
        st.markdown("###")

        st.subheader(output_title[4])
        st.write("__Cast :__", output_ac1[4], ",", output_ac2[4], ",", output_ac3[4])
        st.write("__Director :__", output_dir[4])
        st.write("__Duration :__", output_dur[4])
        st.write("__Description :__", output_descrip[4])
        st.markdown("##")
        st.image(posters[4], width=200)
        st.markdown("###")

        st.subheader(output_title[5])
        st.write("__Cast :__", output_ac1[5], ",", output_ac2[5], ",", output_ac3[5])
        st.write("__Director :__", output_dir[5])
        st.write("__Duration :__", output_dur[5])
        st.write("__Description :__", output_descrip[5])
        st.markdown("##")
        st.image(posters[5], width=200)
        st.markdown("###")

        st.subheader(output_title[6])
        st.write("__Cast :__", output_ac1[6], ",", output_ac2[6], ",", output_ac3[6])
        st.write("__Director :__", output_dir[6])
        st.write("__Duration :__", output_dur[6])
        st.write("__Description :__", output_descrip[6])
        st.markdown("##")
        st.image(posters[6], width=200)
        st.markdown("###")

        st.subheader(output_title[7])
        st.write("__Cast :__", output_ac1[7], ",", output_ac2[7], ",", output_ac3[7])
        st.write("__Director :__", output_dir[7])
        st.write("__Duration :__", output_dur[7])
        st.write("__Description :__", output_descrip[7])
        st.markdown("##")
        st.image(posters[7], width=200)
        st.markdown("###")

        st.subheader(output_title[8])
        st.write("__Cast :__", output_ac1[8], ",", output_ac2[8], ",", output_ac3[8])
        st.write("__Director :__", output_dir[8])
        st.write("__Duration :__", output_dur[8])
        st.write("__Description :__", output_descrip[8])
        st.markdown("##")
        st.image(posters[8], width=200)
        st.markdown("###")

        st.subheader(output_title[9])
        st.write("__Cast :__", output_ac1[9], ",", output_ac2[9], ",", output_ac3[9])
        st.write("__Director :__", output_dir[9])
        st.write("__Duration :__", output_dur[9])
        st.write("__Description :__", output_descrip[9])
        st.image(posters[9], width=200)
