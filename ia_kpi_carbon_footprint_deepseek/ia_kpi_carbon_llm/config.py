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