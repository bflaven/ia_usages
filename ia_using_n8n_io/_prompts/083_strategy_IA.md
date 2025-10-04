
# 083_strategy_IA.md

As a python expert, can you rewrite the script below with the changes : 
1. Externalize the following variables like OLLAMA_URL, MODEL_NAME, cms_section_keywords_list, lang, content, prompt_template, STREAM, OUTPUT_FILE in a python file named `config.py` 
2. The file `config.py` will be at the same level as the script named : `query_ollama.py`
3. Output the 2 files completly so I can cut and paste it.

The main objective is to help me to update the values into the file config.py to launch the script easily with new values.


```python
#!/usr/bin/env python3
"""
cd /Users/brunoflaven/Documents/02_copy/_strategy_IA_fmm/matrice_decision_prompt/008_NER_gold_dataset

ollama serve
ollama ps

ollama run mistral:7b
ollama run phi3.5:3.8b 
ollama run neoali/gemma3-8k:4b 
ollama run gemma3:4b 
ollama run deepseek-r1
ollama run phi3.5:3.8b 
ollama run gemma3:4b (gemma3:latest)
ollama run embeddinggemma
ollama run gemma3:1b
ollama run gemma3n
ollama run phi3:14b
ollama run life4living/ChatGPT:latest


ollama rm mistral:7b
ollama rm phi3.5:3.8b 
ollama rm neoali/gemma3-8k:4b 
ollama rm gemma3:4b 
ollama rm deepseek-r1
ollama rm mistral-small:22b
ollama rm embeddinggemma
ollama rm gemma3:1b
ollama rm gemma3n
ollama rm phi3:14b
ollama rm life4living/ChatGPT:latest

python 001a_ner_F24_FR_Focus_MZ508039.py

Script to request locally installed Mistral 7B model via Ollama
All configurable variables are at the beginning for easy modification
"""

import requests
import json
import sys

# =============================================================================
# CONFIGURABLE VARIABLES - Modify these as needed
# =============================================================================

# Ollama configuration
OLLAMA_URL = "http://localhost:11434"  # Default Ollama URL
MODEL_NAME = "mistral:7b"              # Model name in Ollama
# MODEL_NAME = "mistral:latest"  
# MODEL_NAME = "phi3.5:3.8b"  
# MODEL_NAME = "neoali/gemma3-8k:4b"  
# MODEL_NAME = "deepseek-r1:latest"
# MODEL_NAME = "embeddinggemma:latest"
# MODEL_NAME = "gemma3:1b"
# MODEL_NAME = "gemma3n:latest"
# MODEL_NAME = "phi3:14b"
# MODEL_NAME = "life4living/ChatGPT:latest"

# Content variable

cms_section_keywords_list = """
Sports, Économie / Technologie, Culture, Environnement, France, Europe, Afrique, Amériques, Asie-Pacifique, Moyen-Orient
"""

lang = "français"
# lang = "espagnol"
# lang = "anglais"
 
content = """
A la nuit tombée, le marché du jatte de Ruilly s'anime.
Clients et commerçants sont plongés dans le noir.
C'est à la lumière de leurs lampes de poche
qu'ils observent la couleur et la texture des pierres.
Ce soir, Wang Lin, un négociant chinois,
est à la recherche d'une perle rare.
Regardez la qualité de celle-là.
C'est transparent, brillant et lisse.
J'ai proposé 2000 yuan, mais il en veut au moins 4000.
La Birmanie produit le jatte le plus précieux du monde.
Une marchandise que les clients chinois s'arrachent.
Résultat, les commerçants birmans
travaillent sur ce marché frontalier depuis des décennies.
Mon frère nous a envoyé ses biens
depuis la mine.
Ça vient ici, puis je m'occupe des ventes moi-même.
Des produits de qualité, de la jadéité birmane.
Regarde sous la lumière.
J'en ai vendu trois.
Selon les médias chinois, un tiers de la population de Ruilly
travaille dans l'industrie du jatte.
Le lendemain, nous retrouvons Wang Lin dans son bureau.
Il achète de la jadéite, une forme de jatte rare
que l'on trouve principalement en Birmanie.
Ses clients chinois transformeront ensuite les pierres en bijoux.
La popularité de la jadéite remonte à la dynastie Qing.
Elle s'est imprégnée dans la culture chinoise.
D'après Wang Lin, tant qu'il restera du jatte dans les mines,
la demande chinoise ne disparaîtra pas.
Lui ne se sent pas concerné par la façon dont les pierres ont été extraites.
Je ne sais pas. Je n'ai jamais creusé la terre moi-même.
L'extraction, on la laisse aux professionnels.
La collection de pierres est une chose très importante.
La production de Wang Lin provient des montagnes de Pakant,
au nord de la Birmanie, où les miliciens armés combattent la jante.
Selon l'ONG Global Witness, la production de jade
finance l'armée et les groupes rebelles de ce conflit.
Son exploitation intensive entraîne aussi des glissements de terrain meurtriers,
sans oublier une absence totale du droit du travail.
Le jade dit impérial est souvent importé en contrebande
et vendu directement ou plus au franc,
tandis que les pierres de qualité inférieure
finissent à ruiner.
Ici, les commerçants transfrontaliers et les travailleurs immigrés
souffrent encore des conséquences de la guerre civile
et d'un tremblement de terre.
Des contraintes poussant certaines entreprises chinoises
à chercher plus loin.
Elles importent désormais des pierres africaines.
Huang Bikai, le directeur d'usine,
supervise la transformation de la pierre brute en bijoux.
Notre atelier dispose de 66 machines fonctionnelles.
Elles sont en 24 heures sur 24.
Elles produisent environ une pièce toutes les 20 minutes.
Nous disposons aussi d'un espace dédié à la gravure manuelle,
plus complexe, qui nécessite 2 à 3 jours de travail
pour réaliser une pièce.
Son entreprise est chargée de tailler et de polir
le quartz vert des Swatini.
En Chine, ce type de pierre est souvent appelé le jade africain,
une dénomination qui porte à confusion.
Bien que les pierres se ressentent,
le jade véritable est issu de la jadéite ou du néphrite.
Une fois façonné, un bijou produit par Huang peut coûter 220 euros,
alors qu'une version en jade peut atteindre des dizaines de milliers,
voire des millions d'euros.
Les jades africains sont très beaux.
On les utilise souvent en bijouterie,
notamment pour les colliers ou les bracelets de perles.
Leur haute qualité et leur prix abordable
les rendent accessibles à la population africaine.
C'est une pièce qui est très accessible et attrayante
pour un grand nombre de personnes.
En Chine, le ralentissement économique
n'empêche pas les clients de trouver leur bonheur.
Il existe également de nouvelles façons d'acquérir ces accessoires.
Désormais, il suffit d'un clic sur les réseaux sociaux.
Salut les filles !
Alors quand il s'agit de matériaux délicats et raffinés,
oui, les prix sont plus élevés.
Wen Bao vend des bijoux en ligne depuis 4 ans.
Avant, j'étais spécialisée dans le jade bière.
Je suis désolée, mais je ne suis pas en train de me faire enlever
le prix des bières.
Maintenant, je pense que le jade africain
offre un meilleur rapport qualité-prix.
Surtout qu'on achète moins ces dernières années.
En 2024, dans la ville de Ruili,
la vente en direct a augmenté de 33%
comparé à l'année précédente.
Le live stream a permis d'introduire
des types de pierres variées
à des clients plus jeunes.
Ces nouveaux acteurs sont entrés dans une industrie
vieille de plusieurs siècles.
Sortir des sentiers battus
redonne vie à l'économie de Ruili.
Mais selon Richard Orsay, spécialiste de la Birmanie,
rien ne changera de l'autre côté de la frontière.
En cas de baisse du marché,
on a tendance à stocker
plutôt qu'à stopper l'exploitation minière.
Puis on accepte aussi des prix plus bas
parce que la marge bénéficiaire est énorme,
surtout quand on n'a pas à payer d'impôts
parce qu'il s'agit d'un commerce informel
ou de contrebande.
A l'instar des diamants en Occident,
l'importance culturelle des pierres vertes en Chine
est difficile à éradiquer,
quel que soit leur impact,
social ou environnemental.
Le jade symbolise la chance,
la beauté et la longévité.
De part et d'autre de la frontière,
les acteurs de la pierre verte
souhaiteraient graver cette association
dans le marbre.
"""

# Prompt template variable
prompt_template = """
En vous inspirant des exemples de titres suivants et en adoptant le profil d'un journaliste expérimenté spécialisé dans l'actualité internationale, générez un objet JSON valide strictement conforme aux spécifications ci-dessous à partir du {{content}} fourni par l'utilisateur. Le journaliste est un professionnel rigoureux, doté d'un sens aigu de l'éthique et d'une grande curiosité pour les affaires mondiales. Il est connu pour sa capacité à rendre accessibles des sujets complexes, tout en respectant les nuances culturelles et politiques. Aucune balise de code ou formatage supplémentaire n'est autorisée. La sortie doit être un objet JSON strict pouvant être consommé directement par une API, sans texte explicatif, sans balises ou tout autre format additionnel.

Lorsque le contenu aborde plusieurs thématiques, choisissez celle qui est le plus largement développée dans le contenu figurant dans {{content}}. Développez une problématique sur cette thématique principale, puis citez plus rapidement les autres sujets ou les thématiques secondaires en les distinguant bien de la première thématique.

Exemples de titres :
1. Japon : le combat des pères pour la garde partagée
2. Le successeur du Dalaï-lama sera désigné après sa mort, la Chine veut approuver son nom
3. Ibn Battuta, l'explorateur marocain qui "fait passer Marco Polo pour un flemmard"
4. DJ Snake et Omar Sy dévoilent "Patience", l'épopée "universelle" d'un jeune exilé sénégalais
5. Trump a-t-il raison de dire que l'article 5 de l'Otan peut "s'interpréter de plusieurs façons" ?
6. Washington cesse de livrer certaines armes à l'Ukraine, Kiev convoque le chargé d'affaires américain
7. Emmanuel Grégoire, le socialiste qui rêve de succéder à Anne Hidalgo à Paris
8. Fuites, pollutions, prix… En Outre-mer, une "discrimination environnementale" dans l'accès à l'eau

Format attendu du JSON :
1. "1" : Un titre en {{ lang }} journalistique créatif, pertinent, engageant, riche en mots-clés et adapté à une diffusion sur internet et les réseaux sociaux, pour un média d'actualité internationale. Le titre doit être rédigé en {{ lang }} et respecter les règles typographiques de la presse en {{ lang }} : seule la première lettre du titre doit être en majuscule, les autres lettres en minuscules (sauf noms propres). Les titres doivent comporter entre 50 et 60 caractères (espaces compris). Le titre peut contenir une touche d'humour, mais doit toujours refléter fidèlement le contenu, sans sensationnalisme. Puisqu'il traite de l'actualité internationale, les indications de pays ou de régions sont à privilégier dans les mots-clés de ces titres.
2. "2" : Un résumé complet en {{ lang }} et concis de 8 à 10 phrases des points principaux du texte, avec 1 ou 2 mots-clés inclus pour susciter l'intérêt du lecteur. Ce résumé doit faire entre 600 et 1000 caractères, avec une préférence pour 800 caractères. Il doit résumer la thématique principale en développant une problématique sur cette thématique, sans dévoiler tous les détails, afin de susciter l'intérêt du lecteur, mettre en avant l'angle principal de l'article, en étant à la fois informatif et incitatif. Adopter un ton professionnel, clair, structuré, précis et pédagogique, adapté à un grand public exigeant. Intégrer, si pertinent, une citation ou un chiffre marquant tiré du texte, pour renforcer l'accroche et l'intérêt du chapeau. Citez ensuite les autres sujets ou thématiques secondaires en les distinguant bien de la première thématique. Pour accroître la pertinence sur la thématique principale, posez une ou deux questions rhétoriques qui invitent le lecteur à réfléchir davantage sur le sujet principal. Abordez les thématiques secondaires sous forme de questions pour susciter la curiosité du lecteur et l'inciter à lire l'article complet.
3. "3" : Un tableau de quatre à sept mots-clés ou expressions les plus pertinents du texte, que les lecteurs potentiels utiliseraient pour le rechercher. Ces mots-clés doivent être en {{ lang }}.
4. "4" : Un tableau contenant une ou plusieurs catégories en {{ lang }} à laquelle appartient le contenu, choisies strictement parmi la liste suivante : {{ cms_section_keywords_list }}. La catégorie doit être en {{ lang }} et refléter la localisation géographique ou la thématique principale du contenu.

Le résultat doit être en {{ lang }} et structuré en JSON strictement comme suit :
{
  "1": "Titre de l'article 1",
  "2": "Résumé de l'article en 8-10 phrases.",
  "3": ["Mot-clé 1", "Mot-clé 2", "Mot-clé 3", "Mot-clé 4", "Mot-clé 5"],
  "4": ["Catégorie 1", "Catégorie 2"],
}

Assurez-vous que la catégorie choisie dans le champ 4 est bien dans la langue c'est à dire en {{ lang }} et que le format de sortie est strictement respecté. Ne fournissez que l'objet JSON pur en {{ lang }}, sans aucune balise, texte explicatif, ou autre formatage non JSON. Le résultat doit être un JSON brut et valide, strictement conforme aux spécifications, prêt à être consommé par une API.
"""

# Request configuration
STREAM = False  # Set to True for streaming responses

# Output configuration
OUTPUT_FILE = "001a_ner_mistral_f24_fr_focus_mz508039.json"  # File to save the JSON response

# =============================================================================
# MAIN SCRIPT - Do not modify unless you understand the code
# =============================================================================

def create_prompt(template, lang_var, content_var, cms_keywords_var):
    """
    Create the final prompt by replacing template variables
    """
    return (template.replace("{{ lang }}", lang_var)
                   .replace("{{content}}", content_var)
                   .replace("{{ cms_section_keywords_list }}", cms_keywords_var))

def make_ollama_request(url, model, prompt, stream=False):
    """
    Make a request to Ollama API
    
    Args:
        url (str): Ollama server URL
        model (str): Model name
        prompt (str): The prompt to send
        stream (bool): Whether to stream the response
    
    Returns:
        dict: Response from Ollama or error information
    """
    endpoint = f"{url}/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Sending request to {endpoint}")
        print(f"Model: {model}")
        print(f"Prompt length: {len(prompt)} characters")
        print("=" * 50)
        
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.ConnectionError:
        return {
            "error": "Connection failed",
            "message": f"Could not connect to Ollama at {url}. Make sure Ollama is running."
        }
    except requests.exceptions.HTTPError as e:
        return {
            "error": "HTTP error",
            "message": f"HTTP {e.response.status_code}: {e.response.text}"
        }
    except Exception as e:
        return {
            "error": "Unexpected error",
            "message": str(e)
        }

def save_json_to_file(json_data, filename):
    """
    Save JSON data to a file
    
    Args:
        json_data (dict): JSON data to save
        filename (str): Output filename
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error saving to file: {e}")
        return False

def main():
    """
    Main function to execute the script
    """
    print("Ollama Request Script")
    print("=" * 50)
    
    # Create the final prompt
    final_prompt = create_prompt(prompt_template, lang, content, cms_section_keywords_list)
    
    # Make the request
    result = make_ollama_request(
        OLLAMA_URL,
        MODEL_NAME,
        final_prompt,
        STREAM
    )
    
    # Handle the response
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print(f"Message: {result['message']}")
        sys.exit(1)
    else:
        print("✅ Request successful!")
        print("=" * 50)
        print("Response:")
        
        if "response" in result:
            # Print the model's response
            print(result["response"])
            
            # Try to parse as JSON to validate
            try:
                json_response = json.loads(result["response"])
                print("\n" + "=" * 50)
                print("✅ Valid JSON response received")
                print("Formatted JSON:")
                print(json.dumps(json_response, ensure_ascii=False, indent=2))
                
                # Save to file
                if save_json_to_file(json_response, OUTPUT_FILE):
                    print(f"\n✅ JSON response saved to {OUTPUT_FILE}")
                else:
                    print(f"\n❌ Failed to save JSON to {OUTPUT_FILE}")
                    
            except json.JSONDecodeError:
                print("\n" + "=" * 50)
                print("⚠️  Response is not valid JSON")
                print("Cannot save to JSON file")
                
                # Save raw response to text file as fallback
                try:
                    raw_filename = OUTPUT_FILE.replace('.json', '_raw.txt')
                    with open(raw_filename, 'w', encoding='utf-8') as f:
                        f.write(result["response"])
                    print(f"💾 Raw response saved to {raw_filename}")
                except Exception as e:
                    print(f"❌ Error saving raw response: {e}")
        else:
            print("Unexpected response format:")
            print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()


```