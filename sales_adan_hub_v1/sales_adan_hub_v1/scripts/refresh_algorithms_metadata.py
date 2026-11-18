"""
Atualiza os metadados "vivos" dos algoritmos do Sales ADAN Hub a partir do Unity Catalog.

Para cada algoritmo de data/algorithms.yaml que tenha `output_table.unity_catalog_path`
e/ou `registered_model.unity_catalog_path`, o script busca:
  * schema mais recente da tabela de output (colunas e tipos do UC);
  * data de execução mais recente (MAX de `output_table.execution_date_column`;
    se a coluna for null, usa a última escrita registrada no histórico Delta);
  * versões do modelo registrado (champion, challenger, latest) e a data de
    criação da versão champion (último treinamento).

O resultado é gravado em data/algorithms_live.yaml. O algorithms.yaml curado não é
alterado: services/catalog_service.py sobrepõe os campos vivos na leitura.
Descrições e exemplos das colunas são mantidos do YAML curado quando a coluna já
existe; colunas novas recebem o comentário do UC como descrição.

Execução: rodar no Databricks (serverless ou cluster), como notebook ou tarefa
"Python script" de um Job. Depois, faça o redeploy do app para publicar o arquivo.
"""

from __future__ import annotations

import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml
from databricks.sdk import WorkspaceClient
from pyspark.sql import SparkSession

WRITE_OPERATIONS = {
    "WRITE",
    "CREATE TABLE AS SELECT",
    "CREATE OR REPLACE TABLE AS SELECT",
    "REPLACE TABLE AS SELECT",
    "MERGE",
    "UPDATE",
    "DELETE",
    "STREAMING UPDATE",
    "COPY INTO",
}
_FQN_RE = re.compile(r"^[A-Za-z0-9_]+\.[A-Za-z0-9_]+\.[A-Za-z0-9_]+$")
_COL_RE = re.compile(r"^[A-Za-z0-9_]+$")


def _default_data_dir() -> Path:
    try:
        return Path(__file__).resolve().parent.parent / "data"
    except NameError:  # executado via exec()/notebook, sem __file__
        raise RuntimeError(
            "Não foi possível determinar a pasta data/ automaticamente "
            "(__file__ indisponível, ex.: execução via notebook/exec). "
            "Chame main(data_dir=Path('/caminho/absoluto/para/data')) explicitamente."
        )


def _is_uc_path(value) -> bool:
    return isinstance(value, str) and bool(_FQN_RE.match(value))


def _quote_fqn(fqn: str) -> str:
    return ".".join(f"`{part}`" for part in fqn.split("."))


def _to_date_str(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d")
    return str(value)[:10]


def get_table_columns(w: WorkspaceClient, fqn: str) -> list[dict]:
    """Colunas atuais da tabela no Unity Catalog, na ordem física."""
    info = w.tables.get(full_name=fqn)
    cols = sorted(info.columns or [], key=lambda c: c.position or 0)
    result = []
    for c in cols:
        col_type = c.type_name.value.lower() if c.type_name else (c.type_text or "")
        result.append({"name": c.name, "type": col_type, "comment": c.comment or ""})
    return result


def get_last_execution(spark: SparkSession, fqn: str, date_column: str | None) -> str | None:
    """MAX da coluna de execução ou, sem coluna, a última escrita do histórico Delta."""
    table = _quote_fqn(fqn)
    if date_column:
        if not _COL_RE.match(date_column):
            raise ValueError(f"Nome de coluna inválido: {date_column}")
        row = spark.sql(f"SELECT MAX(`{date_column}`) AS m FROM {table}").first()
        return _to_date_str(row["m"] if row else None)
    history = spark.sql(f"DESCRIBE HISTORY {table} LIMIT 100").select("timestamp", "operation").collect()
    writes = [r["timestamp"] for r in history if r["operation"] in WRITE_OPERATIONS]
    return _to_date_str(max(writes)) if writes else None


def get_model_info(w: WorkspaceClient, fqn: str) -> dict:
    """Versões champion/challenger/latest e data de criação da versão champion."""
    model = w.registered_models.get(full_name=fqn, include_aliases=True)
    aliases = {a.alias_name: a.version_num for a in (model.aliases or [])}
    versions = list(w.model_versions.list(full_name=fqn))
    latest = max((v.version for v in versions), default=None)
    trained_version = aliases.get("champion", latest)
    last_training = None
    if trained_version is not None:
        mv = w.model_versions.get(full_name=fqn, version=trained_version)
        if mv.created_at:
            last_training = datetime.fromtimestamp(mv.created_at / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
    return {
        "name": fqn.split(".")[-1],
        "unity_catalog_path": fqn,
        "champion_version": aliases.get("champion"),
        "challenger_version": aliases.get("challenger"),
        "latest_version": latest,
        "last_training": last_training,
    }


def merge_columns(curated: list[dict], live: list[dict], curated_only: bool) -> tuple[list[dict], list[str], list[str]]:
    """Combina schema do UC com descrições/exemplos curados."""
    curated_by_name = {c["name"]: c for c in (curated or [])}
    live_names = {c["name"] for c in live}
    merged = []
    for col in live:
        cur = curated_by_name.get(col["name"])
        if curated_only and cur is None:
            continue
        merged.append(
            {
                "name": col["name"],
                "type": col["type"],
                "description": (cur or {}).get("description") or col["comment"],
                "example": (cur or {}).get("example", ""),
            }
        )
    new_cols = [c["name"] for c in live if c["name"] not in curated_by_name]
    removed_cols = [n for n in curated_by_name if n not in live_names]
    return merged, new_cols, removed_cols


def build_live_metadata(spark: SparkSession, w: WorkspaceClient, curated: dict) -> dict:
    live: dict = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "algorithms": {},
    }
    for algo in curated["algorithms"]:
        entry: dict = {}
        out = algo.get("output_table") or {}
        table_fqn = out.get("unity_catalog_path")
        if _is_uc_path(table_fqn):
            try:
                uc_cols = get_table_columns(w, table_fqn)
                cols, new_cols, removed = merge_columns(
                    out.get("columns", []), uc_cols, out.get("column_selection") == "curated"
                )
                entry["output_table"] = {
                    "columns": cols,
                    "new_columns": new_cols,
                    "removed_columns": removed,
                    "schema_refreshed_at": live["generated_at"],
                }
                last_run = get_last_execution(spark, table_fqn, out.get("execution_date_column"))
                if last_run:
                    entry["last_run"] = last_run
            except Exception as exc:  # tabela inexistente ou sem permissão
                entry["output_table_error"] = f"{type(exc).__name__}: {exc}"[:300]

        model_fqn = (algo.get("registered_model") or {}).get("unity_catalog_path")
        if _is_uc_path(model_fqn):
            try:
                model_info = get_model_info(w, model_fqn)
                last_training = model_info.pop("last_training")
                if last_training:
                    entry["last_training"] = last_training
                entry["registered_model"] = model_info
            except Exception as exc:
                entry["registered_model_error"] = f"{type(exc).__name__}: {exc}"[:300]

        if entry:
            live["algorithms"][algo["id"]] = entry
    return live


def main(data_dir: Path | None = None, write: bool = True) -> dict:
    data_dir = data_dir or _default_data_dir()
    with open(data_dir / "algorithms.yaml", "r", encoding="utf-8") as f:
        curated = yaml.safe_load(f)

    spark = SparkSession.builder.getOrCreate()
    w = WorkspaceClient()
    live = build_live_metadata(spark, w, curated)

    for algo_id, entry in live["algorithms"].items():
        out = entry.get("output_table", {})
        print(
            f"{algo_id}: last_run={entry.get('last_run')} last_training={entry.get('last_training')} "
            f"cols={len(out.get('columns', []))} new={out.get('new_columns', [])} "
            f"removed={out.get('removed_columns', [])} "
            f"errors={[k for k in entry if k.endswith('_error')]}"
        )

    if write:
        target = data_dir / "algorithms_live.yaml"
        with open(target, "w", encoding="utf-8") as f:
            f.write("# Arquivo gerado por scripts/refresh_algorithms_metadata.py — não editar manualmente.\n")
            yaml.safe_dump(live, f, allow_unicode=True, sort_keys=False, width=120)
        print(f"Gravado: {target}")
    return live


if __name__ == "__main__":
    main(write="--dry-run" not in sys.argv)
