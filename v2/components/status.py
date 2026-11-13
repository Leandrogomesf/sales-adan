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
        f'<span class="adan-badge" style="background-color:{color}22;'
        f'color:{color};border:1px solid {color};">{label}</span>'
    )


def phase_progress(phase: str) -> float:
    if phase not in PHASE_ORDER:
        return 0.0
    return (PHASE_ORDER.index(phase) + 1) / len(PHASE_ORDER)


def secondary_tag_html(tag: str) -> str:
    return f'<span class="adan-badge-secondary">{tag}</span>'
