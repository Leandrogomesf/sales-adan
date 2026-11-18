import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st

from components.kpi_card import ICONS, kpi_card
from components.roadmap import render_roadmap_banner
from components.status import phase_badge_html
from services.catalog_service import load_initiative, load_pilot_results, load_roadmap

initiative = load_initiative()
roadmap = load_roadmap()

render_roadmap_banner()

st.title(initiative["name"])
st.caption(initiative["tagline"])
st.caption(f"Última atualização: {initiative['last_updated']}")

st.divider()

st.subheader("Visão executiva")

KPI_STYLE = {
    "Objetivo": (ICONS["target"], "brand"),
    "Público impactado": (ICONS["users"], "accent"),
    "Produtos ativos": (ICONS["layers"], "green"),
    "Última atualização": (ICONS["clock"], "orange"),
}

cols = st.columns(len(initiative["executive_cards"]))
for col, card in zip(cols, initiative["executive_cards"]):
    icon, color = KPI_STYLE.get(card["label"], (ICONS["pin"], "brand"))
    with col:
        kpi_card(icon, card["label"], card["value"], color)
        if card["label"] == "Produtos ativos":
            if st.button("Ver Produtos de Dados →", key="goto_produtos", use_container_width=True):
                st.switch_page("pages/2_Produtos.py")

st.divider()

st.subheader("Portfólio em números")

PORTFOLIO_STAT_STYLE = {
    "Algoritmos de ML": (ICONS["brain"], "brand"),
    "Features construídas": (ICONS["dna"], "accent"),
    "Hipóteses técnicas testadas": (ICONS["flask"], "orange"),
    "Tasks impactadas / mês": (ICONS["check"], "green"),
}

stat_cols = st.columns(len(initiative["portfolio_stats"]))
for col, stat in zip(stat_cols, initiative["portfolio_stats"]):
    icon, color = PORTFOLIO_STAT_STYLE.get(stat["label"], (ICONS["pin"], "brand"))
    with col:
        kpi_card(icon, stat["label"], stat["value"], color)
        if stat["label"] == "Algoritmos de ML":
            if st.button("Ver Detalhe do Algoritmo →", key="goto_algoritmo", use_container_width=True):
                st.switch_page("pages/3_Algoritmo.py")

st.divider()

september_pilot = next(
    (p for p in load_pilot_results() if p["id"] == "set-2026-uplift"), None
)

if september_pilot:
    st.subheader("Resultados do Piloto de Setembro")
    st.caption(september_pilot["note"])

    SEPTEMBER_ICON_STYLE = [
        (ICONS["trending-up"], "brand"),
        (ICONS["weight"], "green"),
        (ICONS["package"], "accent"),
        (ICONS["clock"], "orange"),
    ]

    big_numbers = september_pilot["big_numbers"]
    pilot_cols = st.columns(len(big_numbers))
    for col, stat, (icon, color) in zip(pilot_cols, big_numbers, SEPTEMBER_ICON_STYLE):
        with col:
            kpi_card(icon, stat["label"], stat["value"], color)

    if st.button("Ver Testes e Resultados →", key="goto_testes_resultados"):
        st.switch_page("pages/4_Testes_e_Resultados.py")

st.divider()

st.subheader("Framework de KPIs")
kpi_framework = initiative["kpi_framework"]
st.markdown(
    f"""
    <div style="background:#0f172a;color:#ffffff;border-radius:16px;padding:18px 24px;
                text-align:center;margin-bottom:18px;">
        <div style="font-size:0.75rem;letter-spacing:1.5px;color:#93c5fd;font-weight:700;">
            NORTH STAR
        </div>
        <div style="font-size:1.15rem;font-weight:700;margin-top:4px;">
            {kpi_framework["north_star"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

PILLAR_COLORS = {
    "brand": "#2563eb",
    "orange": "#ea580c",
    "green": "#16a34a",
    "accent": "#6d5efc",
}

pillar_cols = st.columns(len(kpi_framework["pillars"]))
for col, pillar in zip(pillar_cols, kpi_framework["pillars"]):
    color = PILLAR_COLORS.get(pillar["color"], "#2563eb")
    metrics_html = "".join(f"<li>{m}</li>" for m in pillar["metrics"])
    with col:
        st.markdown(
            f"""
            <div style="border:2px solid {color};border-radius:14px;padding:14px 16px;
                        min-height:150px;">
                <div style="color:{color};font-weight:700;font-size:0.95rem;margin-bottom:8px;">
                    {pillar["name"]}
                </div>
                <ul style="margin:0;padding-left:18px;font-size:0.85rem;color:#374151;">
                    {metrics_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

header_col, button_col = st.columns([4, 1])
with header_col:
    st.subheader("Resumo da iniciativa")
with button_col:
    if st.button("Ver Metodologia →", key="goto_metodologia"):
        st.switch_page("pages/5_Metodologia.py")
st.write(initiative["description"])

st.subheader("Áreas impactadas")
st.write(", ".join(initiative["impacted_areas"]))

st.divider()

st.subheader("Time e responsáveis")
team_df = pd.DataFrame(initiative["team"])
team_df = team_df.rename(
    columns={"role": "Papel", "name": "Responsável", "responsibility": "Responsabilidade"}
)
st.dataframe(team_df, use_container_width=True, hide_index=True)

st.divider()

st.info("📈 Resultados de pilotos e testes já encerrados agora estão na página **Testes e Resultados**.")

with st.expander("OKR da iniciativa (PUDMA)"):
    st.markdown("**Problema**")
    st.write(initiative["okr"]["problem"])
    st.markdown("**Usuários**")
    for u in initiative["okr"]["users"]:
        st.markdown(f"- {u}")
    st.markdown("**Decisões suportadas**")
    for d in initiative["okr"]["decisions"]:
        st.markdown(f"- {d}")
    st.markdown("**Key Results**")
    kr_df = pd.DataFrame(initiative["okr"]["key_results"])
    kr_df = kr_df.rename(
        columns={"kr": "Key Result", "baseline": "Baseline", "target": "Meta", "deadline": "Prazo"}
    )
    st.dataframe(kr_df, use_container_width=True, hide_index=True)

with st.expander("Glossário"):
    glossary_df = pd.DataFrame(initiative["glossary"])
    glossary_df = glossary_df.rename(columns={"term": "Termo", "definition": "Definição"})
    st.dataframe(glossary_df, use_container_width=True, hide_index=True)

if initiative.get("data_catalog_url"):
    st.caption(
        f"📖 **Dicionário de dados completo (domínio Vendas):** "
        f"[abrir Pepeye Data Catalog ↗]({initiative['data_catalog_url']})"
    )

st.divider()

st.subheader("Evolução do portfólio")
st.caption("Fonte: planilha mestre de iniciativas Sales ADAN 2026-2027")

roadmap_df = pd.DataFrame(roadmap)
roadmap_df = roadmap_df[["name", "data_product_type", "duration"]].rename(
    columns={
        "name": "Iniciativa",
        "data_product_type": "Tipo de produto de dados",
        "duration": "Duração",
    }
)
st.dataframe(roadmap_df, use_container_width=True, hide_index=True)
