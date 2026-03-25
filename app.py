import streamlit as st
import pandas as pd

# Configuração da página para um visual mais "clean" e profissional
st.set_page_config(page_title="Angel Performance Dashboard", layout="wide")

# Estilo CSS customizado para melhorar a estética
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
    .main {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Estrutura de Dados
data = {
    "Partida": ["IMG", "Orlando", "Weston", "South Florida"],
    "Minutos Jogados (Texto)": ["40:00", "40:00", "58:20", "19:00"],
    "Minutos Totais": [40, 40, 58.33, 19],
    "Total de Passes": [10, 30, 24, 11],
    "Passes por 90 min": [22.5, 67.5, 37.0, 52.1],
    "Minutos Ativos": [8, 21, 21, 10],
    "% Participação": [20.0, 52.5, 36.2, 52.6]
}

df = pd.DataFrame(data)

# --- SIDEBAR / FILTROS ---
st.sidebar.title("📊 Filtros de Análise")
st.sidebar.markdown("Selecione a partida para detalhamento ou 'Geral' para médias.")
match_option = st.sidebar.selectbox("Escolha a Partida:", ["Geral"] + list(df["Partida"].unique()))

# --- TÍTULO PRINCIPAL ---
st.title("⚽ Dashboard de Performance: Angel")
st.markdown(f"**Status Atual:** Analisando {match_option}")
st.divider()

# --- LÓGICA DE FILTRAGEM ---
if match_option == "Geral":
    display_df = df
    # Médias para o painel geral
    avg_p90 = df["Passes por 90 min"].mean()
    total_passes = df["Total de Passes"].sum()
    avg_participation = df["% Participação"].mean()
    title_suffix = "Médias Gerais"
else:
    display_df = df[df["Partida"] == match_option]
    avg_p90 = display_df["Passes por 90 min"].iloc[0]
    total_passes = display_df["Total de Passes"].iloc[0]
    avg_participation = display_df["% Participação"].iloc[0]
    title_suffix = f"Dados: {match_option}"

# --- SEÇÃO 1: MÉTRICAS (KPIs) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Volume (Passes/90min)", value=f"{avg_p90:.1f}")

with col2:
    st.metric(label="Total de Passes", value=total_passes)

with col3:
    st.metric(label="Densidade de Participação", value=f"{avg_participation:.1f}%")

st.divider()

# --- SEÇÃO 2: TABELAS E GRÁFICOS ---
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader(f"📋 {title_suffix}")
    
    # Formatando a tabela para exibição elegante
    st.dataframe(
        display_df[["Partida", "Minutos Jogados (Texto)", "Total de Passes", "Passes por 90 min", "% Participação", "Janela Ativa"]],
        column_config={
            "% Participação": st.column_config.ProgressColumn(
                "Densidade %", help="Porcentagem de minutos com passes", format="%.1f%%", min_value=0, max_value=100
            ),
            "Total de Passes": st.column_config.NumberColumn("Passes", format="%d 🎯"),
        },
        hide_index=True,
        use_container_width=True
    )

with col_right:
    st.subheader("📈 Comparativo de Verticalidade")
    # Gráfico simples de barras para comparar o P90 entre partidas
    chart_data = df.set_index("Partida")["Passes por 90 min"]
    st.bar_chart(chart_data, color="#2e7d32")

# --- SEÇÃO 3: DETALHAMENTO DE MINUTAGEM ---
st.subheader("⏱️ Detalhes de Minutagem Ativa")
cols = st.columns(len(display_df))

