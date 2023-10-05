#!/usr/bin/python
# -*- coding: utf-8 -*-
# 

"""
[env]
# Conda Environment
conda create --name tagging_entity_extraction python=3.9.13
conda info --envs
source activate tagging_entity_extraction
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n chainlit_python
conda env remove -n ai_chatgpt_prompts

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > tagging_entity_extraction.txt



# to install
pip install -r tagging_entity_extraction.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/tagging_entity_extraction/


python 04_kw_extractor_spacy_linguistic_features.py


"""

import spacy
from collections import Counter
from string import punctuation


# download best-matching version of specific model for your spaCy installation
# python -m spacy download en_core_web_sm


# nlp = spacy.load("en_core_web_sm")
# doc = nlp("This is a sentence.")
# print(doc)

# download best-matching version of specific model for your spaCy installation
# python -m spacy download en_core_web_lg
nlp = spacy.load("en_core_web_lg")
# nlp = spacy.load("en_core_web_sm")



# import en_core_web_lg
# nlp = en_core_web_lg.load()


def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
    doc = nlp(text.lower()) # 2
    for token in doc:
        # 3
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        # 4
        if(token.pos_ in pos_tag):
            result.append(token.text)
                
    return result # 5

# output = get_hotwords('Welcome to Medium! Medium is a publishing platform where people can read important, insightful stories on the topics that matter most to them and share ideas with the world.')


output = get_hotwords('What does the future hold for Wagner in Africa after the failed rebellion?\nRussian Foreign Minister Sergei Lavrov on Monday said that Wagner group troops would continue to operate in Mali and the Central African Republic following the rebellion led by their commander Yevgeny Prigozhin last weekend. Lavrov’s words came amid questions over the private militia’s role in Africa after more than five years of deployment to the continent.\nMembers of the Close Protection Unit for Central African Republic President Touadera, composed of Russian private security company operatives from Sewa Security, are seen in Berengo on August 4, 2018.\nMembers of the Close Protection Unit for Central African Republic President Touadera, composed of Russian private security company operatives from Sewa Security, are seen in Berengo on August 4, 2018. © Florent Vergnes, AFP\n\nText by: \nGrégoire SAUVAGE\nThe Wagner group’s mutiny against Moscow last weekend has raised questions over the private militia’s presence in Africa.\nFor more than five years, thousands of Wagner group troops have deployed to Africa. In 2018 they were sent to support Central African Republic President Faustin-Archange Touadera as he grappled with an armed rebellion. In December 2021 they deployed to Mali in the wake of a coup and they have operated in Sudan since the end of 2017. Wagner troops have also been spotted in Libya and Mozambique.\nBut Lavrov vowed on Monday that the “events” of the last weekend would not impact the militia’s operations on the continent.\nThe Russian "instructors" and “private military contractors” in both Mali and the Central African Republic will continue their work, Lavrov said in an interview with Russia Today.\nPrigozhin’s rebellion will not change anything in Russia\'s ties with its allies, Lavrov added. "There have been many calls (from foreign partners) to President (Vladimir) Putin ... to express their support," he said.\nNo African government has officially commented on the events of the past weekend. But according to Cyril Payen, senior reporter for FRANCE 24, Russia "has undoubtedly become a slightly less reliable partner" since Prigozhin’s rebellion.\n"You can bet that people in Bangui and Bamako are wondering what the future holds," Payen added.\n“The Malian state is now engaged in a double partnership, with the Russian state – the Putin camp – and with the Wagner group – the Prigozhin camp. Until now, this did not make much difference, but that could change if the two camps don’t reconcile in the long term, " said lawyer and political scientist Oumar Berté in an interview with FRANCE 24’s sister radio station Radio France Internationale.\nOverlapping interests\nHowever, a senior official in the Central African Republic’s presidency told AFP that Russia will continue to operate in the central African country, with or without Wagner.\n\n"The Central African Republic signed ( in 2018, editor\'s note) a defence agreement with the Russian Federation, not with Wagner, " said Fidele Gouandjika, special adviser to President Touadera.\n"Russia has subcontracted with Wagner. If Russia no longer agrees with Wagner, then it will send us a new contingent."\nA bridgehead for Russian ambitions on the continent, the Central African Republic is particularly dependent on the Russian militia, whose men even work as private protection officers for Touadera.\nSome 1, 500 Wagner troops have been deployed to Mali since 2021. The paramilitary group has developed close ties with the junta in power, helping to train soldiers as well as taking part in operations to combat terrorist groups.\nPrigozhin’s men have also been seen in Libya, Sudan and Mozambique. Since the Wagner\'s group arrival in Africa, the UN, international NGOs and French authorities have regularly accused the paramilitary group of committing abuse and crimes against civilians.\n >> Read more: France says mercenaries from Russia\'s Wagner Group staged \'French atrocity\' in Mali\nWagner always uses the same strategy every time it advances: disinformation campaigns (based on rejecting former colonial powers) and an offer of security in exchange for the exploitation of natural resources to supply Prigozhin’s war chest and serve the Kremlin’s interests.\nIn Sudan, the partnership between Wagner and the Rapid Support Forces (RSF), led by the junta’s number two, General Mohammed Hamdan Daglo, has enabled the paramilitary group to profit from illegal gold trafficking. It has also enabled them to organise the transport of the metal straight into the coffers of the Russian state, helping to swell its gold reserves and circumvent Western sanctions.\n"Wagner is an entity that defends both private and even criminal interests, and it promotes the Russian state’s agenda. The two are inextricably linked, " said Niagalé Bagayoko, president of the African Security Sector Network during an interview with FRANCE 24.\n‘A creature of the Kremlin’\n"The tensions with the Kremlin arose on the Ukrainian front, not in Africa where, in contrast, Wagner’s interests and those of the Russian government are aligned, " said Africa specialist Thierry Vircoulon, researcher at the French Institute of International Relations (Ifri). "The paramilitary group is a strategic asset for Russia, and it would be ill-advised to interrupt its activities when it has been the main tool of its diplomacy.”\nIf Wagner’s withdrawal from Africa does not look like an option today, a restructuring of its activities seems inevitable. According to Vircoulon, there are several plausible scenarios, including splitting up the group\'s operations. "If Prigozhin remains in the picture, one could see the group dealing solely with external operations and that it would be evacuated from the home front, that is to say from the Ukrainian conflict.”\n>> Read more: No longer untouchable? Putin undermined by Prigozhin\'s march on Moscow\nAnother possibility is that Wagner could be taken over by the Russian Defence Ministry, which recently announced its intention to have all private militias sign a contract. Doing so would be a way of regaining control over the militia’s African activities.\nWestern governments are watching recent events in Russia and their geopolitical implications with caution. "These events raise many questions and we must remain cautious. There are many grey zones, but they show cracks, fractures and flaws within the Russian system," said French Foreign Minister Catherine Colonna.\nPrigozhin broke his silence Monday in an audio message, insisting he never intended to overthrow the government. He did not reveal where he was speaking from, although on Tuesday his arrival in Belarus was confirmed by President Lukashenko.\nA criminal investigation into Prigozhin for “calling for an armed mutiny” is still under way, according to Russian news agencies.')


print ("\n --- output")
print(output)

print ("\n --- result for hashtags")
hashtags = [('#' + x[0]) for x in Counter(output).most_common(5)]
print(' '.join(hashtags))