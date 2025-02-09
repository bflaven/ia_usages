#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_debunk python=3.9.13
conda create --name carbon_footprint python=3.9.13
conda info --envs
source activate ia_debunk
source activate carbon_footprint
conda deactivate


# BURN AFTER READING
source activate ia_debunk
source activate carbon_footprint

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_debunk
conda env remove -n carbon_footprint

# install packages
python -m pip install streamlit 
python -m pip install streamlit

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm/

# launch the file
python 000b1_carbon_footprint_monitoring_system.py


Carbon Footprint Monitoring System


"""

# 000b1_carbon_footprint_monitoring_system.py

# Configuration des variables pour les simulations
CONFIG = {
    # Facteurs d'émission (en kg CO2e par unité)
    'emission_factors': {
        'electricity': 0.5,  # par kWh
        'natural_gas': 2.0,  # par m3
        'water': 0.3,       # par m3
        'waste': 1.5        # par kg
    },
    
    # Objectifs de réduction (en pourcentage)
    'reduction_targets': {
        'electricity': 15,
        'natural_gas': 20,
        'water': 10,
        'waste': 25
    },
    
    # Seuils d'alerte (en kg CO2e)
    'alert_thresholds': {
        'electricity': 1000,
        'natural_gas': 800,
        'water': 300,
        'waste': 500
    }
}

class CarbonFootprintMonitor:
    """Système de surveillance de l'empreinte carbone"""
    
    def __init__(self, config=CONFIG):
        """Initialisation avec la configuration par défaut ou personnalisée"""
        self.config = config
        self.consumption_data = {}
        self.emissions_data = {}
        
    def record_consumption(self, resource_type, amount, period):
        """
        Enregistre la consommation d'une ressource
        
        Args:
            resource_type (str): Type de ressource (electricity, natural_gas, etc.)
            amount (float): Quantité consommée
            period (str): Période de consommation (ex: '2024-02')
        """
        if resource_type not in self.config['emission_factors']:
            raise ValueError(f"Type de ressource invalide: {resource_type}")
            
        if period not in self.consumption_data:
            self.consumption_data[period] = {}
        
        self.consumption_data[period][resource_type] = amount
        
        # Calcul des émissions
        emissions = amount * self.config['emission_factors'][resource_type]
        
        if period not in self.emissions_data:
            self.emissions_data[period] = {}
        
        self.emissions_data[period][resource_type] = emissions
        
        # Vérification des seuils d'alerte
        if emissions > self.config['alert_thresholds'][resource_type]:
            self._generate_alert(resource_type, emissions, period)
    
    def calculate_total_emissions(self, period):
        """Calcule les émissions totales pour une période donnée"""
        if period not in self.emissions_data:
            return 0
        
        return sum(self.emissions_data[period].values())
    
    def generate_reduction_recommendations(self, period):
        """Génère des recommandations de réduction basées sur les objectifs"""
        recommendations = []
        
        if period not in self.emissions_data:
            return recommendations
        
        for resource_type, emissions in self.emissions_data[period].items():
            target = self.config['reduction_targets'][resource_type]
            target_emissions = emissions * (1 - target/100)
            reduction_needed = emissions - target_emissions
            
            if reduction_needed > 0:
                recommendations.append({
                    'resource': resource_type,
                    'current_emissions': emissions,
                    'target_emissions': target_emissions,
                    'reduction_needed': reduction_needed,
                    'reduction_percentage': target
                })
        
        return recommendations
    
    def _generate_alert(self, resource_type, emissions, period):
        """Génère une alerte lorsque le seuil est dépassé"""
        threshold = self.config['alert_thresholds'][resource_type]
        print(f"ALERTE: Émissions de {resource_type} ({emissions:.2f} kg CO2e) "
              f"supérieures au seuil ({threshold} kg CO2e) pour la période {period}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'une instance avec la configuration par défaut
    monitor = CarbonFootprintMonitor()
    
    # Simulation de données pour janvier 2024
    monitor.record_consumption('electricity', 2500, '2024-01')  # kWh
    monitor.record_consumption('natural_gas', 500, '2024-01')   # m3
    monitor.record_consumption('water', 1200, '2024-01')        # m3
    monitor.record_consumption('waste', 400, '2024-01')         # kg
    
    # Calcul des émissions totales
    total_emissions = monitor.calculate_total_emissions('2024-01')
    print(f"\nÉmissions totales pour janvier 2024: {total_emissions:.2f} kg CO2e")
    
    # Génération des recommandations
    recommendations = monitor.generate_reduction_recommendations('2024-01')
    print("\nRecommandations de réduction:")
    for rec in recommendations:
        print(f"- {rec['resource']}: réduire de {rec['reduction_percentage']}% "
              f"({rec['reduction_needed']:.2f} kg CO2e)")


        
        

