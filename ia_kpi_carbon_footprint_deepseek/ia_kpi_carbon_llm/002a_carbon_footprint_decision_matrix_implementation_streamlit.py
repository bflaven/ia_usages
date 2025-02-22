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
streamlit run 002a_carbon_footprint_decision_matrix_implementation_streamlit.py

Carbon Footprint Monitoring System


"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import LANGUAGES, DECISION_CONFIG
from carbon_footprint_decision_matrix_implementation import DecisionMatrix

class DecisionMatrixApp:
    """Application Streamlit pour la matrice de décision"""
    
    def __init__(self):
        """Initialisation de l'application"""
        if 'language' not in st.session_state:
            st.session_state.language = 'fr'
        if 'matrix' not in st.session_state:
            st.session_state.matrix = DecisionMatrix(DECISION_CONFIG)
            
        self.lang = LANGUAGES[st.session_state.language]
        
        # Mapping des évaluations vers des valeurs numériques pour le graphique radar
        self.eval_mapping = {
            'cost': {'low': 5, 'medium': 3, 'high': 1},
            'emission_reduction': {'high': 5, 'medium': 3, 'low': 1},
            'implementation_time': {'short': 5, 'medium': 3, 'long': 1},
            'maintenance_complexity': {'low': 5, 'medium': 3, 'high': 1}
        }
        
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
            st.rerun()
            
        # Interface principale
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._show_initiative_input()
            self._show_visualization()
            
        with col2:
            self._show_config_section()
            self._show_rankings()
        
    def _show_config_section(self):
        """Affiche la section de configuration"""
        with st.expander(f"{self.lang['configuration_criteria']}"):
            st.subheader(f"{self.lang['weight_criteria']}")
            weights = st.session_state.matrix.config['criteria_weights']
            
            total_weight = 0
            for criterion, weight in weights.items():
                new_weight = st.number_input(
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
                st.warning("⚠️ La somme des poids doit être égale à 1")
                
    def _show_initiative_input(self):
        """Affiche le formulaire d'ajout d'initiative"""
        st.subheader(self.lang['add_initiative'])
        
        initiative_name = st.text_input(self.lang['initiative_name'])
        
        cols = st.columns(2)
        evaluations = {}
        
        # Répartition des critères sur deux colonnes
        criteria_items = list(self.eval_mapping.items())
        mid_point = len(criteria_items) // 2
        
        for i, (criterion, scale) in enumerate(criteria_items):
            col_idx = 0 if i < mid_point else 1
            with cols[col_idx]:
                evaluation = st.selectbox(
                    criterion,
                    options=list(scale.keys()),
                    key=f"eval_{criterion}"
                )
                evaluations[criterion] = evaluation
            
        if st.button(self.lang['submit'], type="primary"):
            if not initiative_name:
                st.error("❌ Le nom de l'initiative est requis")
                return
                
            try:
                st.session_state.matrix.add_initiative(initiative_name, evaluations)
                st.success(f"✅ Initiative '{initiative_name}' ajoutée avec succès!")
            except ValueError as e:
                st.error(f"❌ {str(e)}")
                
    def _show_rankings(self):
        """Affiche le classement des initiatives"""
        st.subheader(f"{self.lang['ranking_initiatives']}")
        
        if not st.session_state.matrix.initiatives:
            # st.info("ℹ️ Aucune initiative à évaluer")
            st.info(f"{self.lang['no_initiative']}")
            return
            
        recommendations = st.session_state.matrix.generate_recommendations()
        
        for rec in recommendations:
            score = rec['score']
            color = (
                "🟢" if score >= 4 else
                "🟡" if score >= 3 else
                "🔴"
            )
            st.write(f"{color} {rec['name']}: {score:.2f} ({rec['priority']})")
        
    def _convert_evaluations_to_numeric(self, evaluations):
        """Convertit les évaluations textuelles en valeurs numériques"""
        return {
            criterion: self.eval_mapping[criterion][value]
            for criterion, value in evaluations.items()
        }
        
    def _show_visualization(self):
        """Affiche les visualisations"""
        if not st.session_state.matrix.initiatives:
            return
            
        st.subheader("Visualisations")
        
        tab1, tab2 = st.tabs(["Graphique Radar", "Graphique à barres"])
        
        with tab1:
            # Création du graphique radar
            criteria = list(self.eval_mapping.keys())
            
            fig_radar = go.Figure()
            
            for name, evaluations in st.session_state.matrix.initiatives.items():
                numeric_evals = self._convert_evaluations_to_numeric(evaluations)
                values = [numeric_evals[criterion] for criterion in criteria]
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=criteria,
                    fill='toself',
                    name=name
                ))
                
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )
                ),
                showlegend=True,
                title="Comparaison des initiatives par critère"
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
            
        with tab2:
            # Création du graphique à barres
            recommendations = st.session_state.matrix.generate_recommendations()
            df_viz = pd.DataFrame(recommendations)
            
            fig_scores = px.bar(
                df_viz,
                x='name',
                y='score',
                color='priority',
                title="Scores des initiatives",
                labels={'name': 'Initiative', 'score': 'Score', 'priority': 'Priorité'}
            )
            
            st.plotly_chart(fig_scores, use_container_width=True)
            
            # Affichage détaillé des scores
            if st.checkbox("Voir les détails des scores"):
                st.write("Détail des évaluations:")
                details = []
                
                for name, evals in st.session_state.matrix.initiatives.items():
                    numeric_evals = self._convert_evaluations_to_numeric(evals)
                    weights = st.session_state.matrix.config['criteria_weights']
                    
                    detail = {
                        'Initiative': name,
                        **{f"{c} ({weights[c]:.2f})": v 
                           for c, v in numeric_evals.items()},
                        'Score final': st.session_state.matrix.calculate_score(name)
                    }
                    details.append(detail)
                
                df_details = pd.DataFrame(details)
                st.dataframe(df_details)

if __name__ == "__main__":
    app = DecisionMatrixApp()
    app.run()



    
        
        

