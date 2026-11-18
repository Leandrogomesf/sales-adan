import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st

_NUMERIC_RE = re.compile(r"[-+]?\d+(?:\.\d+)?")


def _parse_metric_value(raw: str) -> float | None:
    """Extrai o valor numérico de strings como '+17,5 p.p.' ou '-0,7'."""
    match = _NUMERIC_RE.search(raw.replace(",", "."))
    return float(match.group()) if match else None

from components.kpi_card import ICONS, kpi_card
from components.roadmap import render_roadmap_banner
from services.catalog_service import load_pilot_results

render_roadmap_banner()

st.title("Testes e Resultados")
st.caption(
    "Consolidação dos pilotos e testes já encerrados do Sales ADAN, em ordem cronológica — "
    "indicadores referentes ao período de medição de cada piloto, não ao resultado corrente "
    "da operação."
)

pilots = load_pilot_results()

BIG_NUMBER_STYLE = ["brand", "accent", "orange", "green"]

# Mapeia o conceito do indicador para um ícone próprio (resolve N11 — antes
# todo KPI usava o mesmo 📊 genérico, sem relação com o que estava medindo).
LABEL_ICON_KEYWORDS = [
    (("net sales", "valor incremental"), ICONS["trending-up"]),
    (("volume",), ICONS["weight"]),
    (("oferta", "completude"), ICONS["package"]),
    (("produtividade",), ICONS["clock"]),
    (("loyalty", "divis"), ICONS["layers"]),
    (("adoção",), ICONS["users"]),
]


def _icon_for_label(label: str) -> str:
    label_lower = label.lower()
    for keywords, icon in LABEL_ICON_KEYWORDS:
        if any(k in label_lower for k in keywords):
            return icon
    return ICONS["pin"]


# Fontes legíveis em vez de nomes de arquivo interno (resolve U11).
SOURCE_LABELS = {
    "sales intel/v1/OKR_Sales_Intelligence.md": "OKR do Sales Intelligence (histórico)",
}


def _readable_source(source: str) -> str:
    return SOURCE_LABELS.get(source, source)


for pilot in pilots:
    st.divider()
    with st.container(border=True):
        st.subheader(pilot["title"])
        st.caption(
            f"Período de referência: {pilot['reference_period']} · "
            f"Fonte: {_readable_source(pilot['source'])}"
        )
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
                    kpi_card(_icon_for_label(stat["label"]), stat["label"], value, color)

        if pilot.get("metrics_table"):
            metrics_table = pilot["metrics_table"]

            st.markdown("**Tendência vs. grupo controle**")
            meses_ordenados = pd.CategoricalIndex(
                ["Fev", "Mar", "Abr"], categories=["Fev", "Mar", "Abr"], ordered=True
            )
            trend_df = pd.DataFrame(
                {
                    m["name"]: [
                        _parse_metric_value(m["fev"]),
                        _parse_metric_value(m["mar"]),
                        _parse_metric_value(m["abr"]),
                    ]
                    for m in metrics_table
                },
                index=meses_ordenados,
            )
            st.line_chart(trend_df)
            st.caption("Diferença em pontos percentuais (ou pontos absolutos para SKUs/PDV) vs. grupo controle.")

            st.markdown("**Métricas por mês (detalhe)**")
            df = pd.DataFrame(metrics_table)
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
