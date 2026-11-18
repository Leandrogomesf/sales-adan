import streamlit as st

from components.status import PHASE_LABELS, PHASE_ORDER
from services.catalog_service import get_algorithms_for_product

FILTER_KEYS = ("f_modules", "f_phases", "f_areas", "f_search")


def product_filters(products: list[dict]) -> dict:
    modules = sorted({p.get("module", "—") for p in products})
    phases_presentes = {p["phase"] for p in products}
    phases_ordenadas = [p for p in PHASE_ORDER if p in phases_presentes]
    areas = sorted({a for p in products for a in p.get("consuming_areas", [])})

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_modules = st.multiselect("Módulo", modules, placeholder="Todos", key="f_modules")
    with col2:
        selected_phases = st.multiselect(
            "Fase",
            phases_ordenadas,
            format_func=lambda p: PHASE_LABELS.get(p, p),
            placeholder="Todas",
            key="f_phases",
        )
    with col3:
        selected_areas = st.multiselect("Área consumidora", areas, placeholder="Todas", key="f_areas")

    search = st.text_input(
        "Buscar produto",
        placeholder="Produto, código ou algoritmo (ex.: KMeans)...",
        key="f_search",
    )

    return {
        "modules": selected_modules,
        "phases": selected_phases,
        "areas": selected_areas,
        "search": search.strip().lower(),
    }


def _product_matches_search(product: dict, term: str) -> bool:
    texto = " ".join(
        [
            product["name"],
            product.get("code", ""),
            product.get("description", ""),
            *[a["name"] for a in get_algorithms_for_product(product["id"])],
        ]
    ).lower()
    return term in texto


def apply_product_filters(products: list[dict], filters: dict) -> list[dict]:
    result = products
    if filters["modules"]:
        result = [p for p in result if p.get("module") in filters["modules"]]
    if filters["phases"]:
        result = [p for p in result if p["phase"] in filters["phases"]]
    if filters["areas"]:
        result = [
            p for p in result
            if set(p.get("consuming_areas", [])) & set(filters["areas"])
        ]
    if filters["search"]:
        result = [p for p in result if _product_matches_search(p, filters["search"])]
    return result


def render_clear_filters_button():
    """Botão que limpa os filtros de produtos e força o rerender (resolve A8/N2)."""
    if st.button("Limpar filtros", icon=":material/filter_alt_off:"):
        for key in FILTER_KEYS:
            st.session_state.pop(key, None)
        st.rerun()
