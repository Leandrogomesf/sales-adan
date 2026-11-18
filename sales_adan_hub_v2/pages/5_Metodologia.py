import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st

from components.kpi_card import kpi_card
from components.metrics import bullet_list
from components.roadmap import render_roadmap_banner
from components.status import PHASE_COLORS, PHASE_LABELS, PHASE_ORDER
from services.catalog_service import load_methodology

render_roadmap_banner()

methodology = load_methodology()

st.title("Metodologia Sales ADAN")
st.caption(methodology["intro"])

st.divider()

# ---------------------------------------------------------------------------
# Bloco 1 — PepOne x ADAN
# ---------------------------------------------------------------------------
st.header("1. PepOne × ADAN — governança da demanda")
pepone = methodology["pepone"]
st.write(pepone["description"])

st.markdown("**Etapas do PepOne**")
stage_cols = st.columns(len(pepone["stages"]))
for col, stage in zip(stage_cols, pepone["stages"]):
    with col:
        with st.container(border=True):
            st.markdown(f"**{stage['name']}**")
            st.caption(stage["description"])

st.markdown("**Mapeamento PepOne × fase ADAN**")
mapping_df = pd.DataFrame(pepone["mapping"])
mapping_df["adan_phase"] = mapping_df["adan_phase"].map(PHASE_LABELS)
mapping_df = mapping_df.rename(
    columns={
        "adan_phase": "Fase ADAN",
        "pepone_stages": "Etapas PepOne ativas",
        "what_happens": "O que acontece",
    }
)
st.dataframe(mapping_df, use_container_width=True, hide_index=True)

st.info(f"⚠️ {pepone['discovery_warning']}")

with st.expander("Taxonomia de tipos de item"):
    types_df = pd.DataFrame(pepone["item_types"]).rename(
        columns={"tag": "Tipo", "when_used": "Quando usar"}
    )
    st.dataframe(types_df, use_container_width=True, hide_index=True)

st.caption(f"🗂️ {pepone['tracking_tool']}")

st.divider()

# ---------------------------------------------------------------------------
# Bloco 2 — Ciclo de Vida do Produto
# ---------------------------------------------------------------------------
st.header("2. Ciclo de Vida do Produto")
lifecycle = methodology["product_lifecycle"]
st.write(lifecycle["description"])

products_by_stage = {row["stage"]: row["products"] for row in lifecycle["products_by_stage"]}

stage_cols = st.columns(len(lifecycle["stages"]))
for col, stage in zip(stage_cols, lifecycle["stages"]):
    with col:
        with st.container(border=True):
            st.markdown(
                f"<div style='color:{stage['color']};font-weight:700;'>{stage['name']}</div>",
                unsafe_allow_html=True,
            )
            st.caption(stage["description"])
            products = products_by_stage.get(stage["name"], [])
            if products:
                bullet_list(products)
            else:
                st.caption("Nenhum produto nesta fase.")

st.caption(f"ℹ️ {lifecycle['decline_note']}")

st.divider()

# ---------------------------------------------------------------------------
# Bloco 3 — Ciclo de Desenvolvimento de Produto de Dados com ML
# ---------------------------------------------------------------------------
st.header("3. Ciclo de Desenvolvimento de Produto de Dados com ML")
adan = methodology["adan_cycle"]
st.write(adan["description"])

big_cols = st.columns(len(adan["big_numbers"]))
BIG_NUMBER_STYLE = ["brand", "accent", "orange"]
for i, (col, stat) in enumerate(zip(big_cols, adan["big_numbers"])):
    with col:
        kpi_card("📌", stat["label"], stat["value"], BIG_NUMBER_STYLE[i % len(BIG_NUMBER_STYLE)])

st.markdown("**Macro-divisão**")
macro_cols = st.columns(len(adan["macro_groups"]))
for col, group in zip(macro_cols, adan["macro_groups"]):
    with col:
        with st.container(border=True):
            st.markdown(f"**{group['name']}**")
            st.caption(group["phases"])
            st.write(f"{group['duration_sprints']} · {group['duration_months']}")

st.markdown("**As 6 fases**")

phase_tabs = st.tabs([PHASE_LABELS[p["id"]] for p in adan["phases"]])
for tab, phase in zip(phase_tabs, adan["phases"]):
    with tab:
        color = PHASE_COLORS.get(phase["id"], "#9CA3AF")
        st.markdown(
            f"<span style='background-color:{color}22;color:{color};border:1px solid {color};"
            f"border-radius:999px;padding:2px 10px;font-size:0.8rem;font-weight:600;'>"
            f"{PHASE_LABELS[phase['id']]}</span> &nbsp; **Duração:** {phase['duration']}",
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Características**")
            bullet_list(phase["characteristics"])
            st.markdown("**Pré-requisitos**")
            bullet_list(phase["prerequisites"])
        with col_b:
            st.markdown("**Outputs**")
            bullet_list(phase["outputs"])
            st.markdown("**Responsabilidades**")
            for resp in phase["responsibilities"]:
                st.markdown(f"- **{resp['role']}**: {resp['detail']}")

        if phase.get("gate"):
            st.success(
                f"**Gate:** {phase['gate']}  \n"
                f"✅ Sim → {phase['gate_yes']}   ·   ❌ Não → {phase['gate_no']}"
            )
        else:
            st.caption("Fase final — sem gate de saída, operação contínua.")

with st.expander("Glossário de funções"):
    role_df = pd.DataFrame(adan["role_glossary"]).rename(columns={"role": "Sigla", "meaning": "Significado"})
    st.dataframe(role_df, use_container_width=True, hide_index=True)
