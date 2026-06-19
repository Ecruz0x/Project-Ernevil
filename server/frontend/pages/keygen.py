import streamlit as st
import string
import random
import requests


st.set_page_config(
    page_title="Generate Key",
)

if "generated_key" not in st.session_state:
    st.session_state.generated_key = None

def add_key(key, length):
    r = requests.post("http://127.0.0.1:8000/api/computers/keys", json = {"key": key, "length": length})
    return r.status_code


def generate_key(length, include_lowercase, inlcude_uppercase, include_digits, include_punctuation):
    key = ''
    random_set = ''

    if include_lowercase:
        random_set += string.ascii_lowercase
        key += random.choice(string.ascii_lowercase)
    
    if inlcude_uppercase:
        random_set += string.ascii_uppercase
        key += random.choice(string.ascii_uppercase)

    if include_digits:
        random_set += string.digits
        key += random.choice(string.digits)

    if include_punctuation:
        random_set += string.punctuation
        key += random.choice(string.punctuation)

    for i in range(length-3):
        key+=random.choice(random_set)

    keylist = list(key)
    random.SystemRandom().shuffle(keylist)
    key = ''.join(keylist)
    return key
    

@st.dialog("Are you sure you want to save this key?")
def confirm_action(key):
    st.code(key)
    st.write("This action cannot be undone.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, Save", key="save"):
            status_code = add_key(key, len(key))
            print("saving...", key)
            st.rerun()

    with col2:
        if st.button("Cancel", key="cancel"):
            st.rerun()

st.header("Key Generator")

length = st.slider('Key Length', min_value=8, max_value=32, value=8, step=1)
include_lowercase = st.checkbox('Include Lowercase Letters', value=True)
include_uppercase = st.checkbox('Include Uppercase Letters', value=True)
include_digits = st.checkbox('Include Digits', value=True)
include_punctuation = st.checkbox('Inclued Punctuation', value=False)

if st.button('Generate Key', key="generate"):
    st.session_state.generated_key = generate_key(
        length,
        include_lowercase,
        include_uppercase,
        include_digits,
        include_punctuation
    )
    st.code(st.session_state.generated_key)

if st.session_state.generated_key:
    if st.button('Save Key'):
        confirm_action(st.session_state.generated_key)



hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)