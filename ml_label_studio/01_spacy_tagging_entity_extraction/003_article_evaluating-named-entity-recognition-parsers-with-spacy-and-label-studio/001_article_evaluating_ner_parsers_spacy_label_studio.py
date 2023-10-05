#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
cd /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/01_spacy_tagging_entity_extraction/003_annotate_tool_demo_label_studio_doccano/001_article_evaluating-named-entity-recognition-parsers-with-spacy-and-label-studio/

python 001_article_evaluating_ner_parsers_spacy_label_studio.py


"""
import io
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
# nlp = spacy.load("en_core_web_lg")
nlp = spacy.load("en_core_web_sm")


# import en_core_web_lg
# nlp = en_core_web_lg.load()


def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN']  # 1
    doc = nlp(text.lower())  # 2
    for token in doc:
        # 3
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        # 4
        if (token.pos_ in pos_tag):
            result.append(token.text)

    return result  # 5

"""
input_text = "After facial recognition, I am tackling language issues with Python. Indeed, after image, the other ingredient for a post is mostly text! As a CMS \"manufacturer\" or PO, I was wondering what advantages I can withdraw from NLP. Concretely, it means exploring and learning Python to improve both user support (FAQs turn as a Chatbot, analyzing User Feedback...) but also think about some editorial features especially with the help of Natural Language Processing (NLP). I am wrestling with the subject for too long because there are tons of libraries and tutorials introducing to Python and NLP! Looking for python is an heavy trend. Apparently, Google users in America have searched for Python more often than for Kim Kardashian. So, \"creating a chatbot in Python\" has become the typical quoted example like \"creating a blog\" or \"hello world\" in other language! Like I said at the beginning of this post. The starting idea was simple, how can I aleviate real-world tasks such as:\
Improve the user feedback loop (monitoring user feedback or converting static FAQs to a modest User Support Conversational Agent).\
Text understanding to enable meaningfull keywords extraction or text summary for instance.\
I found some very contrived examples and some more advanced ones like always. Even though, these examples are oversimplified, there are still caveats for less technical readers, including me, especially when it comes to concepts pertaining to linguistic eg stemming, tokenization, tokenizer, bag of words or Convolutional Neural Network. I invite to check these very intuitive videos that are good introduction to NLP. These videos are giving some enlightening on NLP's concepts such as stemming, tokenization, tokenizer or bag of words or even some explanations on different type of IA’s network such as Convolutional Neural Network and the way to use it.\
Here is a posts'digest to start with NLP oriented around 2 basic usages, that can ba implemented in a CMS: Practical Use Cases in a CMS's support and simple techniques to extract Keywords or even \"slice\" a post. Chronologically, the very first library, I explored was the famous NLPs librairie, NTLK. Then I discovered Pytorch, made by Facebook and then Spacy. There will be certainly a more specific article on Spacy because I really like Spacy for its accessibility both in tutorials and in its core values. After all this reading, I selected few articles that were illustrating, at least, some of my personal interests for NLP. The source code is avalaible on my github account and I am using my own mac plus anaconda to deal and install all the require librairies.\
1. Keyword Extraction\
A beginner's guide to keyword extraction with natural language processing (article_1_keyword_extraction_nlp)\
A good usecase for support where you parse a unique user feedback file and retrieve core informations with NLP. This usecase leverage on a bunch of librairies such as Panda, Scipy, Seaborn, scikit-learn and for sure NLTK. It parses a huge document in .tsv format (Tab-separated values).\
NLP keyword extraction tutorial with RAKE and Maui (article_2_keyword_extraction_rake_rake)\
For me, only first part was interesting, it shows how to use RAKE which stands for Rapid Automatic Keyword Extraction. RAKE extracts keywords that should describe the main topics expressed in a document.\
Extract Keywords Using spaCy in Python (article_3_keyword_extraction_nlp_spacy)\
This article from Ng Wai Foong and some other examples from the great official spaCy documentation show how to quickly get to grip with Spacy. The script extracting keywords with Spacy is straightforward like the other article from this guy Ng Wai Foong.\
Miscellaneous examples with spaCy (article_4_miscellaneous_examples_nlp_spacy)\
Some miscellaneous linguistic scripts using spaCy. There is much more on their github account and the documantion is terrific. https://github.com/explosion/spaCy\
Scraping Post\
Newspaper: Article scraping & curation (article_5_playing_with_newspaper_post_scraping_curation)\
It is just playing with the librairie newspaper that will slice post. I am using my own post Playing with newspaper https://newspaper.readthedocs.io/en/latest/ check the import of newspaper\
\
ChatBot With PyTorch - NLP And Deep Learning (article_6_chatbot_with_pytorch)\
We left the Keyword Extraction for ChatBot. Turning my FAQ to a ChatBot with the help of Pytorch and NLTK. It is a very intuitive tutorial and the videos are making the rest. Certainly, I was not rapt in ecstasy by the chatbot ability but there is a lot of promises for Chatbots, supposed to be handling fairly complex conversation with humans and so using a lot of Natural Language Processing techniques in order to understand the human's requests.\
Build Your First Chatbot in Python (article_7_chatbot_with_tensorflow)\
A different ChatBot Build on TensorFlow from a .txt file.\
Chatbot tutorial by Matthew Inkawhich (article_8_chatbot_tutorial_pytorch)\
I found a more advanced Chatbot tutorial with Pytorch due to a lack of space on my hard drive! I was forced to downsize the training so the chatbot sucks... Anyway the example is great. Check https://pytorch.org/tutorials/beginner/chatbot_tutorial.html\
Text Summarization Using spaCy in Python (article_9_text_summarization_using_spacy)\
A second article from Ng Wai Foong. It is about Text Summarization with TF-IDF (Term Frequency-Inverse Data Frequency). It leverages on Spacy and the result is immediate\
Some critics about IA\
Let's step back a little bit to think a minute about IA consequences. These IA tools exerts an undeniable fascination. Why? These are new tools that actually begin to think and act on its own. The idea that these tools will make decisions and undertake actions on their own is fascinating and scary at the same. I was wondering if any critical thinking existed towards the deafening consensus on AI? I found some opponents, on a philosophical point of view. Even though, IA fanatics report that the AI promise is to \"Humanize the machine, not mechanize the User\". The main critic is the AI's \"injunctive power\". Combined with consent, it makes an unstoppable combination to turn us mankind into passive and obedient sheeps! But the GAFAS, that promote IA, never really assumed they were the bad guy. Indeed, IA can been seen as the ultimate market achievement where, reduced as consumers, we only take decisions with utilitarian goals, \"obeying\" to IA. Regarding NLP, the disturbing thing is the familiar form that this injunction takes. The Chatbot speaks to you, the NLP writes and advises you with own words... This is step forward soft power. So, is the very idea of rebelling still even exist as it sounds ludicrous, to fight with a friend! What I mostly remember from this reading: - IA is a threat to humanity, especially our free will. - IA is the ultimate version of \"Invisible hand\", so criticizing IA seems to be the way to \"burn down\" the system aka capitalism, GAFAS (Facebook, Google, Amazon... etc. that are mostly behind the IA libraries and expect something on return. Anyway, that's always good to read opinions against the mainstream way of thinking!\
What's next? How can I use NLP?\
I wonder more and more if the target has not become to even drop PHP to build a web application or refactor the PHP legacy Code in Python! Indeed, building a web application, I do not even talk about a website seems to be easy nowadays. You can gather an effective SPA (Single Page Application) in a very short time but providing meaningful and advanced features for a CMS is trickier! To be totally transparent, a simple question is spinning around in my head: How can I add some \"intelligent\" functionalities, using these Python libraries, to an existing CMS made in PHP? Apparently, the way seems to build a separate API in Python that will brigde with PHP! Like I said in my previous post, these NLP libraries are not only enabling new tasks to be made but these libraries can even carry out tasks like a real human such as me a P.O for a Backoffice! Great, I am outsourcing myself.\
Using Anaconda\
\
A reminder for useful commands."
"""

input_text = 'What does the future hold for Wagner in Africa after the failed rebellion?\nRussian Foreign Minister Sergei Lavrov on Monday said that Wagner group troops would continue to operate in Mali and the Central African Republic following the rebellion led by their commander Yevgeny Prigozhin last weekend. Lavrov’s words came amid questions over the private militia’s role in Africa after more than five years of deployment to the continent.\nMembers of the Close Protection Unit for Central African Republic President Touadera, composed of Russian private security company operatives from Sewa Security, are seen in Berengo on August 4, 2018.\nMembers of the Close Protection Unit for Central African Republic President Touadera, composed of Russian private security company operatives from Sewa Security, are seen in Berengo on August 4, 2018. © Florent Vergnes, AFP\n\nText by: \nGrégoire SAUVAGE\nThe Wagner group’s mutiny against Moscow last weekend has raised questions over the private militia’s presence in Africa.\nFor more than five years, thousands of Wagner group troops have deployed to Africa. In 2018 they were sent to support Central African Republic President Faustin-Archange Touadera as he grappled with an armed rebellion. In December 2021 they deployed to Mali in the wake of a coup and they have operated in Sudan since the end of 2017. Wagner troops have also been spotted in Libya and Mozambique.\nBut Lavrov vowed on Monday that the “events” of the last weekend would not impact the militia’s operations on the continent.\nThe Russian "instructors" and “private military contractors” in both Mali and the Central African Republic will continue their work, Lavrov said in an interview with Russia Today.\nPrigozhin’s rebellion will not change anything in Russia\'s ties with its allies, Lavrov added. "There have been many calls (from foreign partners) to President (Vladimir) Putin ... to express their support," he said.\nNo African government has officially commented on the events of the past weekend. But according to Cyril Payen, senior reporter for FRANCE 24, Russia "has undoubtedly become a slightly less reliable partner" since Prigozhin’s rebellion.\n"You can bet that people in Bangui and Bamako are wondering what the future holds," Payen added.\n“The Malian state is now engaged in a double partnership, with the Russian state – the Putin camp – and with the Wagner group – the Prigozhin camp. Until now, this did not make much difference, but that could change if the two camps don’t reconcile in the long term, " said lawyer and political scientist Oumar Berté in an interview with FRANCE 24’s sister radio station Radio France Internationale.\nOverlapping interests\nHowever, a senior official in the Central African Republic’s presidency told AFP that Russia will continue to operate in the central African country, with or without Wagner.\n\n"The Central African Republic signed ( in 2018, editor\'s note) a defence agreement with the Russian Federation, not with Wagner, " said Fidele Gouandjika, special adviser to President Touadera.\n"Russia has subcontracted with Wagner. If Russia no longer agrees with Wagner, then it will send us a new contingent."\nA bridgehead for Russian ambitions on the continent, the Central African Republic is particularly dependent on the Russian militia, whose men even work as private protection officers for Touadera.\nSome 1, 500 Wagner troops have been deployed to Mali since 2021. The paramilitary group has developed close ties with the junta in power, helping to train soldiers as well as taking part in operations to combat terrorist groups.\nPrigozhin’s men have also been seen in Libya, Sudan and Mozambique. Since the Wagner\'s group arrival in Africa, the UN, international NGOs and French authorities have regularly accused the paramilitary group of committing abuse and crimes against civilians.\n >> Read more: France says mercenaries from Russia\'s Wagner Group staged \'French atrocity\' in Mali\nWagner always uses the same strategy every time it advances: disinformation campaigns (based on rejecting former colonial powers) and an offer of security in exchange for the exploitation of natural resources to supply Prigozhin’s war chest and serve the Kremlin’s interests.\nIn Sudan, the partnership between Wagner and the Rapid Support Forces (RSF), led by the junta’s number two, General Mohammed Hamdan Daglo, has enabled the paramilitary group to profit from illegal gold trafficking. It has also enabled them to organise the transport of the metal straight into the coffers of the Russian state, helping to swell its gold reserves and circumvent Western sanctions.\n"Wagner is an entity that defends both private and even criminal interests, and it promotes the Russian state’s agenda. The two are inextricably linked, " said Niagalé Bagayoko, president of the African Security Sector Network during an interview with FRANCE 24.\n‘A creature of the Kremlin’\n"The tensions with the Kremlin arose on the Ukrainian front, not in Africa where, in contrast, Wagner’s interests and those of the Russian government are aligned, " said Africa specialist Thierry Vircoulon, researcher at the French Institute of International Relations (Ifri). "The paramilitary group is a strategic asset for Russia, and it would be ill-advised to interrupt its activities when it has been the main tool of its diplomacy.”\nIf Wagner’s withdrawal from Africa does not look like an option today, a restructuring of its activities seems inevitable. According to Vircoulon, there are several plausible scenarios, including splitting up the group\'s operations. "If Prigozhin remains in the picture, one could see the group dealing solely with external operations and that it would be evacuated from the home front, that is to say from the Ukrainian conflict.”\n>> Read more: No longer untouchable? Putin undermined by Prigozhin\'s march on Moscow\nAnother possibility is that Wagner could be taken over by the Russian Defence Ministry, which recently announced its intention to have all private militias sign a contract. Doing so would be a way of regaining control over the militia’s African activities.\nWestern governments are watching recent events in Russia and their geopolitical implications with caution. "These events raise many questions and we must remain cautious. There are many grey zones, but they show cracks, fractures and flaws within the Russian system," said French Foreign Minister Catherine Colonna.\nPrigozhin broke his silence Monday in an audio message, insisting he never intended to overthrow the government. He did not reveal where he was speaking from, although on Tuesday his arrival in Belarus was confirmed by President Lukashenko.\nA criminal investigation into Prigozhin for “calling for an armed mutiny” is still under way, according to Russian news agencies.'

output = get_hotwords(input_text)

print("\n --- output")
print(output)

print("\n --- result for hashtags")
hashtags = [('#' + x[0]) for x in Counter(output).most_common(5)]
print(' '.join(hashtags))
