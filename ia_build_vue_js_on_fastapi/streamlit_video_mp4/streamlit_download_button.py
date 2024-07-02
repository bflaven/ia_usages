"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate


# BURN AFTER READING
source activate fmm_fastapi_poc



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n llm_integration_api_costs

# BURN AFTER READING
conda env remove -n mistral_integration


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install openai
pip install mistralai
pip install langchain-mistralai
pip install beautifulsoup4

python -m pip install beautifulsoup4
python -m pip install openai

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/build_vue_js_on_fastapi/streamlit_video_mp4/

# launch the file
streamlit run streamlit_download_button.py

https://gist.github.com/chad-m/6be98ed6cf1c4f17d09b7f6e5ca2978f#file-streamlit_download_button-py

"""
import base64
import os
import json
import pickle
import uuid
import re

import streamlit as st
import pandas as pd


def download_button(object_to_download, download_filename, button_text, pickle_it=False):
    """
    Generates a link to download the given object_to_download.

    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.

    Returns:
    -------
    (str): the anchor tag to download object_to_download

    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')

    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;

            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link


def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


if __name__ == '__main__':
    st.markdown("""
                ## How to download files in Streamlit with download_button()

                ~> Below are use cases and code examples for the `download_button()`
                function, which returns a clickable download link given your data
                file as input.

                See the `Show code example` at the bottom of each section for a
                code snippet you can copy & paste.
                [Recommend improvements here](https://discuss.streamlit.io/)

                The download_button() function is an extension of a workaround based on
                the discussions covered in more detail at [Awesome Streamlit](http://awesome-streamlit.org/).
                Go to Gallery -> Select the App Dropdown -> Choose "File Download Workaround"
                for more information.""")

    st.markdown('-'*17)


    # ---------------------
    # Download from memory
    # ---------------------
    if st.checkbox('Download object from memory'):
        st.write('~> Use if you want to save some data from memory (e.g. pd.DataFrame, dict, list, str, int)')

        # Enter text for testing
        s = st.selectbox('Select dtype', ['list',  # TODO: Add more
                                          'str',
                                          'int',
                                          'float',
                                          'dict',
                                          'bool',
                                          'pd.DataFrame'])
        
        filename = st.text_input('Enter output filename and ext (e.g. my-dataframe.csv, my-file.json, my-list.txt)', 'my-file.json')

        # Pickle Rick
        pickle_it = st.checkbox('Save as pickle file')

        sample_df = pd.DataFrame({'x': list(range(10)), 'y': list(range(10))})
        sample_dtypes = {'list': [1,'a', [2, 'c'], {'b': 2}],
                         'str': 'Hello Streamlit!',
                         'int': 17,
                         'float': 17.0,
                         'dict': {1: 'a', 'x': [2, 'c'], 2: {'b': 2}},
                         'bool': True,
                         'pd.DataFrame': sample_df}

        # Display sample data
        st.write(f'#### Sample `{s}` to be saved to `{filename}`')
        st.code(sample_dtypes[s], language='python')

        # Download sample
        download_button_str = download_button(sample_dtypes[s], filename, f'Click here to download {filename}', pickle_it=pickle_it)
        st.markdown(download_button_str, unsafe_allow_html=True)

        if st.checkbox('Show code example '):
            code_text = f"""
                        s = {sample_dtypes[s]}

                        download_button_str = download_button(s, '{filename}', 'Click here to download {filename}', pickle_it={pickle_it})
                        st.markdown(download_button_str, unsafe_allow_html=True)"""

            st.code(code_text, language='python')

    # --------------------------
    # Select a file to download
    # --------------------------
    if st.checkbox('Select a file to download'):
        st.write('~> Use if you want to test uploading / downloading a certain file.')

        # Upload file for testing
        folder_path = st.text_input('Enter directory: deafult .', '.')
        filename = file_selector(folder_path=folder_path)

        # Load selected file
        with open(filename, 'rb') as f:
            s = f.read()

        download_button_str = download_button(s, filename, f'Click here to download {filename}')
        st.markdown(download_button_str, unsafe_allow_html=True)

        if st.checkbox('Show code example'):
            code_text = f"""
                        with open('{filename}', 'rb') as f:
                            s = f.read()

                        download_button_str = download_button(s, '{filename}', 'Click here to download {filename}')
                        st.markdown(download_button_str, unsafe_allow_html=True)"""

            st.code(code_text, language='python')