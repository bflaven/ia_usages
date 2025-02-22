# config.py
# Configuration des langues
LANGUAGES = {
    'fr': {
        'title': 'Système de Monitoring Carbone',
        'monitoring_tab': 'Monitoring',
        'decision_tab': 'Matrice de Décision',
        'emission_factors': 'Facteurs d\'émission',
        'reduction_targets': 'Objectifs de réduction',
        'alert_thresholds': 'Seuils d\'alerte',
        'total_emissions': 'Émissions totales',
        'recommendations': 'Recommandations',
        'submit': 'Soumettre',
        'initiative_name': 'Nom de l\'initiative',
        'add_initiative': 'Ajouter une initiative',
        'ranking_initiatives': 'Classement', 
        'no_initiative': 'Aucune initiative à évaluer', 
        'configuration_criteria': 'Configuration des critères', 
        'weight_criteria': 'Poids des critères', 
        'data_entry': 'Saisie des données', 
        'visualizations': 'Visualisations', 
        'recommendations': 'Recommendations', 
        'no_data_visualization': 'Aucune donnée disponible pour la visualisation', 
        'no_data_recommendations': 'Aucune donnée disponible pour les recommandations',
        'no_reduction_needed': 'Aucune réduction nécessaire pour le moment',

        # Classement des initiatives
        # Aucune initiative à évaluer
        # Configuration des critères
        # Poids des critères
        'ranking_initiatives': 'Classement des initiatives',
        'no_initiatives_evaluate': 'Aucune initiative à évaluer',
        'configuration_criteria': 'Configuration des critères',
        'weight_criteria': 'Poids des critères',



        # 002a_carbon_footprint_decision_matrix_implementation_streamlit.py
        # Aucune initiative à évaluer
        # Configuration des critères
        # Poids des critères
        
        # 001_carbon_footprint_monitoring_system_streamlit.py
        # Saisie des données
        # Visualisations
        # Recommendations
        # Aucune donnée disponible pour la visualisation



    },
    'en': {
        'title': 'Carbon Monitoring System',
        'monitoring_tab': 'Monitoring',
        'decision_tab': 'Decision Matrix',
        'emission_factors': 'Emission Factors',
        'reduction_targets': 'Reduction Targets',
        'alert_thresholds': 'Alert Thresholds',
        'total_emissions': 'Total Emissions',
        'recommendations': 'Recommendations',
        'submit': 'Submit',
        'initiative_name': 'Initiative Name',
        'add_initiative': 'Add Initiative',
        'ranking_initiatives': 'Ranking',
        'no_initiative': 'No initiatives to evaluate', 
        'configuration_criteria': 'Configuration of criteria', 
        'weight_criteria': 'Weight of criteria',
        'data_entry': 'Data Entry', 
        'visualizations': 'Visualizations', 
        'recommendations': 'Recommendations', 
        'no_data_visualization': 'No data available for visualization', 
        'no_data_recommendations': 'No data available for recommendations',
        'no_reduction_needed': 'No reduction needed at this time',
        

        # Ranking of initiatives
        # No initiatives to evaluate
        # Configuration of criteria
        # Weight of criteria
        'ranking_initiatives': 'Ranking of initiatives',
        'no_initiatives_evaluate': 'No initiatives to evaluate',
        'configuration_criteria': 'Configuration of criteria',
        'weight_criteria': 'Weight of criteria',



        # 002a_carbon_footprint_decision_matrix_implementation_streamlit.py
        # No initiatives to evaluate
        # Configuration of criteria
        # Weight of criteria

        # 001_carbon_footprint_monitoring_system_streamlit.py
        # Data Entry data_entry
        # Visualizations visualizations
        # Recommendations recommendations
        # No data available for visualization no_data_visualization 
    }
}

# Configuration des facteurs d'émission et des seuils
MONITORING_CONFIG = {
    'emission_factors': {
        'electricity': 0.5,
        'natural_gas': 2.0,
        'water': 0.3,
        'waste': 1.5
    },
    'reduction_targets': {
        'electricity': 15,
        'natural_gas': 20,
        'water': 10,
        'waste': 25
    },
    'alert_thresholds': {
        'electricity': 1000,
        'natural_gas': 800,
        'water': 300,
        'waste': 500
    }
}

# Configuration de la matrice de décision
DECISION_CONFIG = {
    'criteria_weights': {
        'cost': 0.3,
        'emission_reduction': 0.4,
        'implementation_time': 0.15,
        'maintenance_complexity': 0.15
    },
    'evaluation_scales': {
        'cost': {
            'low': 5,
            'medium': 3,
            'high': 1
        },
        'emission_reduction': {
            'high': 5,
            'medium': 3,
            'low': 1
        },
        'implementation_time': {
            'short': 5,
            'medium': 3,
            'long': 1
        },
        'maintenance_complexity': {
            'low': 5,
            'medium': 3,
            'high': 1
        }
    }
}