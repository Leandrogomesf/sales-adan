import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from components.metrics import bullet_list, columns_table, dot_rating, metric_block, tables_table
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

registered_model = algorithm.get("registered_model")
if registered_model:
    versions = " · ".join(
        f"{label} v{registered_model[key]}"
        for label, key in (("champion", "champion_version"), ("challenger", "challenger_version"), ("latest", "latest_version"))
        if registered_model.get(key) is not None
    )
    st.caption(f"**Modelo registrado:** `{registered_model['unity_catalog_path']}` — {versions}")

if product.get("dashboard_url"):
    st.caption(f"**Dashboard do produto:** [abrir ↗]({product['dashboard_url']})")

product_tables = product.get("tables", [])
if product_tables and product_tables[0] not in ("Não Disponível", "Não disponível"):
    with st.expander(f"📋 Tabelas geradas pelo produto ({len(product_tables)})"):
        tables_table(product_tables)

personas = algorithm.get("personas")
if personas:
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    persona_names = {p["cluster"]: p["name"] for p in personas}
    persona_tab_labels = ["📊 Visão Geral"] + [p["name"] for p in personas]
    persona_tabs = st.tabs(persona_tab_labels)

    with persona_tabs[0]:
        overview_path = assets_dir / algorithm["overview_image"]
        if overview_path.exists():
            st.image(str(overview_path))
        st.markdown("**Resumo das 5 personas**")
        summary_rows = [
            {
                "Persona": p["name"],
                "% Clientes": p["share_of_customers"],
                "Ticket médio anual": p["avg_annual_ticket"],
                "% Net Sales": p["net_sales_share"],
                "Principal tipo de PDV": p["main_pdv_type"],
                "Tipo de rota": p["route_type"],
            }
            for p in personas
        ]
        columns_table(summary_rows)

    for persona, tab in zip(personas, persona_tabs[1:]):
        with tab:
            avatar_col, info_col = st.columns([1, 3])
            with avatar_col:
                avatar_path = assets_dir / persona["avatar"]
                if avatar_path.exists():
                    st.image(str(avatar_path))
            with info_col:
                st.subheader(persona["name"])
                m1, m2, m3 = st.columns(3)
                m1.metric("% Clientes", persona["share_of_customers"])
                m2.metric("Ticket médio anual", persona["avg_annual_ticket"])
                m3.metric("% Net Sales", persona["net_sales_share"])

            with st.container(border=True):
                st.markdown("**Sobre esta persona**")
                st.write(persona["description"])

            with st.container(border=True):
                st.markdown("**Desempenho**")
                ratings = persona["ratings"]
                half = (len(ratings) + 1) // 2
                rating_col_a, rating_col_b = st.columns(2)
                for col, chunk in ((rating_col_a, ratings[:half]), (rating_col_b, ratings[half:])):
                    with col:
                        for rating in chunk:
                            st.markdown(f"{rating['label']}  \n{dot_rating(rating['value'])}")

            with st.container(border=True):
                st.markdown("**Mix de marcas (top 4)**")
                for brand_line in persona["brand_mix"]:
                    name, _, pct = brand_line.rpartition(" ")
                    pct_value = pct.replace("%", "").strip()
                    st.caption(f"{name} — {pct}")
                    try:
                        st.progress(min(int(float(pct_value)), 100) / 100)
                    except ValueError:
                        pass

            col_pdv, col_route = st.columns(2)
            with col_pdv:
                with st.container(border=True):
                    st.markdown("**Principal tipo de PDV**")
                    st.write(persona["main_pdv_type"])
            with col_route:
                with st.container(border=True):
                    st.markdown("**Tipo de rota**")
                    st.write(persona["route_type"])

            with st.container(border=True):
                st.markdown("**Características**")
                bullet_list(persona["traits"])

            card_path = assets_dir / persona["card_image"]
            if card_path.exists():
                with open(card_path, "rb") as f:
                    st.download_button(
                        f"🖼️ Baixar card completo de {persona['name']} (imagem)",
                        data=f.read(),
                        file_name=card_path.name,
                        mime="image/jpeg",
                        key=f"download_card_{persona['cluster']}",
                    )

    reference_doc = algorithm.get("reference_doc")
    if reference_doc:
        doc_path = assets_dir / reference_doc
        if doc_path.exists():
            with open(doc_path, "rb") as f:
                st.download_button(
                    "📄 Baixar material completo de Personas (PDF)",
                    data=f.read(),
                    file_name=doc_path.name,
                    mime="application/pdf",
                )

    st.divider()

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
    if tech.get("model_diagram"):
        diagram_path = Path(__file__).resolve().parent.parent / "assets" / tech["model_diagram"]
        if diagram_path.exists():
            st.image(str(diagram_path))
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
    if out.get("schema_refreshed_at"):
        st.caption(f"Schema atualizado em: {out['schema_refreshed_at']}")
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
