"""
[env]
# Conda Environment
conda create --name fmm_fastapi_poc python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n fmm_fastapi_poc


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
To complete

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_prompt_seo/

# launch the file
python usecase_referent_seo_7.py


"""

# for api key
import os
from dotenv import load_dotenv

# Import the OpenAI class from the openai module
from openai import OpenAI

### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
api_key = os.getenv("OPENAI_API_KEY")

# Get the model
model_selected = "gpt-3.5-turbo"
# model_selected = "gpt-4-turbo"



### 2. GET STUFF FROM CHATGPOT ###
# Create an instance of the OpenAI class with the provided API key
client = OpenAI(api_key=api_key)

def openai_chat(user_prompt):

    # Create a chat completion using the OpenAI client
    response = client.chat.completions.create(
        # Set the model to "gpt-3.5-turbo-0125"
        model=model_selected, 
        messages=[{"role": "user", "content": user_prompt}]
    )

    # Response from the chat completion
    answer = response.choices[0].message.content

    # Assuming response and model_selected are defined and have valid values
    if model_selected == "gpt-3.5-turbo":
        input_price = response.usage.prompt_tokens * (0.46 / 1e6)
        output_price = response.usage.completion_tokens * (1.38 / 1e6)
    else:
        if model_selected == "gpt-4-turbo":
            input_price = response.usage.prompt_tokens * (9.18 / 1e6)
            output_price = response.usage.completion_tokens * (27.55 / 1e6)
        else:
            print("Invalid model selected. Please choose between 'gpt-3.5-turbo' and 'gpt-4-turbo'.")

     

    
    # calculate the total price
    total_price = input_price + output_price

    # Return the answer, input price, output price, total price
    # return {
    #     "answer": answer,
    #     "input_price": f"$ {input_price}",
    #     "output_price": f"$ {output_price}",
    #     "total_price": f"$ {total_price}"
    # }

    return {
        "answer": answer,
        "input_price": f"€ {input_price}",
        "output_price": f"€ {output_price}",
        "total_price": f"€ {total_price}"
    }

# FRENCH   
# user_input = """
# <p>Un bus a pris feu et une trentaine de personnes ont été légèrement blessés samedi 25 mai lors d'affrontements entre supporters de l'OL et du <a target="_self" href="https://www.france24.com/fr/tag/psg/" class="gtm-add-suggested-tag">PSG</a> à un péage d'autoroute près d'Arras, juste avant la finale de la <a target="_self" href="https://www.france24.com/fr/tag/coupe-de-france/" class="gtm-add-suggested-tag">Coupe de France</a> à Lille, des faits condamnés "avec la plus grande fermeté" par le président <a target="_self" href="https://www.france24.com/fr/tag/emmanuel-macron/" class="gtm-add-suggested-tag">Emmanuel Macron</a>.</p><p>Selon la préfecture du Pas-de-Calais, cette rixe a opposé des supporters des deux équipes qui se rendaient au stade Pierre-Mauroy de Villeneuve d'Ascq aux environs de 18H00 sur l'Autoroute A1, au niveau du péage de Fresnes-lès-Montauban (Pas-de-Calais), à une soixantaine de kilomètres de Lille.</p><p>"Une centaine d'individus sont impliqués et un bus a pris feu", a-t-elle précisé, ajoutant que "18 bus de supporters parisiens ont repris la route vers Lille". "Les supporters lyonnais ont également été écartés", a-t-elle poursuivi.</p><p>"Ce sont des rendez-vous sportifs où il faut avant tout être dans la joie et le sport. Je condamne avec la plus grande fermeté toutes les violences", a déclaré le chef de l'État lors d'une déambulation publique à Tourcoing. "J'espère que les choses se dérouleront le plus normalement possible ce soir", a-t-il ajouté, confirmant qu'il irait au stade.</p><h2>Aucune interpellation                </h2><p>Selon une source policière, les heurts "ont opposé environ une centaine de supporters lyonnais à près de 200 supporters parisiens" et "la barrière de péage (a été) partiellement incendiée".</p><p>Cette source fait également état de six policiers légèrement blessés, un bilan non confirmé par la préfecture du Pas-de-Calais. Aucune personne n'a été interpellée, selon la source policière.</p><p>D'après une source à la gendarmerie, ces violences font suite à "une rencontre inopportune entre des supporters lyonnais et parisiens".</p><p>"Le dispositif de sécurité important mis en place pour le match et notamment les escortes policières pour encadrer les ultras a permis de mettre fin rapidement, malgré des bus dégradés, aux affrontements", a écrit la préfecture du Nord sur X.</p><p>L'autoroute A1 reste coupée dans les deux sens, selon la préfecture du Pas-de-Calais.</p><p>Au Stade Pierre-Mauroy, la finale de la Coupe Gambardella entre Marseille et Nancy, qui se joue en lever de rideau de celle de la Coupe de France, a été interrompue une dizaine de minutes après le jet d'un projectile par des supporters parisiens, déjà présents dans le stade, en direction du gardien de l'OM.</p><p>Les fans de l'OL et du PSG se sont invectivés pendant cette rencontre, a constaté un journaliste de l'AFP.</p><h2>Alcool interdit</h2><p>Durant la journée, les supporters parisiens, mais surtout lyonnais, ont animé les rues du centre-ville de Lille dans une ambiance bon enfant, a constaté un journaliste de l'AFP. Un impressionnant dispositif policier est déployé dans la ville.</p><p>Selon la préfecture du Pas-de-Calais, 1 000 policiers et gendarmes ont été mobilisés pour sécuriser la rencontre et 1 000 autres pour gérer la sécurité dans le stade.</p><p>Appelant à "la responsabilité collective et individuelle des supporters", la préfecture du Nord avait mis en place plusieurs mesures administratives dans le cadre de cette rencontre classée à très haut risque.</p><p>Les supporters de l'OL et du PSG ont ainsi l'interdiction de se déplacer "en dehors des espaces qui leur sont réservés" et ne peuvent se croiser près de l'enceinte.</p><p>La préfecture avait également demandé aux supporters de chaque équipe d'utiliser chacun une ligne de métro différente, avec des arrêts de métro distincts, pour se rendre au stade et d'éviter au maximum les risques de débordements. </p><p>Autre interdiction : la consommation sur la voie publique et les terrasses de Lezennes, Lille et Villeneuve d'Ascq d'alcool "dans un contenant en verre ou en métal" jusqu'à dimanche 4 H.</p><p><em>Avec Reuters et AFP</em></p>
# """

# SPANISH  
user_input = """
<p>En el Cerrado, una extensa sabana con enorme biodiversidad al sur de la <a href="https://www.france24.com/es/tag/amazonia/" target="_self" class="gtm-add-suggested-tag">Amazonía</a>, <strong>más de 1,11 millones de hectáreas fueron destruidas en 2023, un 68% más que el año precedente</strong>, indicó MapBiomas, un consorcio climático de organizaciones no gubernamentales (ONG), universidades brasileñas y empresas tecnológicas, que monitorea y consolida datos de áreas afectadas.</p><p>Esas pérdidas representaron casi dos tercios de la deforestación que sufrió todo <a href="https://www.france24.com/es/tag/brasil/" target="_self" class="gtm-add-suggested-tag">Brasil</a>, y <strong>unas 2,4 veces la destrucción registrada en la Amazonía,</strong> según el informe.</p><p>La superficie amazónica arrasada el año pasado totalizó 454.300 hectáreas, un descenso de 62,2% contra las cifras de 2022.</p><p>Esta es <strong>la primera vez que la devastación en el Cerrado, que se extiende por 11 estados del centro al noreste de Brasil, supera la de la Amazonía</strong> desde el inicio de los registros de MapBiomas Alerta, en 2019.</p><p class="a-read-more"><span class="a-read-more__label">Leer también</span><a href="https://www.france24.com/es/programas/reporteros/20240422-la-sabana-brasileña-del-cerrado-es-sacrificada-en-nombre-de-la-agricultura-industrial" target="_self" class="a-read-more__link">La sabana brasileña del Cerrado es sacrificada en nombre de la agricultura industrial</a></p><p>"El rostro de la deforestación está cambiando en Brasil, concentrándose en los biomas donde predominan formaciones de sabanas y campestres, y reduciéndose en las formaciones selváticas", describió Tasso Azevedo, coordinador de MapBiomas.</p><p>La causa, sin embargo, fue común a todos los biomas: "Casi toda la deforestación en el país (97%) tuvo la expansión agropecuaria como vector", destacó MapBiomas.</p><p>Además, más del 93% de la destrucción "tuvo al menos un indicio de ilegalidad" o irregularidad, se estimó con los datos también procesados por el Instituto de <a href="https://www.france24.com/es/tag/investigación/" target="_self" class="gtm-add-suggested-tag">Investigación</a> Ambiental de la Amazonía (Ipam).</p><p>Desde un punto de vista más amplio, la<strong> deforestación en Brasil se redujo en 2023 por primera vez en cuatro años</strong>, con una baja de 11,6% respecto del año anterior.</p><p>El informe es una noticia agridulce para el gobierno de <a href="https://www.france24.com/es/tag/luiz-inacio-lula-da-silva/" target="_self" class="gtm-add-suggested-tag">Luiz Inácio Lula da Silva</a>, quien se comprometió a priorizar el cuidado del medioambiente revirtiendo las políticas de su predecesor <a href="https://www.france24.com/es/tag/jair-bolsonaro/" target="_self" class="gtm-add-suggested-tag">Jair Bolsonaro</a> (2019-2022) y a eliminar la deforestación ilegal de la Amazonía en 2030.</p><p>La pérdida de vegetación nativa en el gigante sudamericano continúa siendo una preocupación, especialmente ante las consecuencias cada vez más evidentes, como las devastadoras <a href="https://www.france24.com/es/tag/inundaciones/" target="_self" class="gtm-add-suggested-tag">inundaciones</a> en el estado sureño de Rio Grande do Sul, que dejan al menos 170 muertos y unos 600.000 evacuados.</p>
"""

# ENGLISH
# user_input = """
# <p>In a coordinated move last week, <a href="https://www.france24.com/en/tag/spain/" target="_self" class="gtm-add-suggested-tag">Spain</a>, <a href="https://www.france24.com/en/tag/ireland/" target="_self" class="gtm-add-suggested-tag">Ireland</a> and <a href="https://www.france24.com/en/tag/norway/" target="_self" class="gtm-add-suggested-tag">Norway</a> <a href="https://www.france24.com/en/live-news/20240522-norway-ireland-spain-to-recognise-palestinian-state" target="_self">announced</a> they would formally recognise the state of Palestine. On Tuesday, they fulfilled their promise.</p><p>Described as a “<a href="https://www.france24.com/en/middle-east/20240528-ireland-norway-to-join-spain-in-historic-decision-to-formally-recognise-a-palestinian-state" target="_self">historic decision</a>” by Spanish Prime Minister <a href="https://www.france24.com/en/tag/pedro-sanchez/" target="_self" class="gtm-add-suggested-tag">Pedro Sanchez</a> in a televised address, the three nations hope their initiative will encourage other European countries to do the same.</p><p>But the continent is divided on the issue. Of the 27 member states that make up the <a href="https://www.france24.com/en/tag/european-union/" target="_self" class="gtm-add-suggested-tag">European Union</a>, only 10 have recognised a Palestinian state: Cyprus, Sweden, Hungary, the Czech Republic, Poland, Slovakia, Romania, Bulgaria and now Ireland and Spain.</p><p><a href="https://www.france24.com/en/tag/malta/" target="_self" class="gtm-add-suggested-tag">Malta</a> and <a href="https://www.france24.com/en/tag/slovenia/" target="_self" class="gtm-add-suggested-tag">Slovenia</a> have indicated they will follow suit while <a href="https://www.france24.com/en/tag/france/" target="_self" class="gtm-add-suggested-tag">France</a> and <a href="https://www.france24.com/en/tag/germany/" target="_self" class="gtm-add-suggested-tag">Germany</a> have said now is not the time to do so.</p><p>Sweden was the first Western country to officially recognise the state of Palestine <u><a href="https://www.france24.com/en/20141030-now-right-time-recognize-state-palestine-swedish-fm-wallstrom-tells-f24" target="_self">in October 2014</a></u>, a move its foreign minister at the time, Margot Wallström, said was “an important step that confirms the Palestinians’ rights to self-determination”.</p><p><a href="https://www.france24.com/en/tag/norway/" target="_self" class="gtm-add-suggested-tag">Norway</a>, which is not an EU member state, has played a major role in brokering peace between the Israelis and Palestinians, most notably hosting the secret talks that led to the <a href="https://www.france24.com/en/tag/oslo-accords/" target="_self" class="gtm-add-suggested-tag">Oslo Accords</a> – the widely celebrated 1993 peace agreement between the two parties that <u><a href="https://www.france24.com/en/20130913-oslo-accords-unfulfilled-20-years-palestinian-territories" target="_self">ultimately went unfulfilled</a></u>.</p><p>Now out of the 193 <a href="https://www.france24.com/en/tag/united-nations/" target="_self" class="gtm-add-suggested-tag">UN</a> member states, more than 140 have officially recognised a Palestinian state. Many recognitions date back to 1988, when the Palestinian National Council <u><a href="https://www.france24.com/en/20110919-diplomacy-united-nations-palestinian-un-full-membership-bid-abbas#:~:text=Roughly 100 nations,statehood in 1988." target="_self">unilaterally declared</a></u> its statehood and issued a declaration of independence.</p><p>FRANCE 24 spoke with international criminal investigator Céline Bardet and Johann Soufi, an expert in international law and former head of <a href="https://www.france24.com/en/tag/unrwa/" target="_self">UNRWA</a>’s legal office in Gaza, about the impact recognising the state of Palestine will have.</p><p><strong>Why </strong><strong>does </strong><strong>recognising Palestine as a state matter?  </strong>           </p><p><strong>Céline Bardet: </strong>First of all, it puts Palestine on an equal footing with all the other states. And that is essential, both legally and on the ground.</p><p>Palestine has been a non-member observer state of the United Nations since 2012 and is already recognised by many member states. But this move could give it more bargaining power, particularly on an international level.  </p><p>It also gives a population an identity, even if Palestinians are perfectly aware of their own identity. Still, it is not legal or at least not legally recognised.</p><p>What I find most important is the symbolism that lies behind the decision, especially for the Palestinian people.</p><p><strong>Johann Soufi: </strong>A state is something that precedes recognition. Recognising something just means recognising its existence. Statehood does not depend on recognition.</p><p>A Palestinian state already exists. That is why 143 UN member states <a href="https://www.france24.com/en/live-news/20240510-thwarted-by-us-palestinians-look-to-un-general-assembly" target="_self">recognise</a> it as a sovereign state, but it is also why Palestine is part of the Rome Statute of the International Criminal Court (<a href="https://www.france24.com/en/tag/icc/" target="_self" class="gtm-add-suggested-tag">ICC</a>) and <a href="https://www.france24.com/en/20111031-2011-10-31-2116-wb-en-focus" target="_self">considered a state</a> by <a href="https://www.france24.com/en/tag/unesco/" target="_self" class="gtm-add-suggested-tag">UNESCO</a>.</p><p>But Palestine faces a unique problem. It is still not a full member of the UN. I think this is extremely important because in reality, [being a member] gives you the right to vote and also gives you political influence. It is a form of power.</p><p>For a state to be fully admitted to the UN General Assembly, the UN Charter requires two-thirds of the member states to vote in favour – which is already the case, since there was a recent resolution in which 143 states voted positively.</p><p>It also requires the <a href="https://www.france24.com/en/tag/un-security-council/" target="_self" class="gtm-add-suggested-tag">UN Security Council</a> to green light the decision through a unanimous vote. And that is what is holding things up. The US <u><a href="https://www.france24.com/en/live-news/20240510-thwarted-by-us-palestinians-look-to-un-general-assembly#:~:text=But the United States -- one of five veto-holding members on the Security Council and Israel" target="_self">vetoed the vote</a></u>.</p><p>As long as the US vetoes the decision, Palestine will not be a full member of the UN.</p><p><strong>Why do you think Spain, Norway and Ireland made this move now?</strong></p><p><strong>Bardet: </strong>The recognition of a state is an act of international public law. But it is also a political act.</p><p>When we look at the scale of <a href="https://www.france24.com/en/tag/israel-hamas-war/" target="_self">the conflict</a> [between Israel and Palestine] over the last few months and what has happened, particularly yesterday in Rafah, we understand that these decisions – especially when taken by European countries – play an important role in pushing for discussions or solutions.</p><p>A solution will only come with two states [Israel and Palestine]. The move legitimises Palestine in its stance, in its existence and gives it more power in pushing negotiators to reach a ceasefire deal. But there is also the question of whether this move could have the opposite effect…</p><p><strong>Soufi: </strong>Norwegian Foreign Minister Espen Barth Eide told <u><a href="https://www.bbc.co.uk/programmes/m001zkrj" target="_blank">the BBC</a></u> on Monday that for him, the decision was about rights. [He said that] Palestinians have had a state since 1948 and have the right to self-determination and [the right to protection under] international law. So it is first and foremost a matter of justice.</p><p>From a more political point of view, it is also the only way to bring hope to the peace process. When talking about a two-state solution as the only credible alternative to war, well, there needs to be two states. If we do not recognise one of the two states, there cannot be a two-state solution.</p><!--:Element_Multimedia:WBMZ311710-F24-EN-20240528:orientation:center:theme:multimedia_element_wide:--><p><strong>What are the broader implications of recognising Palestinian statehood?</strong></p><p><strong>Soufi: </strong>It is all very well to recognise a state, even legally. But being a state also means controlling one’s borders, controlling a territory, the entry and exit of goods and people, the ability to gain access to the land.</p><p>In reality, Palestine is not a state because it does not have control over its territory. It has been occupied [by Israel] since 1967. And so in a very pragmatic way, what will truly make Palestine a state is if it can exercise all the rights a state has over its territory and population.</p><p>When I speak of controlling one’s territory, it also implies demarcating borders. And that is a chicken-and-egg problem. There are those who say we must first agree on what borders constitute Palestine and only then can we recognise its existence. This is a way of eternally postponing official recognition and any move towards a true Palestinian state.</p><p>It is important to know where a state begins and ends, but that should not be a determining factor in whether or not the state of Palestine should be recognised.</p><p>Recognising Palestinian statehood means recognising its people, their right to self-determination and their right to live safely on their territory.</p><p><strong>Bardet: </strong>[Recognising Palestine] also determines who makes up its population.</p><p>I think it is important, too, to think about the reconstruction of Palestine [when the war ends]. Who will represent Palestine? What does this mean in terms of governance?</p><p>For Palestinians, recognition will not change their lives overnight. It is not a magical swish of a wand. But if it helps find a solution to the conflict, that will definitely change people’s lives.</p>
# """

###### EXTRACT FROM 003_prompts_seo_bestof.md ######

# seo_manage_title
# prompt_template = f'''
# As an SEO expert proficient, could you create 10 compelling headline ideas for a post about {user_input} in the same language as the post?
# '''

# seo_manage_url
# prompt_template = f'''
# As an SEO expert proficient, create 10 compelling URL ideas for a post about {user_input} in the same language as the post?
# '''


# seo_manage_meta_description
# prompt_template = f'''
# As an SEO expert proficient, please write a meta description of 150-160 characters for a post about {user_input} in the same language as the post.
# '''

# seo_manage_label_internal_link
# prompt_template = f'''
# As an SEO expert proficient, please generate 10 semantic editorial proposals for link labels based on a post about {user_input} in the same language as the post.
# '''


# seo_manage_ner_tags
# prompt_template = f'''
# Given the input text:user input: {user_input} perform NER detection on it. NER TAGS: FAC;  CARDINAL;  NUMBER;  DEMONYM;  QUANTITY;  TITLE;  PHONE_NUMBER;  NATIONAL;  JOB;  PERSON;  LOC;  NORP;  TIME;  CITY;  EMAIL;  GPE;  LANGUAGE;  PRODUCT;  ZIP_CODE;  ADDRESS;  MONEY;  ORDINAL;  DATE;  EVENT;  CRIMINAL_CHARGE;  STATE_OR_PROVINCE;  RELIGION;  DURATION;  WORK_OF_ART;  PERCENT;  CAUSE_OF_DEATH;  COUNTRY;  ORG;  LAW;  NAME;  COUNTRY;  RELIGION;  TIME answer must be in the format tag:value
# '''

# seo_manage_html_subtitles
# prompt_template = f'''
# As an SEO expert proficient,  please generate an HTML code structure for the post content: "{user_input}" in the same language as the post. Use <H1>, <H2>, and <H3> tags to organize the content effectively. Ensure the structure follows best SEO practices for optimal readability and search engine optimization.
# '''

# seo_manage_image_alt_attribute
# prompt_template = f'''
# As an SEO expert proficient, please generate 10 alt text descriptions for images related to the main topic of the post: "{user_input}" in the same language as the post. Each alt text should incorporate synonyms or variations of the main keyword and must not exceed 125 characters.
# '''



# Calling our function with the prompt
openai_chat(prompt_template)

####### OUTPUT #######
print(openai_chat(prompt_template))


