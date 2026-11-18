from pathlib import Path

import streamlit as st
import yaml

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
    return _load_yaml("roadmap.yaml")["initiatives"]


@st.cache_data
def load_products() -> list[dict]:
    return _load_yaml("products.yaml")["products"]


def _apply_live_metadata(algorithms: list[dict]) -> list[dict]:
    """Sobrepõe os campos gerados por scripts/refresh_algorithms_metadata.py."""
    live_path = DATA_DIR / "algorithms_live.yaml"
    if not live_path.exists():
        return algorithms
    live = (_load_yaml("algorithms_live.yaml") or {}).get("algorithms", {})
    for algo in algorithms:
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
    return algorithms


@st.cache_data
def load_algorithms() -> list[dict]:
    return _apply_live_metadata(_load_yaml("algorithms.yaml")["algorithms"])


@st.cache_data
def load_roadmap_phases() -> dict:
    return _load_yaml("roadmap_phases.yaml")


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
