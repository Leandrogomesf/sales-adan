# Auditoria UX/UI v2 — Sales ADAN Hub

**Data:** 18/11/2026
**Versão:** 2. Substitui a v1 e acrescenta testes de interação, responsividade e uma análise das limitações do Streamlit.
**Escopo:** 5 páginas: Visão Geral, Produtos de Dados, Detalhe do Algoritmo, Testes e Resultados e Metodologia.
**Método:** navegação no app publicado. Li textos e estrutura, fiz capturas de tela e testei expanders, filtros, busca, estado vazio e navegação de Produtos para Algoritmo. Testei duas larguras de janela: cerca de 1150px e cerca de 900px. O código-fonte não foi analisado, então os trechos de código assumem uma implementação típica.

**O que não foi testado:**
- modo escuro;
- celular (só simulei uma janela mais estreita);
- todas as combinações de filtro;
- todos os algoritmos (abri Customer Clustering e Modelo de Potencial de PDV);
- as fases de Explore a Sustain na Metodologia.

**Público assumido:** liderança de Vendas, Trade e CRM (pouco tempo, perfil não técnico) e o time de dados (perfil técnico).

---

## 1. Resumo executivo

O hub tem uma **boa espinha dorsal**:
- catálogo filtrável com estado vazio;
- navegação de Produto para Algoritmo com o produto já selecionado;
- transparência sobre limitações e sobre os pilotos;
- OKR com baseline e meta;
- glossário.

Os problemas se concentram em quatro frentes:

1. **Dados inconsistentes entre páginas.** O mesmo produto aparece com fases e status diferentes, e as contagens não batem. É o risco nº 1, porque a liderança perde confiança no hub inteiro quando encontra um número contraditório.
2. **Bugs de texto e formato.** Há `R$`/`US$` virando fórmula, a data `2026-18-11`, títulos de piloto que contradizem o período e textos do Streamlit em inglês.
3. **Layout que não aguenta a largura.** Em janela menor, palavras quebram no meio, tabelas são cortadas e o menu esconde páginas atrás de "View more".
4. **Hierarquia fraca para executivos.** O resultado principal fica longe da primeira dobra, há muito texto e quase nenhum gráfico.

A raiz das frentes 1 e 4 é a mesma: **o conteúdo parece estar fixo em várias páginas, em vez de vir de uma fonte única.** Resolver isso elimina boa parte dos problemas de uma vez.

### Notas por página

| Página | Nota | Principal ponto |
|---|---|---|
| Visão Geral | 6/10 | Primeira dobra desperdiçada, contagens que não batem com Produtos |
| Produtos de Dados | 7/10 | Boa interação, mas a busca não acha algoritmos, a fase vem em minúsculas e há quebra de palavras em janela menor |
| Detalhe do Algoritmo | 7/10 | Ótima estrutura em abas, mas a fase diverge do catálogo e as datas parecem paradas |
| Testes e Resultados | 5,5/10 | Bug de `$`, números repetidos entre pilotos e período contraditório |
| Metodologia | 6,5/10 | Conteúdo sólido, mas denso, com colunas estreitas e tabela cortada |

---

## 2. Pontos fortes (manter)

- **Estado vazio na busca de Produtos:** "Nenhum produto encontrado com os filtros selecionados" e o contador "0 de 8 produtos exibidos".
- **Filtros multiselect** com chips removíveis e contador de resultados.
- **"Ver detalhe do produto"** leva ao Algoritmo com o produto e o algoritmo já selecionados, e com breadcrumb.
- **Estado "não produtivo" tratado no Algoritmo:** "Última execução: Não disponível (ainda não produtivo)".
- **Abas internas no Algoritmo** (Visão funcional, Funcionamento técnico, Tabela gerada, Métricas técnicas e Valor para o negócio), que separam bem os dois públicos.
- **"Explicação não técnica" e "Limitações conhecidas"**, raras em hubs de dados e muito valiosas.
- **Transparência nos pilotos:** período, fonte e aviso de "piloto encerrado". Também informa quando amostra e controle não estão detalhados.
- **OKR (PUDMA)** com tabela de Key Results, baseline e meta.
- **Glossário** em tabela e link para o Data Catalog.
- **Roadmap em quadro** por fase (Discovery, PoC, MVP, Sustain), com mês de cada item.

---

## 3. Achados novos desta rodada

| # | Onde | Achado |
|---|---|---|
| A1 | Produtos × Algoritmo | **Metas** aparece como **PoC** no catálogo e como **"Discovery — hipótese em backtest (H1)"** no detalhe |
| A2 | Roadmap × Produtos | **Portfólio Prioritário** está em **Sustain (Ago/26)** no Roadmap e em **MVP / Test** no catálogo |
| A3 | Produtos × Algoritmo | **Customer Clustering** está como **Sustain / Test** no catálogo e **Sustain / Live** no detalhe |
| A4 | Visão Geral × Produtos | "**6 produtos** em Discovery, PoC ou MVP" na Visão Geral, mas o catálogo tem **5** produtos nessas fases (Step Discount, Metas, Tasks, Cross-sell e Portfólio Prioritário). O número 6 parece contar itens do Roadmap, não produtos |
| A5 | Visão Geral × Roadmap | "**11** algoritmos de ML" na Visão Geral, mas o Roadmap lista **14** itens |
| A6 | Produtos | O placeholder da busca diz "Nome do produto **ou algoritmo**", mas buscar "kmeans" retorna **0 resultados** |
| A7 | Produtos | As opções do filtro Fase aparecem como valores crus em minúsculas (`discovery`, `mvp`, `poc`, `sustain`) e em **ordem alfabética**, não na ordem de maturidade. Os badges dos cards usam "PoC" e "MVP" |
| A8 | Produtos | O estado vazio não tem botão "Limpar filtros" |
| A9 | Todas (janela ~900px) | A sidebar esconde "Metodologia" atrás de **"View more"**, em inglês |
| A10 | Produtos (janela ~900px) | Títulos dos cards quebram no meio da palavra ("Clusterin/g", "Intelligen/ce") e os selects truncam ("Choose a…", "Metas (Target Int…") |
| A11 | Visão Geral → OKR | A coluna "Meta" da tabela de Key Results é cortada à direita |
| A12 | Glossário | Faltam termos usados no hub: **ELMA, DTS, OT, GV, ADAN, DS/DE/AR/GOV, Champion/Challenger** |

---

## 4. Diagnóstico por pilar

### 4.1 Arquitetura da informação
- **Primeira dobra:** o expander "Roadmap" aparece acima do título em **todas** as páginas. Ele empurra o conteúdo para baixo e repete a tabela "Evolução do portfólio".
- **Visão Geral longa:** são cerca de 10 seções. O resultado (+R$ 3 mi) só aparece no terceiro scroll.
- **Redundâncias:**
  - "Áreas impactadas" repete "Público impactado";
  - "Última atualização" aparece duas vezes;
  - o callout azul repete o botão "Ver Testes e Resultados";
  - o expander "Tabelas geradas" repete a aba "Tabela gerada".
- **Métricas para o público errado:** "Features construídas" e "Hipóteses testadas" medem esforço, não resultado. Cabem melhor na página técnica.
- **Testes e Resultados fora de ordem:** Set → Fev–Abr → Ago/Set → Out. Além disso, mistura R$, US$ e % sem base.
- **Fontes com nome de arquivo interno**, por exemplo `OKR_Sales_Intelligence.md` e `STATUS ENTREGAS SALES ADAN.pdf`.

### 4.2 Usabilidade
- O layout centrado usa cerca de 650px de 1150px, o que gera cards apertados e textos quebrados.
- Há três formatos de data: `2026-18-11`, `18/11/2026` e `2026-08-21`.
- Os idiomas se misturam: "Choose an option", "View more", "Live/Test/WIP" e "Kill".
- Não há legenda para a barra de progresso (16%, 50%, 83%) nem para os badges de fase e status.
- Os rótulos estão em cinza claro e pequeno, com contraste insuficiente.
- O rótulo "−40h" parece negativo e não diz o período. "+1 oferta" arredonda uma diferença de 0,73.

### 4.3 Interatividade
- Os filtros funcionam, mas a busca não cobre algoritmos e a ordem das fases é alfabética.
- Os botões "Ver X →" parecem `st.button` + `switch_page`, que não abrem em nova aba nem geram link compartilhável.
- As datas de execução parecem fixas: Customer Clustering mostra "Live" e "mensal", mas a última execução foi em 21/08.
- O site quase não tem gráficos. As tendências aparecem como texto ("declinante", "volátil").

### 4.4 UI visual
- Os cards são HTML customizado e a altura varia conforme o texto, então as grades ficam desalinhadas.
- O ícone 📊 se repete em todos os KPIs de Testes, sem significado próprio.
- Emojis (navegação, títulos) convivem com ícones de linha (cards), e o visual fica sem unidade.
- As cores dos badges não seguem uma semântica fixa por fase.
- O vermelho do tema aparece nos chips de filtro e nas abas, e pode ser lido como "erro".

---

## 5. Limitações do Streamlit e como vencê-las

Esta seção mostra, para cada limitação: como ela aparece no hub, a solução dentro do Streamlit e a alternativa quando o Streamlit não basta.

> Vários recursos citados existem só em versões recentes (1.4x). Confira com `st.__version__`, fixe a versão no `requirements.txt` do Databricks App e consulte a documentação da versão instalada antes de aplicar.

| # | Limitação do Streamlit | Como aparece no hub | Solução no Streamlit | Alternativa fora dele |
|---|---|---|---|---|
| L1 | Layout centrado por padrão, sem grid real | Conteúdo estreito, cards apertados | `layout="wide"` com no máximo 3 colunas por linha | — |
| L2 | `st.columns` não iguala alturas | Grades de cards desalinhadas | `st.container(border=True)` + CSS de altura uniforme (ver 6.4) | Componente customizado ou frontend React |
| L3 | Responsividade limitada (as colunas só empilham em telas bem pequenas) | Palavras quebradas em janela de ~900px | Menos colunas, `overflow-wrap`, media queries injetadas via CSS | Dash ou React com breakpoints reais |
| L4 | Menu lateral recolhe itens em telas baixas ("View more") | "Metodologia" escondida | `st.navigation(..., position="top")` ou `expanded=True`, conforme a versão; agrupar páginas em seções | — |
| L5 | Textos internos dos widgets em inglês | "Choose an option", "View more" | `placeholder=` em selectbox e multiselect; navegação no topo elimina "View more" | — |
| L6 | Markdown interpreta `$...$` como LaTeX | "R$ e US$" virou fórmula | Helper que escapa `$` em todo texto (ver 6.2) | — |
| L7 | Rerun completo a cada interação | Ainda não dói, mas vai doer com mais filtros e dados | `st.cache_data`, `st.fragment` e `st.form` | — |
| L8 | `st.dataframe` não quebra texto longo | Colunas "Responsabilidade", "O que acontece" e "Meta" cortadas | `st.table` para tabelas pequenas; `column_config` com `width="large"` | AgGrid (componente) para tabelas ricas |
| L9 | Tema com poucos tokens | Visual "Streamlit padrão" e vermelho como cor primária | `.streamlit/config.toml` com `[theme]`; versões recentes aceitam raio de borda e fontes customizadas | — |
| L10 | Cards ricos exigem HTML com `unsafe_allow_html` | Cards frágeis, pouca acessibilidade, CSS espalhado | Centralizar em `ui.py`; preferir `st.metric(border=True)`, `st.badge` e `st.container(border=True)` | Componente customizado (React) |
| L11 | Gráficos nativos simples | Roadmap e tendência como texto ou tabela | Plotly (`px.timeline` para Gantt) ou Altair | Databricks AI/BI Dashboards para métricas |
| L12 | Sem deep link de estado por padrão | Não dá para compartilhar "Algoritmo X" por link | `st.query_params` para produto e algoritmo | — |
| L13 | Impressão e exportação ruins | A liderança não consegue levar a visão para reunião | Botão "Baixar resumo (PDF)" gerado no servidor; modo apresentação que esconde a sidebar | Slides ou documento gerado a partir da mesma fonte de dados |
| L14 | Controle fraco de acessibilidade (ARIA, foco) | Emojis lidos por leitor de tela, cor como único diferenciador | Ícones Material (`:material/...:`) no lugar de emojis; texto e cor juntos | Frontend próprio |
| L15 | Cold start de app no Databricks | Primeira carga lenta (percepção de "travado") | `st.spinner` ou `st.status` na carga inicial; cache de dados | — |

### 5.1 Quando sair do Streamlit (matriz de decisão)

| Opção | Quando faz sentido | Prós | Contras | Esforço |
|---|---|---|---|---|
| **Ficar no Streamlit + camada de design** (recomendado agora) | O hub é majoritariamente conteúdo e catálogo, com pouca interação | Time já domina; deploy no Databricks Apps; custo baixo | Teto visual e de responsividade | Baixo |
| **Databricks AI/BI Dashboard** para a parte de métricas | Números de pilotos e KPIs que se atualizam | Nativo no Databricks, governança do Unity Catalog, Genie integrado | Pouco flexível para conteúdo textual | Baixo–médio |
| **Site de documentação** (por exemplo MkDocs Material) para Metodologia e Glossário | Conteúdo estável, longo, com busca e versionamento | Ótima leitura, busca embutida, versionado em Git | Outro sistema para manter | Médio |
| **Dash (Plotly)** | Muitos gráficos interativos com layout preciso | Grid e callbacks finos, sem rerun completo | Curva de aprendizado e mais código | Médio–alto |
| **React + FastAPI no Databricks Apps** | Hub vira produto com perfis de usuário, SSO granular e design system próprio | Controle total de UX e responsividade | Exige frontend dedicado e manutenção | Alto |

**Recomendação:** manter o Streamlit e atacar a raiz, ou seja, fonte única de dados e biblioteca de componentes. Os números de resultado podem migrar para um AI/BI Dashboard embutido por link, e o time já usa esse padrão no Sales Intelligence Dashboard. Vale reavaliar React ou Dash se aparecerem estes requisitos:
- visões por perfil;
- edição de conteúdo pelo negócio;
- uso frequente em celular.

---

## 6. Padrões de solução (código de referência)

### 6.1 Fonte única de verdade para o portfólio
Resolve A1–A5 e o U5 da v1. Todas as páginas leem o mesmo arquivo ou tabela, e as contagens passam a ser **calculadas**, não digitadas.

```yaml
# data/portfolio.yaml
produtos:
  - id: metas
    nome: "Metas (Target Intelligence)"
    codigo: "MT 8.1"
    modulo: Vendedor
    fase: PoC            # um único valor, usado no catálogo, no detalhe e no roadmap
    status: WIP
    areas: [DTS, Sales Intelligence, Trade]
    algoritmos:
      - nome: "Modelo de Potencial de PDV (Build-up Bottom-up)"
        tipo: "Build-up bottom-up"
        modelo_uc: null
```

```python
# core/dados.py
import yaml
import streamlit as st

FASES = ["Discovery", "Explore", "PoC", "Pilot", "MVP", "Sustain"]

@st.cache_data(ttl=3600)
def carregar_portfolio() -> dict:
    with open("data/portfolio.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)

def resumo(portfolio: dict) -> dict:
    produtos = portfolio["produtos"]
    return {
        "produtos": len(produtos),
        "em_desenvolvimento": sum(p["fase"] != "Sustain" for p in produtos),
        "algoritmos": sum(len(p["algoritmos"]) for p in produtos),
    }
```

Acrescente um teste simples no CI para garantir que toda fase pertença a `FASES` e que nenhum produto apareça duplicado.

### 6.2 Texto seguro (escape de `$`) e formatação padrão
```python
# core/ui.py
from datetime import date
import streamlit as st

def md(texto: str, **kwargs):
    """Markdown sem interpretar $ como LaTeX."""
    st.markdown(texto.replace("$", r"\$"), **kwargs)

def data_br(d: date | None) -> str:
    return d.strftime("%d/%m/%Y") if d else "Não disponível"

def brl(valor: float) -> str:
    return f"R$ {valor:,.0f}".replace(",", ".")
```

### 6.3 Tema e configuração global
```toml
# .streamlit/config.toml
[theme]
base = "light"
primaryColor = "#1F5AA6"           # azul institucional no lugar do vermelho padrão
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F3F5F8"
textColor = "#1B2430"
font = "sans serif"
```

```python
st.set_page_config(page_title="Sales ADAN Hub", page_icon=":material/insights:", layout="wide")
```

### 6.4 CSS mínimo e centralizado
Aplique-o uma vez, no arquivo de entrada.

```python
# core/estilo.py
import streamlit as st

CSS = """
<style>
/* largura máxima confortável no modo wide */
.block-container { max-width: 1280px; }

/* evita palavras quebradas no meio, mas permite quebrar strings longas */
h1, h2, h3 { overflow-wrap: normal; word-break: normal; hyphens: auto; }
[data-testid="stMarkdownContainer"] { overflow-wrap: anywhere; }

/* cards com a mesma altura na linha */
[data-testid="stHorizontalBlock"] { align-items: stretch; }
[data-testid="stColumn"] > div { height: 100%; }

/* contraste dos textos secundários */
[data-testid="stCaptionContainer"] { color: #4A5563; }
</style>
"""

def aplicar_estilo():
    st.markdown(CSS, unsafe_allow_html=True)
```

> **Atenção:** seletores `data-testid` podem mudar entre versões do Streamlit. Fixe a versão e revise o CSS a cada atualização. Esse é o custo de contornar o layout nativo.

### 6.5 Navegação no topo, com seções e links reais
Resolve A9 e o "View more".

```python
# app.py
import streamlit as st
from core.estilo import aplicar_estilo

st.set_page_config(page_title="Sales ADAN Hub", layout="wide")
aplicar_estilo()

paginas = {
    "Visão": [
        st.Page("paginas/visao_geral.py", title="Visão Geral", icon=":material/home:", default=True),
        st.Page("paginas/resultados.py", title="Resultados", icon=":material/trending_up:"),
    ],
    "Portfólio": [
        st.Page("paginas/produtos.py", title="Produtos", icon=":material/widgets:"),
        st.Page("paginas/algoritmos.py", title="Algoritmos", icon=":material/science:"),
        st.Page("paginas/roadmap.py", title="Roadmap", icon=":material/timeline:"),
    ],
    "Referência": [
        st.Page("paginas/metodologia.py", title="Metodologia", icon=":material/explore:"),
    ],
}
st.navigation(paginas, position="top").run()   # em versões sem "top": position="sidebar", expanded=True
```

Dentro das páginas, troque `st.button` + `switch_page` por link real:
```python
st.page_link("paginas/resultados.py", label="Ver resultados", icon=":material/arrow_forward:")
```

### 6.6 Filtros de Produtos corrigidos
Resolve A6, A7 e A8.

```python
from core.dados import FASES, carregar_portfolio

produtos = carregar_portfolio()["produtos"]
CHAVES = ("f_modulo", "f_fase", "f_area", "f_busca")

c1, c2, c3 = st.columns(3)
modulos = c1.multiselect("Módulo", sorted({p["modulo"] for p in produtos}),
                         placeholder="Todos", key="f_modulo")
fases = c2.multiselect("Fase", FASES, placeholder="Todas", key="f_fase")   # ordem de maturidade
areas = c3.multiselect("Área consumidora", sorted({a for p in produtos for a in p["areas"]}),
                       placeholder="Todas", key="f_area")
busca = st.text_input("Buscar", placeholder="Produto, código ou algoritmo (ex.: KMeans)",
                      key="f_busca")

def corresponde(p: dict) -> bool:
    texto = " ".join([p["nome"], p["codigo"], p.get("descricao", ""),
                      *[a["nome"] for a in p["algoritmos"]],
                      *[a.get("tipo", "") for a in p["algoritmos"]]]).lower()
    return ((not modulos or p["modulo"] in modulos)
            and (not fases or p["fase"] in fases)
            and (not areas or set(areas) & set(p["areas"]))
            and (not busca or busca.lower() in texto))

filtrados = [p for p in produtos if corresponde(p)]
st.caption(f"{len(filtrados)} de {len(produtos)} produtos")

if not filtrados:
    st.info("Nenhum produto encontrado com esses filtros.")
    if st.button("Limpar filtros", icon=":material/filter_alt_off:"):
        for k in CHAVES:
            st.session_state.pop(k, None)
        st.rerun()
```

### 6.7 Card de produto padronizado (grade de 3 colunas)
```python
COR_FASE = {"Discovery": "gray", "Explore": "violet", "PoC": "orange",
            "Pilot": "blue", "MVP": "green", "Sustain": "primary"}

def card_produto(p: dict):
    with st.container(border=True):
        st.badge(p["fase"], color=COR_FASE[p["fase"]])
        st.markdown(f"#### {p['nome']}")
        st.caption(p["codigo"])
        md(p["descricao"])
        st.caption(f"Módulo: {p['modulo']} · Áreas: {', '.join(p['areas'])}")
        st.page_link("paginas/algoritmos.py", label="Ver detalhe",
                     query_params={"produto": p["id"]})

for i in range(0, len(filtrados), 3):
    for col, p in zip(st.columns(3), filtrados[i:i + 3]):
        with col:
            card_produto(p)
```
Na página de algoritmos, leia o parâmetro com `st.query_params.get("produto")` para pré-selecionar o produto. Assim o link pode ser compartilhado. Verifique se a sua versão aceita `query_params` em `st.page_link`. Se não aceitar, defina `st.session_state` antes de navegar.

### 6.8 Alerta de atualização do modelo
Resolve o caso do Customer Clustering, que aparece como "Live" mas foi executado pela última vez em 21/08.

```python
from datetime import date

LIMITE_DIAS = {"Mensal": 35, "Semanal": 9, "Diária": 2}

def alerta_frescor(ultima_execucao: date | None, frequencia: str):
    if ultima_execucao is None:
        st.info("Ainda não executado em produção.")
        return
    atraso = (date.today() - ultima_execucao).days
    if atraso > LIMITE_DIAS.get(frequencia, 35):
        st.warning(f"Última execução há {atraso} dias, acima da frequência {frequencia.lower()}.")
```
Idealmente, `ultima_execucao` vem do histórico da tabela no Unity Catalog (`DESCRIBE HISTORY`) ou do registry do MLflow, e não de texto fixo.

### 6.9 Primeira dobra da Visão Geral
```python
st.title("Sales ADAN")
st.caption(f"Inteligência de dados e ML para a jornada de vendas nos PDVs · Atualizado em {data_br(ATUALIZACAO)}")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Net Sales incremental", "+R$ 3 mi", border=True,
          help="Piloto de set/2026, já encerrado. Atribuído via VMD vs. grupo controle.")
k2.metric("Volume incremental", "+59 t", border=True)
k3.metric("Produtos em desenvolvimento", resumo(port)["em_desenvolvimento"], border=True)
k4.metric("Horas economizadas", "40 h", border=True, help="Redução média por vendedor no piloto.")

st.page_link("paginas/resultados.py", label="Ver todos os resultados",
             icon=":material/arrow_forward:")
```

### 6.10 Roadmap como Gantt (substitui o expander e a tabela)
```python
import plotly.express as px

fig = px.timeline(df_roadmap, x_start="inicio", x_end="fim", y="iniciativa",
                  color="fase", category_orders={"fase": FASES})
fig.update_yaxes(autorange="reversed", title=None)
fig.update_layout(height=40 * len(df_roadmap) + 80, legend_title_text="Fase")
st.plotly_chart(fig, use_container_width=True)
```

### 6.11 Tendência do piloto em gráfico
```python
import pandas as pd

tendencia = pd.DataFrame(
    {"Volume vs controle": [17.5, 9, 6],
     "Tarefas efetivadas vs controle": [-11, 1.9, 3.2],
     "Adoção digital vs controle": [1.5, -1, 1]},
    index=["Fev", "Mar", "Abr"])
st.line_chart(tendencia)
st.caption("Diferença em pontos percentuais vs. grupo controle · Piloto CC V2")
```

---

## 7. Melhorias priorizadas

### 🔴 URGENTE: informação errada ou quebrada (corrigir antes de divulgar)

| # | Item | Página | Esforço |
|---|---|---|---|
| U1 | Escapar `$`: "R$ e US$" está virando fórmula (6.2) | Testes e Resultados | Minutos |
| U2 | Unificar fase e status por produto: Metas (PoC × Discovery), Portfólio Prioritário (MVP × Sustain), Customer Clustering (Test × Live) | Produtos, Algoritmo, Roadmap | Horas |
| U3 | Corrigir as contagens: "6 produtos em desenvolvimento" (são 5) e "11 algoritmos" (o Roadmap mostra 14), e passar a calculá-las (6.1) | Visão Geral | Horas |
| U4 | Confirmar se os pilotos "Uplift Set" e "ELMA" são o mesmo: os números são idênticos e podem ser lidos como contagem dupla | Testes, Visão Geral | Horas (com o time) |
| U5 | Corrigir o título "Setembro" no bloco ELMA, cujo período é "Agosto" | Testes e Resultados | Minutos |
| U6 | Corrigir a data `2026-18-11` e padronizar `dd/mm/aaaa` em todo o site | Todas | Minutos |
| U7 | Verificar o pipeline do Customer Clustering (última execução em 21/08 com status Live e mensal) e exibir alerta de atraso (6.8) | Algoritmo | Horas |
| U8 | Atualizar a referência "ver na Visão Geral" para Testes e Resultados, com `st.page_link` | Algoritmo | Minutos |
| U9 | `layout="wide"` + CSS anti-quebra de palavra (6.3, 6.4) | Todas | Minutos |
| U10 | Navegação no topo ou expandida, para não esconder "Metodologia" atrás de "View more" (6.5) | Todas | Minutos |
| U11 | Trocar nomes de arquivos internos por fontes legíveis | Testes e Resultados | Minutos |
| U12 | Corrigir o rótulo "+1 oferta" (a diferença real é 0,73) e "−40h" ("40 h economizadas por …") | Testes, Visão Geral | Minutos |
| U13 | Typo: "operação contígua" → "contínua" | Metodologia | Minutos |

### 🟠 NICE TO HAVE: impacto claro em usabilidade

| # | Item | Página |
|---|---|---|
| N1 | Primeira dobra com resultado: título → 4 métricas → link (6.9); mover o expander Roadmap para uma página própria | Visão Geral |
| N2 | Filtro Fase com rótulos corretos e em ordem de maturidade; busca que encontra algoritmos; botão "Limpar filtros" (6.6) | Produtos |
| N3 | Grade de cards em 3 colunas com altura uniforme e card padronizado (6.7) | Produtos |
| N4 | Legenda para fase, status e barra de progresso (ou trocar a barra por "Fase 3 de 6") | Produtos |
| N5 | Placeholders em português ("Todos", "Todas") em todos os selects | Produtos, Algoritmo |
| N6 | Visão Geral em abas: Resumo · Resultados e KPIs · Time e OKR | Visão Geral |
| N7 | Remover redundâncias: "Áreas impactadas", callout azul, "Última atualização" duplicada e expander "Tabelas geradas" | Visão Geral, Algoritmo |
| N8 | Tabelas com texto longo em `st.table` (Time, Key Results, Mapeamento PepOne) | Visão Geral, Metodologia |
| N9 | Pilotos em ordem cronológica, moeda principal única e base do "+6%" | Testes e Resultados |
| N10 | Tendência do piloto CC V2 em gráfico (6.11) | Testes e Resultados |
| N11 | KPIs com ícone próprio (não 📊 em todos) e valor separado da descrição | Testes e Resultados |
| N12 | Completar o Glossário: ELMA, DTS, OT, GV, ADAN, DS/DE/AR/GOV, Champion/Challenger | Visão Geral |
| N13 | Etapas do PepOne em linha do tempo ou lista numerada (hoje são 7 colunas estreitas) e resumo de 3 linhas no topo | Metodologia |
| N14 | "Métricas técnicas" preenchidas com números reais ou ocultas; nada de "Não disponível neste documento" | Algoritmo |
| N15 | Tema próprio: cor primária institucional no lugar do vermelho padrão, que pode parecer "erro" (6.3) | Todas |

### 🟢 GOOD TO HAVE: evolução de médio e longo prazo

| # | Item | Observação |
|---|---|---|
| G1 | Fonte única de verdade (`portfolio.yaml` ou tabela Delta) + teste de consistência no CI (6.1) | Elimina a classe inteira de inconsistências |
| G2 | Biblioteca `core/ui.py` com `md`, `card_produto`, `kpi`, `badge_fase` e `alerta_frescor` | Visual consistente e um só lugar para manter |
| G3 | Roadmap em Gantt numa página própria (6.10) | Substitui o expander repetido e a tabela |
| G4 | Deep links com `st.query_params` (produto e algoritmo) | Permite compartilhar o link exato numa conversa ou reunião |
| G5 | Datas de execução e versões (champion/challenger) lidas do Unity Catalog e do MLflow | Fim dos metadados fixos |
| G6 | Ícones Material no lugar de emojis; cor sempre acompanhada de texto | Coesão visual e acessibilidade |
| G7 | Exportação "Resumo executivo (PDF)" ou modo apresentação | Compensa a impressão ruim do Streamlit |
| G8 | Painel de resultados como AI/BI Dashboard embutido por link | Números vivos com governança nativa |
| G9 | Metodologia e Glossário como site de documentação, se o conteúdo crescer | Melhor leitura e busca para conteúdo longo |
| G10 | Telemetria de uso (páginas mais vistas, buscas sem resultado) | Orienta as próximas melhorias com dados |
| G11 | Reavaliar Dash ou React se surgirem visões por perfil, edição pelo negócio ou uso em celular (5.1) | Decisão de arquitetura, não urgente |

---

## 8. Checklist de QA antes de cada publicação

- [ ] Testar em 1440px, 1280px, 1024px e ~900px de largura (quebra de palavras, colunas, menu)
- [ ] Testar em modo escuro
- [ ] Buscar `$` em todos os textos exibidos
- [ ] Rodar o teste de consistência do portfólio (fases válidas, sem duplicados, contagens calculadas)
- [ ] Conferir se todas as datas estão em `dd/mm/aaaa`
- [ ] Clicar em todos os links internos (nenhum aponta para seção movida)
- [ ] Confirmar que nenhum texto do Streamlit aparece em inglês
- [ ] Verificar o frescor dos modelos marcados como "Live"

---

## 9. Plano de execução sugerido

| Etapa | Conteúdo | Esforço |
|---|---|---|
| 1. Higiene | U1, U5, U6, U8–U13 | Meio dia |
| 2. Consistência | U2, U3, U4, U7 + G1 (fonte única) | 2 a 3 dias, com validação do time |
| 3. Experiência | N1–N8, N15 + G2 (biblioteca de UI) | 3 a 5 dias |
| 4. Conteúdo e resultados | N9–N14 + G3, G4 | 1 sprint |
| 5. Evolução | G5–G11 | Planejar no roadmap |
