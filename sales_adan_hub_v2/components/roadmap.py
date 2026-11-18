from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from components.status import PHASE_COLORS, PHASE_LABELS, PHASE_ORDER
from components.ui import aplicar_estilo
from services.catalog_service import load_algorithms, load_products


def render_roadmap_banner():
    """Banner de maturidade por fase, derivado da fonte única (portfolio.yaml).

    Substitui o antigo roadmap_phases.yaml: uma terceira fonte de fase que
    divergia do catálogo e do detalhe do algoritmo (ver auditoria — A2).

    Toda página chama esta função logo no início, então também é o ponto
    único onde o CSS global da v2 é injetado (ver components/ui.py).
    """
    aplicar_estilo()
    products = load_products()

    with st.expander("🗺️ Roadmap de maturidade do portfólio", expanded=False):
        cols = st.columns(len(PHASE_ORDER))
        for col, phase in zip(cols, PHASE_ORDER):
            color = PHASE_COLORS.get(phase, "#9CA3AF")
            phase_products = [p for p in products if p["phase"] == phase]
            with col:
                st.markdown(
                    f'<div style="border-top:3px solid {color};padding-top:6px;">'
                    f'<strong>{PHASE_LABELS[phase]}</strong></div>',
                    unsafe_allow_html=True,
                )
                for product in sorted(phase_products, key=lambda p: p["name"]):
                    st.caption(product["name"])


def _parse_phase_since(value: str) -> date | None:
    """Converte 'aaaa-mm' em date (dia 1), ou None se ausente/inválido."""
    if not value:
        return None
    try:
        ano, mes = value.split("-")
        return date(int(ano), int(mes), 1)
    except (ValueError, AttributeError):
        return None


def render_roadmap_gantt():
    """Gantt de maturidade do portfólio, por algoritmo, colorido por fase do produto.

    Substitui o antigo expander em texto + a tabela "Evolução do portfólio"
    (ver auditoria — L11/N10/G3): cada barra começa em phase_since (quando o
    algoritmo passou a existir na fase atual do produto) e vai até hoje.
    """
    products = {p["id"]: p for p in load_products()}
    rows = []

    for algo in load_algorithms():
        inicio = _parse_phase_since(algo.get("phase_since"))
        if inicio is None:
            continue
        product = products.get(algo["product_id"])
        if product is None:
            continue
        rows.append(
            {
                "Algoritmo": algo["name"],
                "Produto": product["name"],
                "Fase": PHASE_LABELS.get(product["phase"], product["phase"]),
                "inicio": inicio,
                "fim": date.today(),
            }
        )

    for product in products.values():
        inicio = _parse_phase_since(product.get("phase_since"))
        if inicio is None or product.get("algorithms"):
            continue
        rows.append(
            {
                "Algoritmo": product["name"],
                "Produto": product["name"],
                "Fase": PHASE_LABELS.get(product["phase"], product["phase"]),
                "inicio": inicio,
                "fim": date.today(),
            }
        )

    if not rows:
        st.info("Nenhum dado de início de fase disponível para montar o roadmap.")
        return

    df = pd.DataFrame(rows).sort_values("inicio")
    fase_labels_ordenadas = [PHASE_LABELS[p] for p in PHASE_ORDER]
    cores = {PHASE_LABELS[p]: PHASE_COLORS[p] for p in PHASE_ORDER}

    fig = px.timeline(
        df,
        x_start="inicio",
        x_end="fim",
        y="Algoritmo",
        color="Fase",
        category_orders={"Fase": fase_labels_ordenadas},
        color_discrete_map=cores,
        hover_data={"Produto": True, "inicio": True, "fim": False},
    )
    fig.update_yaxes(autorange="reversed", title=None)
    fig.update_layout(height=max(40 * len(df), 300) + 80, legend_title_text="Fase")
    st.plotly_chart(fig, use_container_width=True)
