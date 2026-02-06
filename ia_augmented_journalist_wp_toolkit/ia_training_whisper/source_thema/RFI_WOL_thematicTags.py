# NB OF TAGS: 150
from typing import Literal
from pydantic import BaseModel

# RFI_WOL_thematicTags
class WolofSectionTag(BaseModel):
    label: Literal[
        # Politique Sénégal
        "Macky Sall",
        "Bassirou Diomaye Faye",
        "Ousmane Sonko",
        "Abdoulaye Wade",
        "Assemblée nationale",
        "APR",
        "PASTEF",
        "PDS",
        "Coalition Benno Bokk Yakaar",
        
        # Géographie Sénégal
        "Dakar",
        "Saint-Louis",
        "Thiès",
        "Kaolack",
        "Ziguinchor",
        "Touba",
        "Diourbel",
        "Louga",
        "Fatick",
        "Tambacounda",
        "Kolda",
        "Sédhiou",
        "Kaffrine",
        "Kédougou",
        "Matam",
        "Casamance",
        "Lac Rose",
        "Île de Gorée",
        
        # Personnalités
        "Youssou N'Dour",
        "Cheikh Anta Diop",
        "Léopold Sédar Senghor",
        "Mariama Bâ",
        "Ousmane Sembène",
        "Cheikh Ahmadou Bamba",
        "Amadou Bamba",
        "Serigne Touba",
        "Sadio Mané",
        "Kalidou Koulibaly",
        "Édouard Mendy",
        "Idrissa Gueye",
        
        # Culture et Religion
        "Mouridisme",
        "Tidjanes",
        "Magal de Touba",
        "Grand Magal",
        "Gamou",
        "Tabaski",
        "Korité",
        "Ramadan",
        "Mbalax",
        "Sabar",
        "Taajabone",
        "Ndawrabine",
        "Xalam",
        "Tama",
        "Boubou",
        "Thiéboudienne",
        "Yassa",
        "Mafé",
        "Ceebu jën",
        "Attaya",
        "Thiakry",
        
        # Économie
        "UEMOA",
        "Franc CFA",
        "Port de Dakar",
        "Aéroport Blaise Diagne",
        "Phosphates",
        "Pêche",
        "Arachide",
        "Agriculture",
        "TER",
        "Train Express Régional",
        
        # Médias et Communication
        "RTS",
        "2STV",
        "TFM",
        "Walf TV",
        "Sen TV",
        "Radiodiffusion Télévision Sénégalaise",
        
        # Sport
        "Lions de la Téranga",
        "ASC Diaraf",
        "Jaraaf",
        "Casa Sport",
        "Génération Foot",
        "Lutte sénégalaise",
        "Balla Gaye 2",
        "Modou Lô",
        "Bombardier",
        "Tyson",
        "Eumeu Sène",
        
        # Éducation
        "Université Cheikh Anta Diop",
        "UCAD",
        "École Normale Supérieure",
        "FASTEF",
        
        # International et Diaspora
        "CEDEAO",
        "Union Africaine",
        "France",
        "États-Unis",
        "Italie",
        "Espagne",
        "Diaspora sénégalaise",
        
        # Environnement
        "Parc national du Niokolo-Koba",
        "Delta du Saloum",
        "Langue de Barbarie",
        "Désertification",
        "Érosion côtière",
        
        # Santé
        "Hôpital Principal de Dakar",
        "Hôpital Aristide Le Dantec",
        "Fann",
        "Institut Pasteur de Dakar",
        "Paludisme",
        "COVID-19",
        
        # Société
        "Teranga",
        "Tontine",
        "Ndeysaan",
        "Mbotaay",
        "Taasu",
        "Njël",
        "Xarit",
        
        # Pays Voisins
        "Gambie",
        "Mauritanie",
        "Mali",
        "Guinée",
        "Guinée-Bissau",
        
        # Événements
        "FIDAK",
        "Biennale de l'Art Africain Contemporain",
        "Dakar Biennale",
        "Saint-Louis Jazz Festival",
        
        # Organisations
        "Mouvement des Forces Démocratiques de Casamance",
        "MFDC",
        "Y'en a marre",
        
        # Thèmes généraux
        "Démocratie",
        "Élections",
        "Corruption",
        "Jeunesse",
        "Émigration",
        "Barça ou Barsax",
        "Droits humains",
        "Femmes",
        "Éducation",
        "Santé",
        "Économie",
        "Agriculture",
        "Pêche",
        "Tourisme",
        "Artisanat"
    ]