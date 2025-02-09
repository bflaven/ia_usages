
# 008_ia_kpi_llm.md


## PROMPT_1
As a python expert, rewrite the script, extract all the sentences in French, put them in variables at the top of the script, make the sentences in French as comment and use English instead of the French when the value is printed out.


```python

# 002_carbon_footprint_decision-matrix_implementation.py

# Configuration des critères et options pour la matrice de décision
CONFIG = {
    # Critères d'évaluation et leurs poids
    'criteria_weights': {
        'cost': 0.3,                    # Coût de mise en œuvre
        'emission_reduction': 0.4,       # Potentiel de réduction des émissions
        'implementation_time': 0.15,     # Temps de mise en œuvre
        'maintenance_complexity': 0.15   # Complexité de maintenance
    },
    
    # Échelles d'évaluation pour chaque critère
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
            'short': 5,    # < 3 mois
            'medium': 3,   # 3-6 mois
            'long': 1      # > 6 mois
        },
        'maintenance_complexity': {
            'low': 5,      # Maintenance simple
            'medium': 3,   # Maintenance modérée
            'high': 1      # Maintenance complexe
        }
    }
}

class DecisionMatrix:
    """Matrice de décision pour l'évaluation des initiatives de réduction carbone"""
    
    def __init__(self, config=CONFIG):
        """Initialisation avec la configuration par défaut ou personnalisée"""
        self.config = config
        self.initiatives = {}
        
    def add_initiative(self, name, evaluations):
        """
        Ajoute une initiative à évaluer
        
        Args:
            name (str): Nom de l'initiative
            evaluations (dict): Évaluations pour chaque critère
        """
        if not all(criterion in evaluations for criterion in self.config['criteria_weights']):
            raise ValueError("Tous les critères doivent être évalués")
            
        self.initiatives[name] = evaluations
        
    def calculate_score(self, initiative_name):
        """Calcule le score pondéré pour une initiative"""
        if initiative_name not in self.initiatives:
            raise ValueError(f"Initiative non trouvée: {initiative_name}")
            
        evaluations = self.initiatives[initiative_name]
        score = 0
        
        for criterion, weight in self.config['criteria_weights'].items():
            evaluation = evaluations[criterion]
            scale = self.config['evaluation_scales'][criterion]
            
            if evaluation not in scale:
                raise ValueError(f"Évaluation invalide pour {criterion}: {evaluation}")
                
            score += scale[evaluation] * weight
            
        return score
    
    def rank_initiatives(self):
        """Classe les initiatives par score"""
        rankings = []
        
        for name in self.initiatives:
            score = self.calculate_score(name)
            rankings.append({
                'name': name,
                'score': score
            })
            
        return sorted(rankings, key=lambda x: x['score'], reverse=True)
    
    def generate_recommendations(self):
        """Génère des recommandations basées sur les scores"""
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
        """Détermine la priorité basée sur le score"""
        if score >= 4:
            return "Haute"
        elif score >= 3:
            return "Moyenne"
        else:
            return "Basse"

# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'une instance avec la configuration par défaut
    matrix = DecisionMatrix()
    
    # Ajout d'initiatives à évaluer
    matrix.add_initiative("Installation de panneaux solaires", {
        'cost': 'high',
        'emission_reduction': 'high',
        'implementation_time': 'medium',
        'maintenance_complexity': 'medium'
    })
    
    matrix.add_initiative("Optimisation du système de chauffage", {
        'cost': 'medium',
        'emission_reduction': 'medium',
        'implementation_time': 'short',
        'maintenance_complexity': 'low'
    })
    
    matrix.add_initiative("Programme de réduction des déchets", {
        'cost': 'low',
        'emission_reduction': 'low',
        'implementation_time': 'short',
        'maintenance_complexity': 'low'
    })
    
    # Génération des recommandations
    recommendations = matrix.generate_recommendations()
    
    print("\nClassement des initiatives:")
    for rec in recommendations:
        print(f"{rec['rank']}. {rec['name']}")
        print(f"   Score: {rec['score']:.2f}")
        print(f"   Priorité: {rec['priority']}")





```

## CLAUDE_1



