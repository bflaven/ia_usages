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
python 001_carbon_footprint_monitoring_system.py


Carbon Footprint Monitoring System


"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional
import psutil
import GPUtil
import json
from pathlib import Path

# Configuration globale
CONFIG = {
    # Paramètres de charge de travail
    'MONTHLY_FILE_COUNT': 500,  # Nombre de fichiers par mois
    'GROWTH_RATE': 1.5,        # Taux de croissance mensuel
    
    # Durées moyennes des contenus
    'AUDIO_DURATION_MINUTES': 15,     # Durée moyenne des fichiers audio
    'VIDEO_DURATION_MINUTES': 20,     # Durée moyenne des fichiers vidéo
    'TEXT_TOKEN_COUNT': 2000,         # Nombre moyen de tokens par texte
    
    # Répartition par langue (en pourcentage)
    'LANGUAGE_DISTRIBUTION': {
        'FR': 40,
        'EN': 30,
        'ES': 20,
        'AR': 10
    },
    
    # Consommation électrique des modèles (kWh)
    'MODEL_POWER_CONSUMPTION': {
        'whisper': 0.2,    # kWh par heure d'audio
        'nllb': 0.1,       # kWh par MB de texte
        'mistral-7b': 0.15 # kWh par inférence
    },
    
    # Facteurs de complexité par langue
    'LANGUAGE_COMPLEXITY': {
        'FR': 1.0,
        'EN': 1.0,
        'ES': 1.1,
        'AR': 1.3
    },
    
    # Paramètres hardware
    'CPU_TDP_WATTS': 65,      # TDP du CPU en watts
    'GPU_TDP_WATTS': 250,     # TDP du GPU en watts
    'MEMORY_WATTS_PER_GB': 0.37,  # Consommation par GB de RAM
    
    # Facteur d'émission du grid (kgCO2e/kWh)
    'GRID_CARBON_INTENSITY': 0.475
}

@dataclass
class CarbonMetrics:
    endpoint: str
    duration_ms: float
    cpu_percent: float
    memory_mb: float
    gpu_utilization: Optional[float]
    input_size_mb: float
    model_type: str
    language: str

class CarbonFootprintMonitor:
    def __init__(self, config=CONFIG):
        self.config = config
        self.metrics_history: List[CarbonMetrics] = []
        
    def simulate_request(self, model_type: str, language: str, input_size_mb: float) -> CarbonMetrics:
        """Simule une requête et retourne les métriques"""
        # Simule l'utilisation des ressources
        duration = self._simulate_duration(model_type, input_size_mb)
        cpu_usage = self._simulate_cpu_usage(model_type)
        memory_usage = self._simulate_memory_usage(model_type)
        gpu_usage = self._simulate_gpu_usage(model_type)
        
        metrics = CarbonMetrics(
            endpoint=f"/{model_type}/{language}",
            duration_ms=duration,
            cpu_percent=cpu_usage,
            memory_mb=memory_usage,
            gpu_utilization=gpu_usage,
            input_size_mb=input_size_mb,
            model_type=model_type,
            language=language
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def calculate_carbon_footprint(self, metrics: CarbonMetrics) -> float:
        """Calcule l'empreinte carbone en kg CO2e"""
        # Calcul de la consommation électrique de base
        base_power = (
            metrics.cpu_percent * 0.01 * self.config['CPU_TDP_WATTS'] +
            metrics.memory_mb * self.config['MEMORY_WATTS_PER_GB'] / 1024 +
            (metrics.gpu_utilization or 0) * self.config['GPU_TDP_WATTS']
        )
        
        # Conversion en kWh
        duration_hours = metrics.duration_ms / (1000 * 3600)
        power_consumption = base_power * duration_hours
        
        # Application des facteurs spécifiques
        model_factor = self.config['MODEL_POWER_CONSUMPTION'].get(metrics.model_type, 0.1)
        language_factor = self.config['LANGUAGE_COMPLEXITY'].get(metrics.language, 1.0)
        
        # Calcul final
        carbon_footprint = (
            power_consumption *
            model_factor *
            language_factor *
            self.config['GRID_CARBON_INTENSITY']
        )
        
        return carbon_footprint
    
    def simulate_monthly_usage(self) -> Dict:
        """Simule l'usage mensuel et calcule l'empreinte carbone totale"""
        total_footprint = 0
        footprint_by_model = {}
        footprint_by_language = {}
        
        # Pour chaque type de modèle
        for model_type in self.config['MODEL_POWER_CONSUMPTION'].keys():
            footprint_by_model[model_type] = 0
            
            # Pour chaque langue
            for lang, percentage in self.config['LANGUAGE_DISTRIBUTION'].items():
                file_count = (self.config['MONTHLY_FILE_COUNT'] * percentage / 100)
                
                # Simulation des requêtes
                input_size = self._get_input_size(model_type)
                metrics = self.simulate_request(model_type, lang, input_size)
                footprint = self.calculate_carbon_footprint(metrics) * file_count
                
                # Accumulation des résultats
                total_footprint += footprint
                footprint_by_model[model_type] += footprint
                footprint_by_language[lang] = footprint_by_language.get(lang, 0) + footprint
        
        return {
            'total_kg_co2e': total_footprint,
            'by_model': footprint_by_model,
            'by_language': footprint_by_language,
            'projections': self._calculate_projections(total_footprint)
        }
    
    def _simulate_duration(self, model_type: str, input_size_mb: float) -> float:
        """Simule la durée de traitement en ms"""
        base_duration = {
            'whisper': 500,
            'nllb': 200,
            'mistral-7b': 300
        }.get(model_type, 250)
        return base_duration * input_size_mb
    
    def _simulate_cpu_usage(self, model_type: str) -> float:
        """Simule l'utilisation CPU"""
        return {
            'whisper': 80,
            'nllb': 60,
            'mistral-7b': 70
        }.get(model_type, 50)
    
    def _simulate_memory_usage(self, model_type: str) -> float:
        """Simule l'utilisation mémoire en MB"""
        return {
            'whisper': 2000,
            'nllb': 1500,
            'mistral-7b': 3000
        }.get(model_type, 1000)
    
    def _simulate_gpu_usage(self, model_type: str) -> float:
        """Simule l'utilisation GPU"""
        return {
            'whisper': 0.8,
            'nllb': 0.6,
            'mistral-7b': 0.7
        }.get(model_type, 0.5)
    
    def _get_input_size(self, model_type: str) -> float:
        """Retourne la taille d'entrée simulée en MB"""
        if model_type == 'whisper':
            return self.config['AUDIO_DURATION_MINUTES'] * 0.5  # 0.5 MB par minute
        elif model_type == 'nllb':
            return self.config['TEXT_TOKEN_COUNT'] * 0.0001  # 0.0001 MB par token
        else:
            return 0.1  # Taille par défaut
    
    def _calculate_projections(self, monthly_footprint: float) -> Dict:
        """Calcule les projections de croissance"""
        projections = {
            '3_months': monthly_footprint * (1 + self.config['GROWTH_RATE']) ** 3,
            '6_months': monthly_footprint * (1 + self.config['GROWTH_RATE']) ** 6,
            '12_months': monthly_footprint * (1 + self.config['GROWTH_RATE']) ** 12
        }
        return projections

# Exemple d'utilisation
if __name__ == "__main__":
    monitor = CarbonFootprintMonitor()
    results = monitor.simulate_monthly_usage()
    
    # Affichage des résultats
    print("\nRésultats de la simulation:")
    print(f"Empreinte carbone totale: {results['total_kg_co2e']:.2f} kg CO2e")
    print("\nPar modèle:")
    for model, footprint in results['by_model'].items():
        print(f"- {model}: {footprint:.2f} kg CO2e")
    print("\nPar langue:")
    for lang, footprint in results['by_language'].items():
        print(f"- {lang}: {footprint:.2f} kg CO2e")
    print("\nProjections:")
    for period, value in results['projections'].items():
        print(f"- {period}: {value:.2f} kg CO2e")

        

