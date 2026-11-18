"""Biblioteca de UI central do Sales ADAN Hub.

Concentra helpers de texto/formatação e o CSS global, para que cada página
não precise reimplementar escape de $, formatação de data/moeda ou lidar
com o teto visual nativo do Streamlit (ver auditoria v2 — U1, L2, L3, L6).
"""

from datetime import date, datetime

import streamlit as st

_STYLE_INJECTED_KEY = "_ui_style_injected"

_CSS = """
<style>
/* largura máxima confortável no modo wide (resolve L1) */
.block-container { max-width: 1280px; }

/* evita palavras quebradas no meio: só quebra uma palavra isolada quando ela
   sozinha não cabe no container (ex.: URL longa), nunca em texto normal
   (resolve L3/A10 — "break-word" preserva a palavra sempre que há opção de
   quebrar entre palavras; "anywhere" quebraria qualquer palavra prematuramente) */
h1, h2, h3, [data-testid="stMarkdownContainer"] {
    overflow-wrap: break-word;
    word-break: normal;
    hyphens: auto;
}

/* cards com a mesma altura na linha, mesmo com texto de tamanhos diferentes (resolve L2/N3) */
[data-testid="stHorizontalBlock"] { align-items: stretch; }
[data-testid="stColumn"] > div { height: 100%; }

/* contraste dos textos secundários (captions) */
[data-testid="stCaptionContainer"] { color: #4A5563; }
</style>
"""


def aplicar_estilo():
    """Injeta o CSS global uma única vez por sessão."""
    if not st.session_state.get(_STYLE_INJECTED_KEY):
        st.markdown(_CSS, unsafe_allow_html=True)
        st.session_state[_STYLE_INJECTED_KEY] = True


def md(texto: str, **kwargs):
    """st.markdown que escapa `$` para não ser interpretado como LaTeX (resolve U1/L6)."""
    st.markdown(texto.replace("$", r"\$"), **kwargs)


def data_br(d: "date | datetime | str | None") -> str:
    """Formata uma data no padrão dd/mm/aaaa. Aceita date/datetime ou string ISO (aaaa-mm-dd)."""
    if d is None:
        return "Não disponível"
    if isinstance(d, (date, datetime)):
        return d.strftime("%d/%m/%Y")
    texto = str(d).strip()
    if len(texto) >= 10 and texto[4] == "-" and texto[7] == "-":
        ano, mes, dia = texto[:10].split("-")
        return f"{dia}/{mes}/{ano}"
    return texto


def brl(valor: float) -> str:
    """Formata um número como moeda brasileira: R$ 1.234."""
    return f"R$ {valor:,.0f}".replace(",", ".")
