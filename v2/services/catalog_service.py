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


@st.cache_data
def load_algorithms() -> list[dict]:
    return _load_yaml("algorithms.yaml")["algorithms"]


@st.cache_data
def load_roadmap_phases() -> dict:
    return _load_yaml("roadmap_phases.yaml")


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
