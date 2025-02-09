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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_kpi_carbon_footprint_deepseek/ia_kpi_carbon_llm


# launch the file
python 000b2_carbon_footprint_monitoring_system.py


Carbon Footprint Monitoring System


"""

# 000b2_carbon_footprint_monitoring_system.py

# French: Configuration des variables pour les simulations
FRENCH_STRINGS = {
    'config_description': "Configuration des variables pour les simulations",
    'system_description': "Système de surveillance de l'empreinte carbone",
    'init_description': "Initialisation avec la configuration par défaut ou personnalisée",
    'record_consumption_desc': "Enregistre la consommation d'une ressource",
    'invalid_resource': "Type de ressource invalide",
    'alert_message': "ALERTE: Émissions de {} ({:.2f} kg CO2e) supérieures au seuil ({} kg CO2e) pour la période {}",
    'total_emissions_msg': "Émissions totales pour janvier 2024",
    'reduction_recommendations': "Recommandations de réduction",
    'reduce_by': "réduire de"
}

# Configuration variables for simulations
CONFIG = {
    # Emission factors (in kg CO2e per unit)
    'emission_factors': {
        'electricity': 0.5,  # per kWh
        'natural_gas': 2.0,  # per m3
        'water': 0.3,       # per m3
        'waste': 1.5        # per kg
    },
    
    # Reduction targets (in percentage)
    'reduction_targets': {
        'electricity': 15,
        'natural_gas': 20,
        'water': 10,
        'waste': 25
    },
    
    # Alert thresholds (in kg CO2e)
    'alert_thresholds': {
        'electricity': 1000,
        'natural_gas': 800,
        'water': 300,
        'waste': 500
    }
}

class CarbonFootprintMonitor:
    """Carbon footprint monitoring system"""
    
    def __init__(self, config=CONFIG):
        """Initialization with default or custom configuration"""
        self.config = config
        self.consumption_data = {}
        self.emissions_data = {}
        
    def record_consumption(self, resource_type, amount, period):
        """
        Record resource consumption
        
        Args:
            resource_type (str): Resource type (electricity, natural_gas, etc.)
            amount (float): Amount consumed
            period (str): Consumption period (e.g., '2024-02')
        """
        if resource_type not in self.config['emission_factors']:
            raise ValueError(f"Invalid resource type: {resource_type}")
            
        if period not in self.consumption_data:
            self.consumption_data[period] = {}
        
        self.consumption_data[period][resource_type] = amount
        
        # Calculate emissions
        emissions = amount * self.config['emission_factors'][resource_type]
        
        if period not in self.emissions_data:
            self.emissions_data[period] = {}
        
        self.emissions_data[period][resource_type] = emissions
        
        # Check alert thresholds
        if emissions > self.config['alert_thresholds'][resource_type]:
            self._generate_alert(resource_type, emissions, period)
    
    def calculate_total_emissions(self, period):
        """Calculate total emissions for a given period"""
        if period not in self.emissions_data:
            return 0
        
        return sum(self.emissions_data[period].values())
    
    def generate_reduction_recommendations(self, period):
        """Generate reduction recommendations based on targets"""
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
        """Generate an alert when threshold is exceeded"""
        threshold = self.config['alert_thresholds'][resource_type]
        print(f"ALERT: {resource_type} emissions ({emissions:.2f} kg CO2e) "
              f"exceed threshold ({threshold} kg CO2e) for period {period}")

# Usage example
if __name__ == "__main__":
    # Create an instance with default configuration
    monitor = CarbonFootprintMonitor()
    
    # Simulate data for January 2024
    monitor.record_consumption('electricity', 2500, '2024-01')  # kWh
    monitor.record_consumption('natural_gas', 500, '2024-01')   # m3
    monitor.record_consumption('water', 1200, '2024-01')        # m3
    monitor.record_consumption('waste', 400, '2024-01')         # kg
    
    # Calculate total emissions
    total_emissions = monitor.calculate_total_emissions('2024-01')
    print(f"\nTotal emissions for January 2024: {total_emissions:.2f} kg CO2e")
    
    # Generate recommendations
    recommendations = monitor.generate_reduction_recommendations('2024-01')
    print("\nReduction recommendations:")
    for rec in recommendations:
        print(f"- {rec['resource']}: reduce by {rec['reduction_percentage']}% "
              f"({rec['reduction_needed']:.2f} kg CO2e)")

        
        
        

