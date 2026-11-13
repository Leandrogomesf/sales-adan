import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from components.cards import product_card
from components.filters import apply_product_filters, product_filters
from components.roadmap import render_roadmap_banner
from services.catalog_service import load_products

render_roadmap_banner()

st.title("Produtos de Dados")
st.caption("Catálogo de produtos de dados do portfólio Sales ADAN.")

products = load_products()

filters = product_filters(products)
filtered = apply_product_filters(products, filters)

st.caption(f"{len(filtered)} de {len(products)} produtos exibidos.")

if not filtered:
    st.info("Nenhum produto encontrado com os filtros selecionados.")
else:
    cols = st.columns(2)
    for i, product in enumerate(filtered):
        with cols[i % 2]:
            product_card(product)
