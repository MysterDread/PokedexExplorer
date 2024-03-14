import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
import requests
import numpy as np

st.title("Pokemon Explorer!")

def get_details(poke_number):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        return pokemon['name'], pokemon['height'], pokemon['weight'], len(pokemon['moves']), [t['type']['name'] for t in pokemon['types']], pokemon['sprites']['other']['official-artwork']['front_default'], pokemon['cries']['latest']
    except Exception as e:
        print(e)
        return 'Error', np.nan, np.nan, np.nan, None

pokemon_number = st.slider("Pick a pokemon",
                           min_value=1,
                           max_value=1008
                           )

name, height, weight, moves, types, sprite_url, cry_url = get_details(pokemon_number)
height = height * 10

height_data = pd.DataFrame({'Pokemon': ['weedle', name , 'Dragonair'],
                            'Heights': [30, height, 220]})
colour_mapper = {"normal":"#00b3b3",
                 "fire":"#ffa64d", 
                 "water":"#6699ff", 
                 "grass":"#00cc66", 
                 "flying":"#66ccff", 
                 "fighting":"#ff0066", 
                 "poison":"#cc00ff", 
                 "electric":"#ffff00", 
                 "ground":"#996633", 
                 "rock":"#b8b894", 
                 "psychic":"#ff6666", 
                 "ice":"#66ffff", 
                 "bug":"#33cc33", 
                 "ghost":"#0099ff", 
                 "steel":"#79a6d2", 
                 "dragon":"#3366cc", 
                 "dark":"#006666", 
                 "fairy":"#cc99ff"}
colours = colours = ['gray', colour_mapper[types[0]], 'gray'] if types else ['gray', 'gray', 'gray']
col1, col2 = st.columns(2)
col1.header(f"{name.title()}")
col1.image(sprite_url, use_column_width = True)
col2.table(pd.DataFrame({'Attributes': ['Height', 'Weight', 'Moves','Types'],
   'Value': [height, weight, moves, types]}).set_index('Attributes'))
graph = sns.barplot(data=height_data,
                    x='Pokemon',
                    y='Heights',
                    palette=colours)

st.write(f'Name: {name.title()}')

if cry_url:
    cry_audio = requests.get(cry_url)
    st.audio(cry_audio.content, format = 'audio/mp3, start_time=0')
else:
    st.write('No battle cry audio available')
st.pyplot(graph.figure)
