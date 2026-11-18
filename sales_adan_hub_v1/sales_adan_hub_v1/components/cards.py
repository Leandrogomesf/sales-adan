import streamlit as st

from components.metrics import tables_table
from components.status import phase_badge_html, phase_progress, secondary_tag_html


def executive_card(label: str, value: str):
    st.metric(label, value)


def product_card(product: dict):
    with st.container(border=True):
        header_col, badge_col = st.columns([3, 1])
        with header_col:
            st.subheader(product["name"])
            st.caption(product.get("code", ""))
        with badge_col:
            tags_html = "".join(secondary_tag_html(t) for t in product.get("phase_tags", []))
            st.markdown(phase_badge_html(product["phase"]) + tags_html, unsafe_allow_html=True)

        st.progress(phase_progress(product["phase"]))
        st.write(product["description"])

        st.caption(
            f"**Módulo:** {product.get('module', '—')} · "
            f"**Áreas:** {', '.join(product.get('consuming_areas', []))}"
        )

        if product.get("dashboard_url"):
            st.link_button("🔗 Abrir Dashboard", product["dashboard_url"])

        tables = product.get("tables", [])
        if tables and tables[0] not in ("Não Disponível", "Não disponível"):
            with st.expander(f"Tabelas geradas ({len(tables)})"):
                tables_table(tables)

        if st.button("Ver detalhe do produto", key=f"open_{product['id']}"):
            st.session_state["selected_product"] = product["id"]
            st.session_state["selected_algorithm"] = None
            st.switch_page("pages/3_Algoritmo.py")


def algorithm_chip(algo: dict, product_id: str):
    label = f"{algo['name']} · {algo.get('status', '')}"
    if st.button(label, key=f"algo_{algo['id']}", use_container_width=True):
        st.session_state["selected_product"] = product_id
        st.session_state["selected_algorithm"] = algo["id"]
        st.switch_page("pages/3_Algoritmo.py")
