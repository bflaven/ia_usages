"""
007_poc_api_dtsi.py

- Modèle et température définis dans une section CONFIG en tête de script
- Utilise un pattern de classe avec méthode statique AzureEurModel()
- Pas d'argument CLI : tout se configure dans la section CONFIG

[env]
conda create --name ia_achats python=3.9.13
source activate ia_achats


# [path]
cd /Users/brunoflaven/Documents/02_copy/_strategy_IA_fmm/_denia_migration_poc_api_dtsi/
python 007_poc_api_dtsi.py
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import AzureChatOpenAI


# ============================================================================
# CONFIG — tout modifier ici, ne pas toucher au reste du script
# ============================================================================

class CONFIG:
    # --- Modèle ---
    # Choix disponibles : mistral-small | mistral-large | gpt-4.1-mini | gpt-4.1
    # MODEL       = "mistral-small"
    # MODEL       = "mistral-large"
    # MODEL       = "gpt-4.1-mini"
    MODEL       = "gpt-4.1"


    # --- Paramètres du modèle ---
    TEMPERATURE = 0.7
    STREAMING   = False   # ← False pour éviter stream_options
    TIMEOUT     = 30
    MAX_TOKENS  = None    # ← None pour ne pas envoyer max_completion_tokens

    # --- Langue de sortie ---
    # Exemples : "français" | "espagnol" | "anglais" | "arabe"
    LANG        = "espagnol"

    # --- Contenu source à traiter ---
    CONTENT = """
El cantante Luis R. Conríquez abandonó el escenario entre abucheos y objetos lanzados
por el público el pasado 11 de abril. La razón se negó a interpretar un narco corrido
que glorificaba a los carteles. En contraste, otro grupo, Los Alegres del Barranco, proyectó
el rostro de El Mencho, líder del poderoso cartel Jalisco Nueva Generación, frente a
11.000 fanáticos eufóricos en Guadalajara. En la tercera ciudad más grande del país,
capital del estado donde nació ese cartel, los narco corridos siguen siendo populares.
Este grupo originario de Sinaloa ya no puede interpretar esta canción en público.
Tras el concierto de Los Alegres del Barranco, las autoridades de Jalisco, uniéndose a otras
10 entidades, prohibieron las presentaciones públicas de este género.
Para evitar problemas con el gobierno, estos cantantes han optado por ahora por mantener
un perfil bajo. Los intérpretes de este género a veces funcionan como voceros de grupos criminales
que financian sus carreras y encargan canciones.
Al menos 25 intérpretes de narco corridos han sido asesinados en México en los últimos años.
Las víctimas más recientes fueron músicos del grupo Fugitivo, asesinados en el norte del país
el pasado 25 de mayo por miembros del cartel del Golfo.
La guerra de baja intensidad en México deja cada año decenas de miles de muertos y desaparecidos.
En respuesta a la polémica, la presidenta de México lanzó el concurso México Canta,
buscando canciones de cualquier género que no hagan apología al delito o al crimen.
El concurso, abierto a participantes de México y Estados Unidos, finalizará el 5 de octubre.
El ganador grabará un álbum de 12 canciones con una de las disqueras más importantes del país.
"""


# ============================================================================
# PROMPT TEMPLATE
# ============================================================================

PROMPT_TEMPLATE = """
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
3. "3" : Un tableau des cinq mots-clés ou expressions les plus pertinents du texte, que les lecteurs potentiels utiliseraient pour le rechercher. Ces mots-clés doivent être en {{ lang }}.
4. "4" : Une catégorie unique en {{ lang }} à laquelle appartient le contenu, en utilisant des catégories larges adaptées à un site d'information international en {{ lang }}, telles que "France", "Europe", "Afrique", "Amériques", "Asie-Pacifique", "Moyen-Orient", "Sports", "Économie / Technologie", "Culture" et "Environnement". La catégorie doit être en {{ lang }} et refléter la localisation géographique ou la thématique principale du contenu.

Le résultat doit être en {{ lang }} et structuré en JSON strictement comme suit :
{
  "1": "Titre de l'article 1",
  "2": "Résumé de l'article en 8-10 phrases.",
  "3": ["Mot-clé 1", "Mot-clé 2", "Mot-clé 3", "Mot-clé 4", "Mot-clé 5"],
  "4": "Catégorie ou sujet principal"
}

Assurez-vous que la catégorie choisie dans le champ 4 est bien dans la langue c'est à dire en {{ lang }} et que le format de sortie est strictement respecté. Ne fournissez que l'objet JSON pur en {{ lang }}, sans aucune balise, texte explicatif, ou autre formatage non JSON. Le résultat doit être un JSON brut et valide, strictement conforme aux spécifications, prêt à être consommé par une API.

Contenu source à traiter :
{{content}}
"""


# ============================================================================
# CLASSE AzureClient — fabrique du modèle
# ============================================================================

class AzureClient:

    @staticmethod
    def AzureEurModel(
    model: str,
    temperature: float = 0.7,
    streaming: bool = False,
    timeout: int = 30,
    max_tokens: int = None,
    ) -> AzureChatOpenAI:
        load_dotenv(Path(__file__).resolve().parent / ".env")

        azure_endpoint = os.getenv("ENDPOINT")
        api_key        = os.getenv("API_KEY")

        if not azure_endpoint or not api_key:
            raise RuntimeError("ENDPOINT ou API_KEY manquant dans .env.")

        kwargs = dict(
            azure_endpoint   = azure_endpoint,
            api_key          = api_key,
            api_version      = "2024-05-01-preview",
            azure_deployment = model,
            temperature      = temperature,
            streaming        = streaming,
            timeout          = timeout,
        )
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens   # seulement si explicitement défini

        return AzureChatOpenAI(**kwargs)


# ============================================================================
# HELPERS
# ============================================================================

def build_prompt(lang: str, content: str) -> str:
    """Injecte {{ lang }} et {{content}} dans le gabarit PROMPT_TEMPLATE."""
    return (
        PROMPT_TEMPLATE
        .replace("{{ lang }}", lang)
        .replace("{{content}}", content)
    )


def print_banner() -> None:
    print("=" * 80)
    print("🚀  007_poc_api_dtsi.py — génération JSON (titre, résumé, mots-clés, catégorie)")
    print(f"   ├─ Modèle      : {CONFIG.MODEL}")
    print(f"   ├─ Langue      : {CONFIG.LANG}")
    print(f"   ├─ Température : {CONFIG.TEMPERATURE}")
    print(f"   ├─ Streaming   : {CONFIG.STREAMING}")
    print(f"   ├─ Timeout     : {CONFIG.TIMEOUT}s")
    print(f"   └─ Max tokens  : {CONFIG.MAX_TOKENS}")
    print("=" * 80)


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    print_banner()

    llm = AzureClient.AzureEurModel(
        model       = CONFIG.MODEL,
        temperature = CONFIG.TEMPERATURE,
        streaming   = CONFIG.STREAMING,
        timeout     = CONFIG.TIMEOUT,
        max_tokens  = CONFIG.MAX_TOKENS,
    )

    final_prompt = build_prompt(CONFIG.LANG, CONFIG.CONTENT)

    messages = [
        ("system", "Tu es un assistant qui renvoie uniquement du JSON strictement valide."),
        ("user",   final_prompt),
    ]

    try:
        response = llm.invoke(messages)
        print("\n✅ Sortie du modèle (JSON attendu) :")
        print("-" * 80)
        print(response.content)
        print("-" * 80)
    except Exception as e:
        print(f"\n❌ Erreur : {e}")


if __name__ == "__main__":
    main()