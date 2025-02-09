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
python _api_call_demo.py


Carbon Footprint Monitoring System


"""

# 001_carbon_footprint_monitoring_system_streamlit.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
from config import LANGUAGES, MONITORING_CONFIG
from carbon_footprint_monitoring_system import CarbonFootprintMonitor


class CarbonMonitoringApp:
    """Application Streamlit pour le monitoring de l'empreinte carbone"""
    
    def __init__(self):
        """Initialisation de l'application"""
        # Initialisation de la session state si nécessaire
        if 'language' not in st.session_state:
            st.session_state.language = 'fr'
        if 'monitor' not in st.session_state:
            st.session_state.monitor = CarbonFootprintMonitor(MONITORING_CONFIG)
            
        self.lang = LANGUAGES[st.session_state.language]
        
    def run(self):
        """Exécution de l'application"""
        st.title(self.lang['title'])
        
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
        self._show_data_input_section()
        self._show_visualization_section()
        self._show_recommendations_section()
        
    def _show_config_section(self):
        """Affiche la section de configuration"""
        with st.expander(self.lang['emission_factors']):
            # Affichage et modification des facteurs d'émission
            factors = st.session_state.monitor.config['emission_factors']
            cols = st.columns(len(factors))
            
            for col, (resource, factor) in zip(cols, factors.items()):
                new_factor = col.number_input(
                    f"{resource} (kg CO2e/unité)",
                    value=float(factor),
                    key=f"factor_{resource}"
                )
                st.session_state.monitor.config['emission_factors'][resource] = new_factor
                
    def _show_data_input_section(self):
        """Affiche la section de saisie des données"""
        st.subheader("Saisie des données")
        
        # Sélection de la période
        current_date = datetime.now()
        selected_period = st.date_input(
            "Période",
            value=current_date,
            format="YYYY-MM"
        ).strftime("%Y-%m")
        
        # Saisie des consommations
        cols = st.columns(4)
        consumption_data = {}
        
        for col, resource in zip(cols, st.session_state.monitor.config['emission_factors'].keys()):
            consumption = col.number_input(
                f"{resource}",
                value=0.0,
                step=0.1,
                key=f"consumption_{resource}"
            )
            consumption_data[resource] = consumption
            
        # Bouton de soumission
        if st.button(self.lang['submit']):
            for resource, amount in consumption_data.items():
                st.session_state.monitor.record_consumption(resource, amount, selected_period)
            st.success("Données enregistrées avec succès!")
            
    def _show_visualization_section(self):
        """Affiche la section des visualisations"""
        st.subheader("Visualisations")
        
        if not st.session_state.monitor.emissions_data:
            st.warning("Aucune donnée disponible pour la visualisation")
            return
            
        # Préparation des données pour les graphiques
        df = pd.DataFrame(st.session_state.monitor.emissions_data).T
        df.index.name = 'period'
        df = df.reset_index()
        
        # Graphique des émissions totales par période
        fig_total = px.bar(
            df,
            x='period',
            y=df.drop('period', axis=1).sum(axis=1),
            title="Émissions totales par période"
        )
        st.plotly_chart(fig_total)
        
        # Graphique des émissions par ressource
        df_melted = df.melt(
            id_vars=['period'],
            var_name='resource',
            value_name='emissions'
        )
        fig_by_resource = px.bar(
            df_melted,
            x='period',
            y='emissions',
            color='resource',
            title="Émissions par ressource"
        )
        st.plotly_chart(fig_by_resource)
        
    def _show_recommendations_section(self):
        """Affiche la section des recommandations"""
        st.subheader(self.lang['recommendations'])
        
        if not st.session_state.monitor.emissions_data:
            st.warning("Aucune donnée disponible pour les recommandations")
            return
            
        # Dernière période disponible
        latest_period = max(st.session_state.monitor.emissions_data.keys())
        recommendations = st.session_state.monitor.generate_reduction_recommendations(latest_period)
        
        if not recommendations:
            st.success("Aucune réduction nécessaire pour le moment")
            return
            
        # Affichage des recommandations
        for rec in recommendations:
            with st.expander(f"Recommandation pour {rec['resource']}"):
                cols = st.columns(3)
                cols[0].metric("Émissions actuelles", f"{rec['current_emissions']:.2f} kg CO2e")
                cols[1].metric("Objectif", f"{rec['target_emissions']:.2f} kg CO2e")
                cols[2].metric("Réduction nécessaire", f"{rec['reduction_needed']:.2f} kg CO2e")

if __name__ == "__main__":
    app = CarbonMonitoringApp()
    app.run()

    
        

