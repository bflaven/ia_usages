# 02_using_label_studio

**A	 simple example of using with step by step to use Label Studio and Spacy to build a NER.**

*It requires Docker and anaconda to manage the python environment*

For the text, there are 2 texts one in Portuguese the other in English.

- In Portuguese, use case is inspired by this article, especially for the data but the text to annoted is in Portuguese. https://medium.com/@johnidouglasmarangon/train-a-custom-named-entity-recognition-with-spacy-v3-ea48dfce67a5. The code is available at https://gist.github.com/johnidm/27e3b2ff50e592bc37183907ba97d31d

- Still in Portuguese, you can find the excellent Jupyter Notebook
https://gist.github.com/johnidm/27e3b2ff50e592bc37183907ba97d31d


- In English, I try with a text about African football extracted randomly from this article. https://www.bbc.com/sport/football/47415221


**A. In a first console:**


- 1. Create a directory
```
cd /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio

#If needed...
mkdir spacy_ml_with_label_studio
cd spacy_ml_with_label_studio
```


- 2. Installing Label Studio
```
# Run latest Docker version
docker run -it -p 8080:8080 -v `pwd`/mydata:/label-studio/ml-data heartexlabs/label-studio:latest
```

- 3. Go to Label Studio in a browser
```
# Go to http://localhost:8080 or http://0.0.0.0:8080/
# Create a user admin added label-studio
# user :: test1@example.com
# pwd :: test1test1*234
# URL :: http://localhost:8080/user/signup
```

- 4. Creating your Project
```
# 4.1 Project Name
# Title :: NER SPACY #1
# Description :: My first labeling project
```

- 4.2 Data Import
```
# Import /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/02_using_label_studio/ner_source_text_csv/source_pt_johnidm_3.txt
```

- 4.3 Labeling Setup
```
# Select Natural Language Processing > Named Entity Recognition
# Use source_pt_johnidm_labeling_preannotated_ner_tasks_1.xml
```


**B. In a second console: play with Spacy**



- 5. Convert exported JSON from label-studio into spacy format.
```
# Working with Spacy (required the anaconda env)
cd /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/02_using_label_studio


# create the Conda Environment
conda create --name ml_with_label_studio python=3.9.13
conda info --envs
source activate ml_with_label_studio


# Install the requirements
pip install -r requirements_using_label_studio.txt

# convert the label-studio file into spacy format
# You can use "01_convert_label_studio_json_to_spacy.py" with 
# "project-2-at-2023-08-25-14-12-3cbb7a88.json", it will generate the file named # "spacy_output_format.json"

```


- 6. Convert exported JSON named spacy_output_format.json into .spacy with 02_convert_spacy_training.py

```
# You should see dev.spacy and train.spacy inside the directory /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/02_using_label_studio/spacy_output/
```

- 7. Working with Spacy (required the anaconda env)
```
# With the help of Spacy, you can create a config file on the website https://spacy.io/usage/training/ let's call it def_base_config_en.cfg for English text (Select NER and language EN) or def_base_config_pt for Portuguese (Select NER and language PT)
```

- 8. Create spacy config for your NER meaning init config for PT or EN
```
# Command to init the config for the NER in EN with config (generated a config file) with arguments
python -m spacy init config spacy_split_output/def_base_config_en.cfg --lang en --pipeline ner --optimize efficiency --force

# Command to init the config for the NER in PT with config (generated a config file) with arguments
python -m spacy init config spacy_split_output/def_base_config_pt.cfg --lang pt --pipeline ner --optimize efficiency --force

# Command to init the config with "fill-config" (generated a config file from a model)
python -m spacy init fill-config spacy_conf_file/sample_base_config_en.cfg spacy_split_output/def_base_config_en_good.cfg --diff
```

- 9. Train the NER
```
# Command to train
python -m spacy train ./spacy_split_output/def_base_config_en_good.cfg --output ./spacy_model_output --paths.train ./spacy_split_output/train.spacy --paths.dev ./spacy_split_output/dev.spacy

```











