import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st

from components.kpi_card import kpi_card
from components.roadmap import render_roadmap_banner
from services.catalog_service import load_pilot_results

render_roadmap_banner()

st.title("Testes e Resultados")
st.caption(
    "Consolidação dos pilotos e testes já encerrados do Sales ADAN — indicadores "
    "referentes ao período de medição de cada piloto, não ao resultado corrente da operação."
)

pilots = load_pilot_results()

BIG_NUMBER_STYLE = ["brand", "accent", "orange", "green"]

for pilot in pilots:
    st.divider()
    with st.container(border=True):
        st.subheader(pilot["title"])
        st.caption(f"Período de referência: {pilot['reference_period']} · Fonte: {pilot['source']}")
        st.warning(pilot["note"])

        if pilot.get("big_numbers"):
            big_numbers = pilot["big_numbers"]
            cols = st.columns(min(len(big_numbers), 3))
            for i, stat in enumerate(big_numbers):
                color = BIG_NUMBER_STYLE[i % len(BIG_NUMBER_STYLE)]
                value = stat["value"]
                if stat.get("secondary"):
                    value = f"{value}  \n{stat['secondary']}"
                with cols[i % len(cols)]:
                    kpi_card("📊", stat["label"], value, color)

        if pilot.get("metrics_table"):
            st.markdown("**Métricas por mês**")
            df = pd.DataFrame(pilot["metrics_table"])
            df = df.rename(
                columns={
                    "name": "Métrica",
                    "fev": "Fev",
                    "mar": "Mar",
                    "abr": "Abr",
                    "trend": "Tendência",
                }
            )
            st.dataframe(df, use_container_width=True, hide_index=True)

        if pilot.get("divisions_table"):
            st.markdown("**Performance por divisão**")
            df = pd.DataFrame(pilot["divisions_table"])
            df = df.rename(
                columns={
                    "division": "Divisão",
                    "net_sales_var_pct": "Var. Net Sales (teste)",
                    "net_sales_var_control_pct": "Var. Net Sales (controle)",
                    "incremental_ns_growth_pct": "Crescimento incremental NS (%)",
                    "incremental_ns_growth_value": "Crescimento incremental NS (R$)",
                }
            )
            st.dataframe(df, use_container_width=True, hide_index=True)
