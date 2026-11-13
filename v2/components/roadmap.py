import streamlit as st

from components.status import PHASE_COLORS
from services.catalog_service import load_roadmap_phases

MONTH_LABELS = {
    "01": "Jan", "02": "Fev", "03": "Mar", "04": "Abr",
    "05": "Mai", "06": "Jun", "07": "Jul", "08": "Ago",
    "09": "Set", "10": "Out", "11": "Nov", "12": "Dez",
}


def _format_start_date(start_date: str) -> str:
    year, month = start_date.split("-")
    return f"{MONTH_LABELS.get(month, month)}/{year[2:]}"


def render_roadmap_banner():
    data = load_roadmap_phases()
    phase_order = data["phase_order"]
    phase_labels = data["phase_labels"]
    items = data["items"]

    with st.expander("🗺️ Roadmap de maturidade do portfólio", expanded=False):
        cols = st.columns(len(phase_order))
        for col, phase in zip(cols, phase_order):
            color = PHASE_COLORS.get(phase, "#9CA3AF")
            phase_items = [i for i in items if i["phase"] == phase]
            with col:
                st.markdown(
                    f'<div style="border-top:3px solid {color};padding-top:6px;">'
                    f'<strong>{phase_labels[phase]}</strong></div>',
                    unsafe_allow_html=True,
                )
                for item in sorted(phase_items, key=lambda i: i["start_date"]):
                    st.caption(f"{item['name']} · {_format_start_date(item['start_date'])}")
