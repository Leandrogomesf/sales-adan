"""
Valida a consistência de data/portfolio.yaml antes de publicar o hub.

Checa:
  1. Toda fase de produto pertence a components.status.PHASE_ORDER.
  2. Nenhum produto duplicado por id.
  3. Nenhum algoritmo duplicado por id (entre todos os produtos).
  4. Todo produto tem operational_status preenchido.

Uso: python scripts/validar_portfolio.py
Sai com código 1 e lista os problemas encontrados, ou código 0 se tudo ok.
"""

import io
import sys
from pathlib import Path

import yaml

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from components.status import PHASE_ORDER

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def validar() -> list[str]:
    with open(DATA_DIR / "portfolio.yaml", "r", encoding="utf-8") as f:
        portfolio = yaml.safe_load(f)

    erros = []
    product_ids_vistos = set()
    algorithm_ids_vistos = set()

    for product in portfolio["products"]:
        pid = product["id"]
        if pid in product_ids_vistos:
            erros.append(f"Produto duplicado: id='{pid}'")
        product_ids_vistos.add(pid)

        if product.get("phase") not in PHASE_ORDER:
            erros.append(f"Produto '{pid}': fase inválida '{product.get('phase')}' (válidas: {PHASE_ORDER})")

        if not product.get("operational_status"):
            erros.append(f"Produto '{pid}': operational_status não preenchido")

        for algo in product.get("algorithms", []):
            aid = algo["id"]
            if aid in algorithm_ids_vistos:
                erros.append(f"Algoritmo duplicado: id='{aid}' (produto '{pid}')")
            algorithm_ids_vistos.add(aid)

            if not algo.get("operational_status"):
                erros.append(f"Algoritmo '{aid}' (produto '{pid}'): operational_status não preenchido")

    return erros


def main() -> int:
    erros = validar()
    if erros:
        print(f"❌ {len(erros)} problema(s) encontrado(s) em data/portfolio.yaml:\n")
        for erro in erros:
            print(f"  - {erro}")
        return 1

    print("✅ data/portfolio.yaml consistente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
