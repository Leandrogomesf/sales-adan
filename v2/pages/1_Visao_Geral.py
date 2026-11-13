import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st

from components.kpi_card import kpi_card
from components.roadmap import render_roadmap_banner
from components.status import phase_badge_html
from services.catalog_service import load_initiative, load_roadmap

initiative = load_initiative()
roadmap = load_roadmap()

render_roadmap_banner()

st.title(initiative["name"])
st.caption(initiative["tagline"])
st.caption(f"Última atualização: {initiative['last_updated']}")

st.divider()

st.subheader("Visão executiva")

KPI_STYLE = {
    "Objetivo": ("🎯", "brand"),
    "Público impactado": ("👥", "accent"),
    "Produtos ativos": ("🧩", "green"),
    "Última atualização": ("🕒", "orange"),
}

cols = st.columns(len(initiative["executive_cards"]))
for col, card in zip(cols, initiative["executive_cards"]):
    icon, color = KPI_STYLE.get(card["label"], ("📌", "brand"))
    with col:
        kpi_card(icon, card["label"], card["value"], color)

st.divider()

st.subheader("Objetivo da iniciativa")
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

st.subheader(initiative["pilot_results"]["title"])
st.caption(
    f"Período de referência: {initiative['pilot_results']['reference_period']} · "
    f"Fonte: {initiative['pilot_results']['source']}"
)
st.warning(initiative["pilot_results"]["note"])
pilot_df = pd.DataFrame(initiative["pilot_results"]["metrics"])
pilot_df = pilot_df.rename(
    columns={
        "name": "Métrica",
        "fev": "Fev",
        "mar": "Mar",
        "abr": "Abr",
        "trend": "Tendência",
    }
)
st.dataframe(pilot_df, use_container_width=True, hide_index=True)

st.divider()

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

st.divider()

st.subheader("Evolução do portfólio")
st.caption("Fonte: planilha mestre de iniciativas Sales ADAN 2026-2027")

col_f1, col_f2 = st.columns(2)
with col_f1:
    only_prioritized = st.checkbox("Mostrar apenas priorizadas no EDF", value=False)
with col_f2:
    only_with_detail = st.checkbox("Mostrar apenas com página de detalhe", value=False)

filtered_roadmap = roadmap
if only_prioritized:
    filtered_roadmap = [i for i in filtered_roadmap if i["prioritized_in_edf"]]
if only_with_detail:
    filtered_roadmap = [i for i in filtered_roadmap if i["product_id"]]

roadmap_df = pd.DataFrame(filtered_roadmap)
roadmap_df["prioritized_in_edf"] = roadmap_df["prioritized_in_edf"].map(
    {True: "Sim", False: "Não"}
)
roadmap_df = roadmap_df[
    ["name", "data_product_type", "focal_point", "origin", "duration", "prioritized_in_edf"]
].rename(
    columns={
        "name": "Iniciativa",
        "data_product_type": "Tipo de produto de dados",
        "focal_point": "Ponto focal",
        "origin": "Origem",
        "duration": "Duração",
        "prioritized_in_edf": "Priorizado no EDF",
    }
)
st.dataframe(roadmap_df, use_container_width=True, hide_index=True)
st.caption(
    f"{len(filtered_roadmap)} de {len(roadmap)} iniciativas exibidas. "
    "Iniciativas sem página de detalhe aparecem apenas aqui (roadmap/conceito)."
)
