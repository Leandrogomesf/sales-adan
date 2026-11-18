from pathlib import Path

import streamlit as st
import yaml

from components.status import PHASE_ORDER

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_yaml(filename: str) -> dict:
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@st.cache_data
def load_initiative() -> dict:
    return _load_yaml("initiative.yaml")


@st.cache_data
def load_roadmap() -> list[dict]:
    """Lista mestre de iniciativas planejadas (produtos futuros, sem página de detalhe ainda)."""
    return _load_yaml("roadmap.yaml")["initiatives"]


@st.cache_data
def load_portfolio() -> dict:
    """Fonte única de verdade: produtos e algoritmos consolidados em um só documento.

    Elimina as divergências de fase/status entre catálogo, detalhe e roadmap
    que existiam na v1 (ver auditoria — achados A1, A2, A3).
    """
    return _load_yaml("portfolio.yaml")


def _apply_live_metadata(products: list[dict]) -> list[dict]:
    """Sobrepõe os campos gerados por scripts/refresh_algorithms_metadata.py."""
    live_path = DATA_DIR / "algorithms_live.yaml"
    if not live_path.exists():
        return products
    live = (_load_yaml("algorithms_live.yaml") or {}).get("algorithms", {})
    for product in products:
        for algo in product.get("algorithms", []):
            entry = live.get(algo["id"])
            if not entry:
                continue
            for key in ("last_run", "last_training"):
                if entry.get(key):
                    algo[key] = entry[key]
            if entry.get("registered_model"):
                algo["registered_model"] = {**algo.get("registered_model", {}), **entry["registered_model"]}
            live_out = entry.get("output_table") or {}
            if live_out.get("columns"):
                algo.setdefault("output_table", {})
                algo["output_table"]["columns"] = live_out["columns"]
                algo["output_table"]["schema_refreshed_at"] = live_out.get("schema_refreshed_at")
    return products


@st.cache_data
def load_products() -> list[dict]:
    """Produtos do portfólio, no formato plano usado pelas páginas (phase + status únicos)."""
    products = _apply_live_metadata(load_portfolio()["products"])
    return [
        {
            **{k: v for k, v in p.items() if k != "algorithms"},
            "status": p["operational_status"],
        }
        for p in products
    ]


@st.cache_data
def load_algorithms() -> list[dict]:
    """Algoritmos "achatados" (um nível acima dos produtos), no formato plano usado pelas páginas."""
    algorithms = []
    for product in _apply_live_metadata(load_portfolio()["products"]):
        for algo in product.get("algorithms", []):
            algorithms.append({
                **algo,
                "product_id": product["id"],
                "phase": product["phase"],
                "status": algo["operational_status"],
            })
    return algorithms


@st.cache_data
def load_pilot_results() -> list[dict]:
    return _load_yaml("pilot_results.yaml")["pilots"]


@st.cache_data
def load_methodology() -> dict:
    return _load_yaml("methodology.yaml")


def get_product(product_id: str) -> dict | None:
    for product in load_products():
        if product["id"] == product_id:
            return product
    return None


def get_algorithm(algorithm_id: str) -> dict | None:
    for algo in load_algorithms():
        if algo["id"] == algorithm_id:
            return algo
    return None


def get_algorithms_for_product(product_id: str) -> list[dict]:
    return [a for a in load_algorithms() if a["product_id"] == product_id]


def count_active_products() -> int:
    """Produtos fora de Sustain — 'ativos em desenvolvimento'. Calculado, nunca digitado à mão."""
    return sum(1 for p in load_products() if p["phase"] != "sustain")


def count_algorithms() -> int:
    """Total de algoritmos no portfólio, somando os de todos os produtos."""
    return len(load_algorithms())


def count_products_by_phase() -> dict:
    """Quantos produtos existem em cada fase ADAN, na ordem de PHASE_ORDER."""
    products = load_products()
    return {phase: sum(1 for p in products if p["phase"] == phase) for phase in PHASE_ORDER}
