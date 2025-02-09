
# 002_ia_kpi_llm.md



## PROMPT_1


1. Réécris les deux scripts en isolant les valeurs pour les variables en début de afin de faire des simulations pour avec de vrais chiffres sur la base de ce j'ai indiqué parce tes scripts ne produisent aucun résultat.

- Carbon Footprint Monitoring System (001_carbon_footprint_monitoring_system.py)
- Decision Matrix Implementation (002_carbon_footprint_decision-matrix_implementation.py)


2. En tant que développeur python et streamlit, écris à nouveau une application comprenant deux onglets avec des simulations chiffrées. Externalise le maximum de variables (chiffres, langues) de sorte que je puisse jouer avec et simuler des scénarios

- Carbon Footprint Monitoring System (001_carbon_footprint_monitoring_system_streamlit.py)
- Decision Matrix Implementation (002_carbon_footprint_decision-matrix_implementation_streamlit.py)

Note
- Tout le code doit être commenté.
- Recourir aux bonnes pratiques de programmation en utilisant des classes et des fonctions pour rendre le code lisible et maintenable.


## CLAUDE_1


project/
│
├── config.py                                                # Configuration (langues et paramètres)
├── carbon_footprint_monitoring_system.py                    # Classe de base pour le monitoring
├── carbon_footprint_decision_matrix_implementation.py       # Classe de base pour la matrice de décision
├── 001_carbon_footprint_monitoring_system_streamlit.py     # Application Streamlit de monitoring
└── 002_carbon_footprint_decision-matrix_implementation_streamlit.py  # Application Streamlit de matrice de décision




StreamlitAPIException: The provided format (YYYY-MM) is not valid. DateInput format should be one of YYYY/MM/DD, DD/MM/YYYY, or MM/DD/YYYY and can also use a period (.) or hyphen (-) as separators.




