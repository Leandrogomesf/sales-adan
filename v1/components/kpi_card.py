import streamlit as st

ICON_COLORS = {
    "brand": ("#2563eb", "#eaf1ff"),
    "accent": ("#6d5efc", "#f1effe"),
    "green": ("#16a34a", "#ecfdf3"),
    "orange": ("#ea580c", "#fff3ea"),
}

_STYLE_INJECTED_KEY = "_kpi_card_style_injected"

_STYLE = """
<style>
.adan-kpi-card {
    background-color: #ffffff;
    border: 1px solid #eceef1;
    border-radius: 16px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 1px 1px rgba(0,0,0,0.03);
    padding: 20px;
    min-height: 168px;
    display: flex;
    flex-direction: column;
}
.adan-icon-badge {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 10px;
}
.adan-kpi-label {
    font-size: 0.82rem;
    color: #6b7280;
    font-weight: 500;
    margin-bottom: 4px;
}
.adan-kpi-value {
    font-size: 1.05rem;
    color: #1a1a1e;
    font-weight: 700;
    letter-spacing: -0.2px;
    line-height: 1.4;
}
</style>
"""


def kpi_card(icon: str, label: str, value: str, color: str = "brand"):
    if not st.session_state.get(_STYLE_INJECTED_KEY):
        st.markdown(_STYLE, unsafe_allow_html=True)
        st.session_state[_STYLE_INJECTED_KEY] = True

    icon_color, icon_bg = ICON_COLORS.get(color, ICON_COLORS["brand"])
    st.markdown(
        f"""
        <div class="adan-kpi-card">
            <div class="adan-icon-badge" style="background-color:{icon_bg};color:{icon_color};">
                {icon}
            </div>
            <div class="adan-kpi-label">{label}</div>
            <div class="adan-kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
