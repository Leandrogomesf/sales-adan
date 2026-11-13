import pandas as pd
import streamlit as st


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
