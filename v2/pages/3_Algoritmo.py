import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from components.metrics import bullet_list, columns_table, metric_block
from components.roadmap import render_roadmap_banner
from components.status import phase_badge_html
from services.catalog_service import (
    get_algorithm,
    get_algorithms_for_product,
    get_product,
    load_products,
)

render_roadmap_banner()

st.title("Detalhe do Algoritmo")

products = load_products()
product_names = {p["id"]: p["name"] for p in products}
product_ids = list(product_names.keys())

current_product_id = st.session_state.get("selected_product")
if current_product_id not in product_ids:
    current_product_id = product_ids[0]

sel_col1, sel_col2 = st.columns(2)
with sel_col1:
    chosen_product_id = st.selectbox(
        "Produto",
        options=product_ids,
        format_func=lambda pid: product_names[pid],
        index=product_ids.index(current_product_id),
    )

if chosen_product_id != current_product_id:
    st.session_state["selected_algorithm"] = None

st.session_state["selected_product"] = chosen_product_id
product = get_product(chosen_product_id)

algorithms = get_algorithms_for_product(chosen_product_id)

if not algorithms:
    with sel_col2:
        st.selectbox("Algoritmo", options=["Nenhum algoritmo documentado"], disabled=True)
    st.caption(f"Produtos > {product['name']}")
    st.warning("Nenhum algoritmo documentado para este produto ainda.")
    st.stop()

algo_names = {a["id"]: a["name"] for a in algorithms}
algo_ids = list(algo_names.keys())
current_algorithm_id = st.session_state.get("selected_algorithm")
if current_algorithm_id not in algo_ids:
    current_algorithm_id = algo_ids[0]

with sel_col2:
    chosen_algorithm_id = st.selectbox(
        "Algoritmo",
        options=algo_ids,
        format_func=lambda aid: algo_names[aid],
        index=algo_ids.index(current_algorithm_id),
    )

st.session_state["selected_algorithm"] = chosen_algorithm_id

st.caption(f"Produtos > {product['name']} > {algo_names[chosen_algorithm_id]}")

algorithm = get_algorithm(chosen_algorithm_id)

st.divider()

header_col, badge_col = st.columns([3, 1])
with header_col:
    st.header(algorithm["name"])
    st.caption(f"Produto: {product['name']}")
with badge_col:
    st.markdown(phase_badge_html(algorithm["phase"]), unsafe_allow_html=True)
    st.caption(algorithm.get("status", ""))

meta_col1, meta_col2 = st.columns(2)
with meta_col1:
    st.caption(f"**Última execução:** {algorithm.get('last_run', 'Não disponível')}")
with meta_col2:
    st.caption(f"**Último treinamento:** {algorithm.get('last_training', 'Não disponível')}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Visão funcional",
        "Funcionamento técnico",
        "Tabela gerada",
        "Métricas técnicas",
        "Valor para o negócio",
    ]
)

with tab1:
    func = algorithm["functional"]
    st.markdown("**Problema resolvido**")
    st.write(func["problem_solved"])
    st.markdown("**Decisão suportada**")
    st.write(func["decision_supported"])
    st.markdown("**Usuários**")
    bullet_list(func["users"])
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Granularidade**")
        st.write(func["granularity"])
    with col_b:
        st.markdown("**Frequência de atualização**")
        st.write(func["update_frequency"])
    st.markdown("**Explicação não técnica**")
    st.info(func["plain_explanation"])
    st.markdown("**Limitações conhecidas**")
    st.warning(func["known_limitations"])

with tab2:
    tech = algorithm["technical"]
    st.markdown("**Pipeline**")
    st.code(tech["pipeline"], language=None)
    st.markdown("**Algoritmo / Modelo**")
    st.write(tech["model"])
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Target**")
        st.write(tech["target"])
        st.markdown("**Janela de observação**")
        st.write(tech["observation_window"])
        st.markdown("**Estratégia de validação**")
        st.write(tech["validation_strategy"])
    with col_b:
        st.markdown("**Janela de previsão**")
        st.write(tech["prediction_window"])
        st.markdown("**Método de calibração**")
        st.write(tech["calibration_method"])
        st.markdown("**Periodicidade de retraining**")
        st.write(tech["retraining_frequency"])
    st.markdown("**Features principais**")
    bullet_list(tech["main_features"])
    st.markdown("**Regras de pós-processamento**")
    st.write(tech["postprocessing_rules"])

with tab3:
    out = algorithm["output_table"]
    st.markdown(f"**Tabela:** `{out['name']}`")
    st.caption(f"Caminho Unity Catalog: {out['unity_catalog_path']}")
    st.caption("Exemplos abaixo são sintéticos/mascarados — não representam dados reais de cliente.")
    columns_table(out["columns"])

with tab4:
    metrics = algorithm["technical_metrics"]
    col_a, col_b = st.columns(2)
    with col_a:
        metric_block("Performance do modelo", metrics["model_performance"])
        st.markdown("**Cobertura**")
        st.write(metrics["coverage"])
    with col_b:
        st.markdown("**Qualidade operacional**")
        st.write(metrics["operational_quality"])
        st.markdown("**Drift e estabilidade**")
        st.write(metrics["drift_stability"])

with tab5:
    value = algorithm["business_value"]
    st.info(value["note"])
    st.markdown("**Métricas de valor acompanhadas**")
    bullet_list(value["metrics"])
