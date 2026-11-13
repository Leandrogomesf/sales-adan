import streamlit as st

ICON_COLORS = {
    "brand": ("#2563eb", "#eaf1ff"),
    "accent": ("#6d5efc", "#f1effe"),
    "green": ("#16a34a", "#ecfdf3"),
    "orange": ("#ea580c", "#fff3ea"),
}


def kpi_card(icon: str, label: str, value: str, color: str = "brand"):
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
