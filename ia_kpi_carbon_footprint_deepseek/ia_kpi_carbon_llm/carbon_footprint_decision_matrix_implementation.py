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
python 000a2_carbon_footprint_decision_matrix_implementation.py


Decision Matrix Implementation


"""

# 000a2_carbon_footprint_decision_matrix_implementation.py

# French: Configuration des critères et options pour la matrice de décision
FRENCH_STRINGS = {
    'matrix_config': "Configuration des critères et options pour la matrice de décision",
    'evaluation_criteria': "Critères d'évaluation et leurs poids",
    'implementation_cost': "Coût de mise en œuvre",
    'emission_reduction_potential': "Potentiel de réduction des émissions",
    'maintenance_complexity_fr': "Complexité de maintenance",
    'evaluation_scales_fr': "Échelles d'évaluation pour chaque critère",
    'moderate_maintenance': "Maintenance modérée",
    'matrix_description': "Matrice de décision pour l'évaluation des initiatives de réduction carbone",
    'init_description': "Initialisation avec la configuration par défaut ou personnalisée",
    'add_initiative_desc': "Ajoute une initiative à évaluer",
    'evaluations_desc': "Évaluations pour chaque critère",
    'criteria_error': "Tous les critères doivent être évalués",
    'calculate_score_desc': "Calcule le score pondéré pour une initiative",
    'initiative_not_found': "Initiative non trouvée",
    'invalid_evaluation': "Évaluation invalide pour",
    'generate_recommendations_desc': "Génère des recommandations basées sur les scores",
    'determine_priority_desc': "Détermine la priorité basée sur le score",
    'create_instance': "Création d'une instance avec la configuration par défaut",
    'add_initiatives': "Ajout d'initiatives à évaluer",
    'generate_recommendations_fr': "Génération des recommandations"
}

# Configuration of criteria and options for the decision matrix
CONFIG = {
    # Evaluation criteria and their weights
    'criteria_weights': {
        'cost': 0.3,                    # Implementation cost
        'emission_reduction': 0.4,       # Emission reduction potential
        'implementation_time': 0.15,     # Implementation time
        'maintenance_complexity': 0.15   # Maintenance complexity
    },
    
    # Evaluation scales for each criterion
    'evaluation_scales': {
        'cost': {
            'low': 5,      # < 5000 €
            'medium': 3,   # 5000-15000 €
            'high': 1      # > 15000 €
        },
        'emission_reduction': {
            'high': 5,     # > 30%
            'medium': 3,   # 10-30%
            'low': 1       # < 10%
        },
        'implementation_time': {
            'short': 5,    # < 3 months
            'medium': 3,   # 3-6 months
            'long': 1      # > 6 months
        },
        'maintenance_complexity': {
            'low': 5,      # Simple maintenance
            'medium': 3,   # Moderate maintenance
            'high': 1      # Complex maintenance
        }
    }
}

class DecisionMatrix:
    """Decision matrix for evaluating carbon reduction initiatives"""
    
    def __init__(self, config=CONFIG):
        """Initialization with default or custom configuration"""
        self.config = config
        self.initiatives = {}
        
    def add_initiative(self, name, evaluations):
        """
        Add an initiative to evaluate
        
        Args:
            name (str): Name of the initiative
            evaluations (dict): Evaluations for each criterion
        """
        if not all(criterion in evaluations for criterion in self.config['criteria_weights']):
            raise ValueError("All criteria must be evaluated")
            
        self.initiatives[name] = evaluations
        
    def calculate_score(self, initiative_name):
        """Calculate weighted score for an initiative"""
        if initiative_name not in self.initiatives:
            raise ValueError(f"Initiative not found: {initiative_name}")
            
        evaluations = self.initiatives[initiative_name]
        score = 0
        
        for criterion, weight in self.config['criteria_weights'].items():
            evaluation = evaluations[criterion]
            scale = self.config['evaluation_scales'][criterion]
            
            if evaluation not in scale:
                raise ValueError(f"Invalid evaluation for {criterion}: {evaluation}")
                
            score += scale[evaluation] * weight
            
        return score
    
    def rank_initiatives(self):
        """Rank initiatives by score"""
        rankings = []
        
        for name in self.initiatives:
            score = self.calculate_score(name)
            rankings.append({
                'name': name,
                'score': score
            })
            
        return sorted(rankings, key=lambda x: x['score'], reverse=True)
    
    def generate_recommendations(self):
        """Generate recommendations based on scores"""
        rankings = self.rank_initiatives()
        recommendations = []
        
        for rank, initiative in enumerate(rankings, 1):
            score = initiative['score']
            priority = self._determine_priority(score)
            
            recommendations.append({
                'rank': rank,
                'name': initiative['name'],
                'score': score,
                'priority': priority
            })
            
        return recommendations
    
    def _determine_priority(self, score):
        """Determine priority based on score"""
        if score >= 4:
            return "High"
        elif score >= 3:
            return "Medium"
        else:
            return "Low"

# Usage example
if __name__ == "__main__":
    # Create an instance with default configuration
    matrix = DecisionMatrix()
    
    # Add initiatives to evaluate
    matrix.add_initiative("Solar Panel Installation", {
        'cost': 'high',
        'emission_reduction': 'high',
        'implementation_time': 'medium',
        'maintenance_complexity': 'medium'
    })
    
    matrix.add_initiative("Heating System Optimization", {
        'cost': 'medium',
        'emission_reduction': 'medium',
        'implementation_time': 'short',
        'maintenance_complexity': 'low'
    })
    
    matrix.add_initiative("Waste Reduction Program", {
        'cost': 'low',
        'emission_reduction': 'low',
        'implementation_time': 'short',
        'maintenance_complexity': 'low'
    })
    
    # Generate recommendations
    recommendations = matrix.generate_recommendations()
    
    print("\nInitiative Rankings:")
    for rec in recommendations:
        print(f"{rec['rank']}. {rec['name']}")
        print(f"   Score: {rec['score']:.2f}")
        print(f"   Priority: {rec['priority']}")
             
