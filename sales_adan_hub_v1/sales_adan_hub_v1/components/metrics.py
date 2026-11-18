import re

import pandas as pd
import streamlit as st

_TABLE_ENTRY_RE = re.compile(r"^(.*?)\s*\((.+)\)$")


def bullet_list(items: list[str]):
    for item in items:
        st.markdown(f"- {item}")


def key_value_table(rows: list[dict], columns: list[str]):
    df = pd.DataFrame(rows)
    if columns:
        df = df[columns]
    st.dataframe(df, use_container_width=True, hide_index=True)


def columns_table(columns: list[dict]):
    if not columns:
        st.info("Nenhuma coluna documentada para esta tabela.")
        return
    df = pd.DataFrame(columns)
    df = df.rename(
        columns={
            "name": "Coluna",
            "type": "Tipo",
            "description": "Descrição",
            "example": "Exemplo (sintético)",
        }
    )
    st.dataframe(df, use_container_width=True, hide_index=True)


def metric_block(title: str, values: list[str]):
    st.markdown(f"**{title}**")
    bullet_list(values)


def dot_rating(value: int, max_value: int = 5) -> str:
    filled = "●" * value
    empty = "○" * max(max_value - value, 0)
    return filled + empty


def parse_table_entries(tables: list[str]) -> list[dict]:
    """Separa strings "Nome (caminho.unity.catalog)" em {name, path}."""
    entries = []
    for raw in tables:
        match = _TABLE_ENTRY_RE.match(raw.strip())
        if match:
            entries.append({"name": match.group(1).strip(), "path": match.group(2).strip()})
        else:
            entries.append({"name": raw.strip(), "path": ""})
    return entries


def tables_table(tables: list[str]):
    entries = parse_table_entries(tables)
    df = pd.DataFrame(entries).rename(columns={"name": "Nome", "path": "Caminho Unity Catalog"})
    st.dataframe(df, use_container_width=True, hide_index=True)
