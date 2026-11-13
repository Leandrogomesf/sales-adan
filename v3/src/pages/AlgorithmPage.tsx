import { useEffect, useState } from "react";
import productsData from "../data/products.json";
import algorithmsData from "../data/algorithms.json";
import type { Product, Algorithm } from "../types";
import { RoadmapBanner } from "../components/RoadmapBanner";
import { PhaseBadge } from "../components/PhaseBadge";

const products = productsData.products as Product[];
const algorithms = algorithmsData.algorithms as Algorithm[];

type TabId = "functional" | "technical" | "table" | "metrics" | "value";

const TABS: { id: TabId; label: string }[] = [
  { id: "functional", label: "Visão funcional" },
  { id: "technical", label: "Funcionamento técnico" },
  { id: "table", label: "Tabela gerada" },
  { id: "metrics", label: "Métricas técnicas" },
  { id: "value", label: "Valor para o negócio" },
];

interface AlgorithmPageProps {
  selectedProductId: string | null;
  selectedAlgorithmId: string | null;
  onSelectionChange: (productId: string, algorithmId: string) => void;
}

export function AlgorithmPage({
  selectedProductId,
  selectedAlgorithmId,
  onSelectionChange,
}: AlgorithmPageProps) {
  const [productId, setProductId] = useState(selectedProductId ?? products[0].id);
  const [activeTab, setActiveTab] = useState<TabId>("functional");

  const algorithmsForProduct = algorithms.filter((a) => a.product_id === productId);
  const [algorithmId, setAlgorithmId] = useState(
    selectedAlgorithmId && algorithmsForProduct.some((a) => a.id === selectedAlgorithmId)
      ? selectedAlgorithmId
      : algorithmsForProduct[0]?.id ?? ""
  );

  useEffect(() => {
    if (selectedProductId) setProductId(selectedProductId);
  }, [selectedProductId]);

  useEffect(() => {
    const valid = algorithms.filter((a) => a.product_id === productId);
    if (!valid.some((a) => a.id === algorithmId)) {
      setAlgorithmId(valid[0]?.id ?? "");
    }
  }, [productId]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (algorithmId) onSelectionChange(productId, algorithmId);
  }, [productId, algorithmId]); // eslint-disable-line react-hooks/exhaustive-deps

  const product = products.find((p) => p.id === productId);
  const algorithm = algorithms.find((a) => a.id === algorithmId);

  return (
    <div className="view-fade">
      <RoadmapBanner />

      <h1 className="page-title">Detalhe do Algoritmo</h1>

      <div className="select-pair">
        <div className="filter-group">
          <label>Produto</label>
          <select value={productId} onChange={(e) => setProductId(e.target.value)}>
            {products.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <label>Algoritmo</label>
          <select
            value={algorithmId}
            onChange={(e) => setAlgorithmId(e.target.value)}
            disabled={algorithmsForProduct.length === 0}
          >
            {algorithmsForProduct.length === 0 ? (
              <option>Nenhum algoritmo documentado</option>
            ) : (
              algorithmsForProduct.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name}
                </option>
              ))
            )}
          </select>
        </div>
      </div>

      {!algorithm || !product ? (
        <div className="warning-box">Nenhum algoritmo documentado para este produto ainda.</div>
      ) : (
        <>
          <div className="breadcrumb">
            Produtos &gt; {product.name} &gt; {algorithm.name}
          </div>

          <hr className="divider" />

          <div className="product-card-header" style={{ marginBottom: 6 }}>
            <div>
              <h2 style={{ margin: 0, letterSpacing: "-0.3px" }}>{algorithm.name}</h2>
              <p className="page-subtitle">Produto: {product.name}</p>
            </div>
            <div style={{ textAlign: "right" }}>
              <PhaseBadge phase={algorithm.phase} />
              <div className="page-subtitle" style={{ marginTop: 4 }}>
                {algorithm.status}
              </div>
            </div>
          </div>

          <div style={{ display: "flex", gap: 32, marginBottom: 18 }}>
            <div className="page-subtitle">
              <strong>Última execução:</strong> {algorithm.last_run}
            </div>
            <div className="page-subtitle">
              <strong>Último treinamento:</strong> {algorithm.last_training}
            </div>
          </div>

          <div className="tabs">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                className={`tab-btn ${activeTab === tab.id ? "active" : ""}`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {activeTab === "functional" && <FunctionalTab algorithm={algorithm} />}
          {activeTab === "technical" && <TechnicalTab algorithm={algorithm} />}
          {activeTab === "table" && <TableTab algorithm={algorithm} />}
          {activeTab === "metrics" && <MetricsTab algorithm={algorithm} />}
          {activeTab === "value" && <ValueTab algorithm={algorithm} />}
        </>
      )}
    </div>
  );
}

function FunctionalTab({ algorithm }: { algorithm: Algorithm }) {
  const f = algorithm.functional;
  return (
    <div>
      <strong>Problema resolvido</strong>
      <p>{f.problem_solved}</p>
      <strong>Decisão suportada</strong>
      <p>{f.decision_supported}</p>
      <strong>Usuários</strong>
      <ul className="plain-list">
        {f.users.map((u) => (
          <li key={u}>{u}</li>
        ))}
      </ul>
      <div className="grid grid-2">
        <div>
          <strong>Granularidade</strong>
          <p>{f.granularity}</p>
        </div>
        <div>
          <strong>Frequência de atualização</strong>
          <p>{f.update_frequency}</p>
        </div>
      </div>
      <strong>Explicação não técnica</strong>
      <div className="info-box" style={{ marginTop: 6, marginBottom: 14 }}>
        {f.plain_explanation}
      </div>
      <strong>Limitações conhecidas</strong>
      <div className="warning-box" style={{ marginTop: 6 }}>
        {f.known_limitations}
      </div>
    </div>
  );
}

function TechnicalTab({ algorithm }: { algorithm: Algorithm }) {
  const t = algorithm.technical;
  return (
    <div>
      <strong>Pipeline</strong>
      <pre
        style={{
          background: "var(--page-bg)",
          padding: 12,
          borderRadius: 8,
          whiteSpace: "pre-wrap",
          fontSize: "0.82rem",
        }}
      >
        {t.pipeline}
      </pre>
      <strong>Algoritmo / Modelo</strong>
      <p>{t.model}</p>
      <div className="grid grid-2">
        <div>
          <strong>Target</strong>
          <p>{t.target}</p>
          <strong>Janela de observação</strong>
          <p>{t.observation_window}</p>
          <strong>Estratégia de validação</strong>
          <p>{t.validation_strategy}</p>
        </div>
        <div>
          <strong>Janela de previsão</strong>
          <p>{t.prediction_window}</p>
          <strong>Método de calibração</strong>
          <p>{t.calibration_method}</p>
          <strong>Periodicidade de retraining</strong>
          <p>{t.retraining_frequency}</p>
        </div>
      </div>
      <strong>Features principais</strong>
      <ul className="plain-list">
        {t.main_features.map((feat) => (
          <li key={feat}>{feat}</li>
        ))}
      </ul>
      <strong>Regras de pós-processamento</strong>
      <p>{t.postprocessing_rules}</p>
    </div>
  );
}

function TableTab({ algorithm }: { algorithm: Algorithm }) {
  const out = algorithm.output_table;
  return (
    <div>
      <strong>
        Tabela: <code>{out.name}</code>
      </strong>
      <p className="page-subtitle">Caminho Unity Catalog: {out.unity_catalog_path}</p>
      <p className="page-subtitle">
        Exemplos abaixo são sintéticos/mascarados — não representam dados reais de cliente.
      </p>
      {out.columns.length === 0 ? (
        <div className="info-box">Nenhuma coluna documentada para esta tabela.</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Coluna</th>
              <th>Tipo</th>
              <th>Descrição</th>
              <th>Exemplo (sintético)</th>
            </tr>
          </thead>
          <tbody>
            {out.columns.map((col) => (
              <tr key={col.name}>
                <td>{col.name}</td>
                <td>{col.type}</td>
                <td>{col.description}</td>
                <td>{col.example}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

function MetricsTab({ algorithm }: { algorithm: Algorithm }) {
  const m = algorithm.technical_metrics;
  return (
    <div className="grid grid-2">
      <div>
        <strong>Performance do modelo</strong>
        <ul className="plain-list">
          {m.model_performance.map((p) => (
            <li key={p}>{p}</li>
          ))}
        </ul>
        <strong>Cobertura</strong>
        <p>{m.coverage}</p>
      </div>
      <div>
        <strong>Qualidade operacional</strong>
        <p>{m.operational_quality}</p>
        <strong>Drift e estabilidade</strong>
        <p>{m.drift_stability}</p>
      </div>
    </div>
  );
}

function ValueTab({ algorithm }: { algorithm: Algorithm }) {
  const v = algorithm.business_value;
  return (
    <div>
      <div className="info-box">{v.note}</div>
      <strong style={{ display: "block", marginTop: 14 }}>Métricas de valor acompanhadas</strong>
      <ul className="plain-list">
        {v.metrics.map((metric) => (
          <li key={metric}>{metric}</li>
        ))}
      </ul>
    </div>
  );
}
