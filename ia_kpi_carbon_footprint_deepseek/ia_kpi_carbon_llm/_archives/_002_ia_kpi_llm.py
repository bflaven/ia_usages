#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_debunk python=3.9.13
conda info --envs
source activate ia_debunk
conda deactivate


# BURN AFTER READING
source activate ia_debunk

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_debunk

# install packages
python -m pip install XXX 


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/ia_kpi_llm


# launch the file
python 002_ia_kpi_llm.py


Decision Matrix Implementation


"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class Decision(Enum):
    ACTIVATE = "activate"
    DEACTIVATE = "deactivate"
    REDUCE_VOLUME = "reduce_volume"
    OPTIMIZE = "optimize"

@dataclass
class ServiceThresholds:
    max_carbon_per_request: float  # kg CO2e
    max_daily_carbon: float      # kg CO2e
    max_monthly_carbon: float    # kg CO2e
    max_response_time: float     # ms
    min_success_rate: float      # percentage

class DecisionMatrix:
    def __init__(self):
        self.thresholds = {
            'whisper': ServiceThresholds(
                max_carbon_per_request=0.001,
                max_daily_carbon=1.0,
                max_monthly_carbon=25.0,
                max_response_time=5000,
                min_success_rate=95.0
            ),
            'nllb': ServiceThresholds(
                max_carbon_per_request=0.0005,
                max_daily_carbon=0.5,
                max_monthly_carbon=12.0,
                max_response_time=2000,
                min_success_rate=98.0
            ),
            'mistral-7b': ServiceThresholds(
                max_carbon_per_request=0.002,
                max_daily_carbon=2.0,
                max_monthly_carbon=50.0,
                max_response_time=3000,
                min_success_rate=97.0
            )
        }
        
    def evaluate_service(
        self,
        service_name: str,
        metrics: Dict[str, float]
    ) -> List[Decision]:
        """
        Évalue un service et retourne les décisions recommandées
        """
        decisions = []
        thresholds = self.thresholds.get(service_name)
        
        if not thresholds:
            return [Decision.OPTIMIZE]
        
        # Vérification des seuils
        if metrics['carbon_per_request'] > thresholds.max_carbon_per_request:
            decisions.append(Decision.OPTIMIZE)
            
        if metrics['daily_carbon'] > thresholds.max_daily_carbon:
            decisions.append(Decision.REDUCE_VOLUME)
            
        if metrics['monthly_carbon'] > thresholds.max_monthly_carbon:
            decisions.append(Decision.DEACTIVATE)
            
        if metrics['response_time'] > thresholds.max_response_time:
            decisions.append(Decision.OPTIMIZE)
            
        if metrics['success_rate'] < thresholds.min_success_rate:
            decisions.append(Decision.OPTIMIZE)
            
        return decisions or [Decision.ACTIVATE]
    
    def get_optimization_recommendations(
        self,
        service_name: str,
        metrics: Dict[str, float]
    ) -> List[str]:
        """
        Génère des recommandations d'optimisation spécifiques
        """
        recommendations = []
        thresholds = self.thresholds.get(service_name)
        
        if metrics['carbon_per_request'] > thresholds.max_carbon_per_request:
            recommendations.extend([
                "Optimiser le modèle pour réduire la consommation par requête",
                "Envisager un modèle plus léger",
                "Implémenter du batching pour les requêtes"
            ])
            
        if metrics['response_time'] > thresholds.max_response_time:
            recommendations.extend([
                "Optimiser le pipeline de traitement",
                "Vérifier la configuration du hardware",
                "Considérer la mise en cache des résultats fréquents"
            ])
            
        if metrics['success_rate'] < thresholds.min_success_rate:
            recommendations.extend([
                "Analyser les logs d'erreur",
                "Améliorer la validation des entrées",
                "Renforcer la gestion des cas limites"
            ])
            
        return recommendations

# Example usage
matrix = DecisionMatrix()
service_metrics = {
    'carbon_per_request': 0.0015,
    'daily_carbon': 1.5,
    'monthly_carbon': 30.0,
    'response_time': 4000,
    'success_rate': 96.0
}

decisions = matrix.evaluate_service('whisper', service_metrics)
recommendations = matrix.get_optimization_recommendations('whisper', service_metrics)


