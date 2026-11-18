import streamlit as st

ICON_COLORS = {
    "brand": ("#2563eb", "#eaf1ff"),
    "accent": ("#6d5efc", "#f1effe"),
    "green": ("#16a34a", "#ecfdf3"),
    "orange": ("#ea580c", "#fff3ea"),
}

_SVG_WRAPPER = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round">{}</svg>'
)

ICONS = {
    "target": _SVG_WRAPPER.format(
        '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>'
    ),
    "users": _SVG_WRAPPER.format(
        '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
        '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
    ),
    "layers": _SVG_WRAPPER.format(
        '<path d="m12.83 2.18 8.49 4.24a1 1 0 0 1 0 1.79l-8.49 4.25a2 2 0 0 1-1.79 0L2.68 8.21a1 1 0 0 1 0-1.79Z"/>'
        '<path d="m22 12.24-8.83 4.4a2 2 0 0 1-1.79 0L2 12.24"/>'
        '<path d="m22 17.24-8.83 4.4a2 2 0 0 1-1.79 0L2 17.24"/>'
    ),
    "clock": _SVG_WRAPPER.format('<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'),
    "brain": _SVG_WRAPPER.format(
        '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/>'
        '<path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>'
        '<path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/>'
    ),
    "dna": _SVG_WRAPPER.format(
        '<path d="m10 16 1.5 1.5"/><path d="m14 8-1.5-1.5"/><path d="M15 2c-1.798 1.998-2.518 3.995-2.807 5.993"/>'
        '<path d="M9 22c1.798-1.998 2.518-3.995 2.807-5.993"/>'
        '<path d="M7.5 6.5 10 9"/><path d="M16.5 17.5 14 15"/>'
        '<path d="M6.5 8.5h2"/><path d="M15.5 15.5h2"/>'
    ),
    "flask": _SVG_WRAPPER.format(
        '<path d="M9 2v6.5l-5 9A2 2 0 0 0 5.75 21h12.5a2 2 0 0 0 1.75-3.5l-5-9V2"/><path d="M8.5 2h7"/>'
    ),
    "check": _SVG_WRAPPER.format('<path d="M20 6 9 17l-5-5"/>'),
    "pin": _SVG_WRAPPER.format('<path d="M12 17v5"/><path d="M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24V17a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V7a1 1 0 0 1 1-1 2 2 0 0 0 0-4H8a2 2 0 0 0 0 4 1 1 0 0 1 1 1Z"/>'),
    "trending-up": _SVG_WRAPPER.format(
        '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>'
    ),
    "package": _SVG_WRAPPER.format(
        '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>'
        '<path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>'
    ),
    "weight": _SVG_WRAPPER.format(
        '<circle cx="12" cy="5" r="3"/><path d="M6.5 8a2 2 0 0 0-2 1.6l-1.4 7A2 2 0 0 0 5 19h14a2 2 0 0 0 1.9-2.4l-1.4-7A2 2 0 0 0 17.5 8Z"/>'
    ),
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
