PHASE_ORDER = ["discovery", "explore", "poc", "pilot", "mvp", "sustain"]

PHASE_LABELS = {
    "discovery": "Discovery",
    "explore": "Explore",
    "poc": "PoC",
    "pilot": "Pilot",
    "mvp": "MVP",
    "sustain": "Sustain",
}

PHASE_COLORS = {
    "discovery": "#9CA3AF",
    "explore": "#60A5FA",
    "poc": "#FBBF24",
    "pilot": "#FB923C",
    "mvp": "#34D399",
    "sustain": "#10B981",
}


def phase_badge_html(phase: str) -> str:
    label = PHASE_LABELS.get(phase, phase)
    color = PHASE_COLORS.get(phase, "#9CA3AF")
    return (
        f'<span style="background-color:{color}22;color:{color};'
        f'border:1px solid {color};border-radius:999px;padding:2px 10px;'
        f'font-size:0.8rem;font-weight:600;white-space:nowrap;">{label}</span>'
    )


def phase_progress(phase: str) -> float:
    if phase not in PHASE_ORDER:
        return 0.0
    return (PHASE_ORDER.index(phase) + 1) / len(PHASE_ORDER)


def secondary_tag_html(tag: str) -> str:
    return (
        '<span style="background-color:#E5E7EB;color:#374151;'
        "border-radius:999px;padding:2px 10px;font-size:0.75rem;"
        f'font-weight:500;white-space:nowrap;margin-left:6px;">{tag}</span>'
    )


def phase_legend_html() -> str:
    """Legenda de cores das fases ADAN, para contextualizar badges e barras de progresso."""
    chips = "".join(
        f'<span style="display:inline-flex;align-items:center;margin-right:14px;'
        f'font-size:0.8rem;color:#374151;">'
        f'<span style="width:10px;height:10px;border-radius:50%;background-color:{PHASE_COLORS[p]};'
        f'display:inline-block;margin-right:5px;"></span>{PHASE_LABELS[p]}</span>'
        for p in PHASE_ORDER
    )
    return f'<div style="margin:4px 0 12px 0;">{chips}</div>'
