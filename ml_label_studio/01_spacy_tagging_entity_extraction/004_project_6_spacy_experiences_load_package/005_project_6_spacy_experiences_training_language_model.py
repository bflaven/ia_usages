#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
# NO CONDA ENV

conda create --name tagging_entity_extraction python=3.9.13
conda info --envs
source activate tagging_entity_extraction

conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]




# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > tagging_entity_extraction.txt



# to install
pip install -r tagging_entity_extraction.txt

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/tagging_entity_extraction/project_6_spacy_experiences/

[file]
python 005_project_6_spacy_experiences..py

python -m spacy download es_core_news_md
python -m spacy download en_core_news_md

More corpus
https://spacy.io/models/es#es_core_news_sm



Source: https://medium.com/mlearning-ai/automatic-skill-extraction-from-resumes-using-spacy-710507624a1e

"""
import spacy
from string import punctuation
from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

# lang = "en"
# query_string ='What does the future hold for Wagner in Africa after the failed rebellion? Russian Foreign Minister Sergei Lavrov on Monday said that Wagner group troops would continue to operate in Mali and the Central African Republic following the rebellion led by their commander Yevgeny Prigozhin last weekend. Lavrov’s words came amid questions over the private militia\'s role in Africa after more than five years of deployment to the continent. Members of the Close Protection Unit for Central African Republic President Touadera, composed of Russian private security company operatives from Sewa Security, are seen in Berengo on August 4, 2018. Members of the Close Protection Unit for Central African Republic President Touadera, composed of Russian private security company operatives from Sewa Security, are seen in Berengo on August 4, 2018. © Florent Vergnes, AFP. The Wagner group’s mutiny against Moscow last weekend has raised questions over the private militia’s presence in Africa. For more than five years, thousands of Wagner group troops have deployed to Africa. In 2018 they were sent to support Central African Republic President Faustin-Archange Touadera as he grappled with an armed rebellion. In December 2021 they deployed to Mali in the wake of a coup and they have operated in Sudan since the end of 2017. Wagner troops have also been spotted in Libya and Mozambique. But Lavrov vowed on Monday that the “events” of the last weekend would not impact the militia’s operations on the continent. The Russian "instructors" and “private military contractors” in both Mali and the Central African Republic will continue their work, Lavrov said in an interview with Russia Today.Prigozhin\'s rebellion will not change anything in Russia\'s ties with its allies, Lavrov added. "There have been many calls (from foreign partners) to President (Vladimir) Putin ... to express their support," he said. No African government has officially commented on the events of the past weekend. But according to Cyril Payen, senior reporter for FRANCE 24, Russia "has undoubtedly become a slightly less reliable partner" since Prigozhin’s rebellion. The Malian state is now engaged in a double partnership, with the Russian state – the Putin camp – and with the Wagner group – the Prigozhin camp. Until now, this did not make much difference, but that could change if the two camps don’t reconcile in the long term, " said lawyer and political scientist Oumar Berté in an interview with FRANCE 24’s sister radio station Radio France Internationale.'

# Extracting terms from a sentence in English
en_sentence = (
    "The giant panda, also known as the panda bear (or simply the panda)"
    " is a bear native to South Central China. It is characterised by its"
    " bold black-and-white coat and rotund body. The name 'giant panda'"
    " is sometimes used to distinguish it from the red panda, a neighboring"
    " musteloid. Though it belongs to the order Carnivora, the giant panda"
    " is a folivore, with bamboo shoots and leaves making up more than 99%"
    " of its diet. Giant pandas in the wild will occasionally eat other grasses,"
    " wild tubers, or even meat in the form of birds, rodents, or carrion."
    " In captivity, they may receive honey, eggs, fish, shrub leaves,"
    " oranges, or bananas.\n"
)


es_sentence = (
    "El panda gigante, también conocido como oso panda (o simplemente panda),"
    " es un oso originario del centro-sur de China. Se caracteriza por su"
    " llamativo pelaje blanco y negro, y su cuerpo rotundo. El nombre 'panda"
    " gigante' se usa en ocasiones para distinguirlo del panda rojo, un"
    " mustélido parecido. Aunque pertenece al orden de los carnívoros, el panda"
    " gigante es folívoro, y más del 99 % de su dieta consiste en brotes y"
    " hojas de bambú. En la naturaleza, los pandas gigantes comen ocasionalmente"
    " otras hierbas, tubérculos silvestres o incluso carne de aves, roedores o"
    " carroña. En cautividad, pueden alimentarse de miel, huevos, pescado, hojas"
    " de arbustos, naranjas o plátanos.\n"
)

# def get_keywords():
#     if (lang == "en"):
#         lang_pack = "en_core_web_sm"
#     elif (lang == "es"):
#         lang_pack = "es_core_news_sm"
#     elif (lang == "de"):
#         lang_pack = "de_core_news_sm"
#     else:
#         lang_pack = "en_core_web_sm"
def extract_keywords(nlp, sequence):
    """ Takes a Spacy core language model,
    string sequence of text and optional
    list of special tags as arguments.
    
    If any of the words in the string are 
    in the list of special tags they are immediately 
    added to the result.  
    
    Arguments:
        sequence {str} -- string sequence to have keywords extracted from
    
    Keyword Arguments:
        tags {list} --  list of tags to be automatically added (default: {None})
    
    Returns:
        {list} -- list of the unique keywords extracted from a string
    """
    result = []

    # custom list of part of speech tags we are interested in
    # we are interested in proper nouns, nouns, and adjectives
    # edit this list of POS tags according to your needs.
    pos_tag = ['PROPN', 'NOUN']

    # create a spacy doc object by calling the nlp object on the input sequence
    doc = nlp(sequence.lower())

    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if (token.pos_ in pos_tag):
                final_chunk = final_chunk + token.text + " "
        if final_chunk:
            result.append(final_chunk.strip())

    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return list(set(result))
    

# nlp_pack = spacy.load(lang_pack)
# nlp_pack = spacy.load("en_core_web_md")
# keywords = extract_keywords(nlp_pack, en_sentence)

nlp_pack = spacy.load("es_core_news_md")
keywords = extract_keywords(nlp_pack, es_sentence)

print('\n --- RESULT')
print(keywords)
