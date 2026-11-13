from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Sales ADAN Hub",
    page_icon="📊",
    layout="wide",
)

logo_path = Path(__file__).resolve().parent / "assets" / "pepsico_logo.png"
with st.sidebar:
    st.image(str(logo_path), width=90)

visao_geral = st.Page("pages/1_Visao_Geral.py", title="Visão Geral", icon="🏠", default=True)
produtos = st.Page("pages/2_Produtos.py", title="Produtos de Dados", icon="🧩")
algoritmo = st.Page("pages/3_Algoritmo.py", title="Detalhe do Algoritmo", icon="🔬")

pg = st.navigation([visao_geral, produtos, algoritmo])
pg.run()
