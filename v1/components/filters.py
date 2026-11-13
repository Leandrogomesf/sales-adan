import streamlit as st


def product_filters(products: list[dict]) -> dict:
    modules = sorted({p.get("module", "—") for p in products})
    phases = sorted({p["phase"] for p in products})
    areas = sorted({a for p in products for a in p.get("consuming_areas", [])})

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_modules = st.multiselect("Módulo", modules)
    with col2:
        selected_phases = st.multiselect("Fase", phases)
    with col3:
        selected_areas = st.multiselect("Área consumidora", areas)

    search = st.text_input("Buscar produto", placeholder="Nome do produto ou algoritmo...")

    return {
        "modules": selected_modules,
        "phases": selected_phases,
        "areas": selected_areas,
        "search": search.strip().lower(),
    }


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
        term = filters["search"]
        result = [
            p for p in result
            if term in p["name"].lower() or term in p.get("description", "").lower()
        ]
    return result
