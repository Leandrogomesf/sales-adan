import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from components.cards import product_card
from components.filters import apply_product_filters, product_filters, render_clear_filters_button
from components.roadmap import render_roadmap_banner
from components.status import phase_legend_html
from services.catalog_service import load_products

render_roadmap_banner()

st.title("Produtos de Dados")
st.caption("Catálogo de produtos de dados do portfólio Sales ADAN.")
st.markdown(phase_legend_html(), unsafe_allow_html=True)

products = load_products()

filters = product_filters(products)
filtered = apply_product_filters(products, filters)

st.caption(f"{len(filtered)} de {len(products)} produtos exibidos.")

if not filtered:
    st.info("Nenhum produto encontrado com os filtros selecionados.")
    render_clear_filters_button()
else:
    cols = st.columns(3)
    for i, product in enumerate(filtered):
        with cols[i % 3]:
            product_card(product)
