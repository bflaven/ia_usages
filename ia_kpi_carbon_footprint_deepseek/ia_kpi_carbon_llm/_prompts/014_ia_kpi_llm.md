
# 012_ia_kpi_llm.md



## INPUT_1
rewrite the complete two files with the same and correct the error. 
```text
ValueError: All arguments should have the same length. The length of argument `theta` is 4, whereas the length of  previously-processed arguments ['r'] is 5
```

**002_carbon_footprint_decision_matrix_implementation_streamlit.py**

```python
# 002_carbon_footprint_decision-matrix_implementation_streamlit.py

import streamlit as st
import pandas as pd
import plotly.express as px
import json
from config import LANGUAGES, DECISION_CONFIG
from carbon_footprint_decision_matrix_implementation import DecisionMatrix

class DecisionMatrixApp:
    """Application Streamlit pour la matrice de décision"""
    
    def __init__(self):
        """Initialisation de l'application"""
        # Initialisation de la session state si nécessaire
        if 'language' not in st.session_state:
            st.session_state.language = 'fr'
        if 'matrix' not in st.session_state:
            st.session_state.matrix = DecisionMatrix(DECISION_CONFIG)
            
        self.lang = LANGUAGES[st.session_state.language]
        
    def run(self):
        """Exécution de l'application"""
        st.title(self.lang['decision_tab'])
        
        # Sélecteur de langue
        selected_lang = st.sidebar.selectbox(
            "Language/Langue",
            options=['fr', 'en'],
            index=0 if st.session_state.language == 'fr' else 1
        )
        
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.experimental_rerun()
            
        # Interface principale
        self._show_config_section()
        self._show_initiative_input()
        self._show_rankings()
        self._show_visualization()
        
    def _show_config_section(self):
        """Affiche la section de configuration"""
        with st.expander("Configuration des critères"):
            # Modification des poids des critères
            st.subheader("Poids des critères")
            weights = st.session_state.matrix.config['criteria_weights']
            cols = st.columns(len(weights))
            
            total_weight = 0
            for col, (criterion, weight) in zip(cols, weights.items()):
                new_weight = col.number_input(
                    criterion,
                    min_value=0.0,
                    max_value=1.0,
                    value=float(weight),
                    step=0.05,
                    key=f"weight_{criterion}"
                )
                total_weight += new_weight
                st.session_state.matrix.config['criteria_weights'][criterion] = new_weight
                
            if abs(total_weight - 1.0) > 0.001:
                st.warning("La somme des poids doit être égale à 1")
                
    def _show_initiative_input(self):
        """Affiche le formulaire d'ajout d'initiative"""
        st.subheader(self.lang['add_initiative'])
        
        # Nom de l'initiative
        initiative_name = st.text_input(self.lang['initiative_name'])
        
        # Évaluation des critères
        cols = st.columns(4)
        evaluations = {}
        
        for col, (criterion, scale) in zip(cols, st.session_state.matrix.config['evaluation_scales'].items()):
            evaluation = col.selectbox(
                criterion,
                options=list(scale.keys()),
                key=f"eval_{criterion}"
            )
            evaluations[criterion] = evaluation
            
        # Bouton d'ajout
        if st.button(self.lang['submit']):
            if not initiative_name:
                st.error("Le nom de l'initiative est requis")
                return
                
            try:
                st.session_state.matrix.add_initiative(initiative_name, evaluations)
                st.success(f"Initiative '{initiative_name}' ajoutée avec succès!")
            except ValueError as e:
                st.error(str(e))
                
    def _show_rankings(self):
        """Affiche le classement des initiatives"""
        st.subheader("Classement des initiatives")
        
        if not st.session_state.matrix.initiatives:
            st.info("Aucune initiative à évaluer")
            return
            
        recommendations = st.session_state.matrix.generate_recommendations()
        
        # Création d'un DataFrame pour l'affichage
        df_rankings = pd.DataFrame(recommendations)
        df_rankings.columns = ['Rang', 'Initiative', 'Score', 'Priorité']
        st.dataframe(df_rankings)
        
    def _show_visualization(self):
        """Affiche les visualisations"""
        if not st.session_state.matrix.initiatives:
            return
            
        st.subheader("Visualisations")
        
        # Préparation des données
        recommendations = st.session_state.matrix.generate_recommendations()
        df_viz = pd.DataFrame(recommendations)
        
        # Graphique des scores
        fig_scores = px.bar(
            df_viz,
            x='name',
            y='score',
            color='priority',
            title="Scores des initiatives",
            labels={'name': 'Initiative', 'score': 'Score', 'priority': 'Priorité'}
        )
        st.plotly_chart(fig_scores)
        
        # Graphique radar des évaluations
        initiatives_data = []
        for name, evals in st.session_state.matrix.initiatives.items():
            data = {'Initiative': name}
            data.update(evals)
            initiatives_data.append(data)
            
        df_radar = pd.DataFrame(initiatives_data)
        fig_radar = px.line_polar(
            df_radar,
            r=[1,2,3,4,5],
            theta=list(st.session_state.matrix.config['criteria_weights'].keys()),
            line_close=True,
            title="Comparaison des évaluations"
        )
        st.plotly_chart(fig_radar)
        
if __name__ == "__main__":
    app = DecisionMatrixApp()
    app.run()
```

**carbon_footprint_decision_matrix_implementation.py**
```python
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

```

## OUTPUT_1_PERPLEXITY
