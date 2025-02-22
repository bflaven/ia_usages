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
streamlit run 002_carbon_footprint_decision_matrix_implementation_streamlit.py





Carbon Footprint Monitoring System

ranking_initiatives self.lang['ranking_initiatives']
no_initiatives_evaluate self.lang['no_initiatives_evaluate']
configuration_criteria self.lang['configuration_criteria']
weight_criteria self.lang['weight_criteria']


"""

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
            st.rerun()
            
        # Interface principale
        self._show_config_section()
        self._show_initiative_input()
        self._show_rankings()
        self._show_visualization()
        
    def _show_config_section(self):
        """Affiche la section de configuration"""
        with st.expander(self.lang['ranking_initiatives']):
            # Modification des poids des critères
            st.subheader(self.lang['weight_criteria'])
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
        st.subheader(self.lang['ranking_initiatives'])
        
        if not st.session_state.matrix.initiatives:
            st.info(self.lang['no_initiatives_evaluate'])
            return
            
        recommendations = st.session_state.matrix.generate_recommendations()
        
        # Création d'un DataFrame pour l'affichage
        df_rankings = pd.DataFrame(recommendations)
        # Keep original column names to ensure compatibility with visualizations
        display_df = df_rankings.copy()
        display_df.columns = ['Rang', 'Initiative', 'Score', 'Priorité']
        st.dataframe(display_df)
        
    def _show_visualization(self):
        """Affiche les visualisations"""
        if not st.session_state.matrix.initiatives:
            return
            
        st.subheader(self.lang['visualizations'])
        
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
            for criterion, value in evals.items():
                scale = st.session_state.matrix.config['evaluation_scales'][criterion]
                numeric_value = scale[value]
                data[criterion] = numeric_value
            initiatives_data.append(data)
            
        df_radar = pd.DataFrame(initiatives_data)
        
        # Create the radar chart with matching lengths for theta and r
        if initiatives_data:
            # Get all criteria (columns except 'Initiative')
            criteria = [col for col in df_radar.columns if col != 'Initiative']
            
            for initiative in df_radar['Initiative'].unique():
                initiative_data = df_radar[df_radar['Initiative'] == initiative]
                
                # Extract the values for this initiative for all criteria
                r_values = [initiative_data[criterion].iloc[0] for criterion in criteria]
                
                fig_radar = px.line_polar(
                    r=r_values,
                    theta=criteria,  # Use criteria as theta
                    line_close=True,
                    title=f"Évaluation: {initiative}"
                )
                st.plotly_chart(fig_radar)
        
if __name__ == "__main__":
    app = DecisionMatrixApp()
    app.run() 
        
        

