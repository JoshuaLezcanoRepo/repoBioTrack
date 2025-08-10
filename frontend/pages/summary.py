"""
Página de Resumen General (Inicio). Muestra las métricas clave.
Versión actualizada para Supabase
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from services import api_client

def mostrar_resumen_general(estado_app):
    # Cargar datos del perfil
    perfil = api_client.cargar_metricas_perfil(estado_app.usuario_actual_id)
    nombre_usuario = perfil.get('nombre', 'Usuario') if perfil else 'Usuario'
    
    st.title(f"¡Bienvenido a BioTrack, {nombre_usuario}! 👋")
    st.markdown("<p class='titleSection'>Resumen Energético</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>Acá podes ver un resumen de tu impacto energético y de sostenibilidad.</p>", unsafe_allow_html=True)
    
    # Cargar métricas
    metricas = api_client.cargar_metricas_resumen(estado_app.usuario_actual_id)
    if not metricas:
        st.warning("No se pudieron cargar las métricas. Añade facturas y electrodomésticos para ver tu resumen.")
        return

    # Tarjetas de métricas principales
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Consumo (kWh)", f"{metricas.get('consumo_total_kwh', 0):.2f}")
    col2.metric("Costo ($)", f"{metricas.get('costo_total', 0):.2f}")
    col3.metric("Huella CO₂ (kg)", f"{metricas.get('huella_co2_total', 0):.2f}")
    col4.metric("Puntos 🌱", metricas.get('puntos_sostenibilidad', 0))

    # Consejo del día
    if metricas.get('consejo_dinamico'):
        st.info(f"💡 **Consejo del Día:** {metricas['consejo_dinamico']['texto']}")

    # Gráfico de Torta (Consumo por Electrodoméstico)
    st.markdown("<p class='titleSection'>Consumo por Electrodoméstico</p>", unsafe_allow_html=True)
    desglose = metricas.get('desglose_electrodomesticos', [])
    if desglose and sum(d['total_kwh'] for d in desglose) > 0:
        df_desglose = pd.DataFrame(desglose)
        fig = px.pie(df_desglose, names="nombre", values="total_kwh", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Añade electrodomésticos para ver el desglose de consumo.")