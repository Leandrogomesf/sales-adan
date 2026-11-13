import initiativeData from "../data/initiative.json";
import roadmapData from "../data/roadmap.json";
import type { Initiative, RoadmapInitiative } from "../types";
import { RoadmapBanner } from "../components/RoadmapBanner";
import { KpiCard } from "../components/KpiCard";
import { TargetIcon, UsersIcon, PuzzleIcon, ClockIcon } from "../components/icons";
import { useState } from "react";

const initiative = initiativeData as Initiative;
const roadmap = roadmapData.initiatives as RoadmapInitiative[];

const KPI_STYLE: Record<string, { icon: JSX.Element; color: "brand" | "accent" | "green" | "orange" }> = {
  Objetivo: { icon: <TargetIcon />, color: "brand" },
  "Público impactado": { icon: <UsersIcon />, color: "accent" },
  "Produtos ativos": { icon: <PuzzleIcon />, color: "green" },
  "Última atualização": { icon: <ClockIcon />, color: "orange" },
};

export function OverviewPage() {
  const [onlyPrioritized, setOnlyPrioritized] = useState(false);
  const [onlyWithDetail, setOnlyWithDetail] = useState(false);

  let filteredRoadmap = roadmap;
  if (onlyPrioritized) filteredRoadmap = filteredRoadmap.filter((i) => i.prioritized_in_edf);
  if (onlyWithDetail) filteredRoadmap = filteredRoadmap.filter((i) => i.product_id);

  return (
    <div className="view-fade">
      <RoadmapBanner />

      <h1 className="page-title">{initiative.name}</h1>
      <p className="page-subtitle">{initiative.tagline}</p>
      <p className="page-subtitle">Última atualização: {initiative.last_updated}</p>

      <hr className="divider" />

      <div className="section-title">Visão executiva</div>
      <div className="grid grid-4">
        {initiative.executive_cards.map((card) => {
          const style = KPI_STYLE[card.label] ?? { icon: <TargetIcon />, color: "brand" as const };
          return (
            <KpiCard key={card.label} icon={style.icon} label={card.label} value={card.value} color={style.color} />
          );
        })}
      </div>

      <hr className="divider" />

      <div className="section-title">Objetivo da iniciativa</div>
      <p>{initiative.description}</p>

      <div className="section-title">Áreas impactadas</div>
      <p>{initiative.impacted_areas.join(", ")}</p>

      <hr className="divider" />

      <div className="section-title">Time e responsáveis</div>
      <table className="data-table">
        <thead>
          <tr>
            <th>Papel</th>
            <th>Responsável</th>
            <th>Responsabilidade</th>
          </tr>
        </thead>
        <tbody>
          {initiative.team.map((member) => (
            <tr key={member.role}>
              <td>{member.role}</td>
              <td>{member.name}</td>
              <td>{member.responsibility}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <hr className="divider" />

      <div className="section-title">{initiative.pilot_results.title}</div>
      <p className="page-subtitle">
        Período de referência: {initiative.pilot_results.reference_period} · Fonte:{" "}
        {initiative.pilot_results.source}
      </p>
      <div className="warning-box" style={{ marginBottom: 14 }}>
        {initiative.pilot_results.note}
      </div>
      <table className="data-table">
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Fev</th>
            <th>Mar</th>
            <th>Abr</th>
            <th>Tendência</th>
          </tr>
        </thead>
        <tbody>
          {initiative.pilot_results.metrics.map((m) => (
            <tr key={m.name}>
              <td>{m.name}</td>
              <td>{m.fev}</td>
              <td>{m.mar}</td>
              <td>{m.abr}</td>
              <td>{m.trend}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <hr className="divider" />

      <details className="card" style={{ marginBottom: 16 }}>
        <summary style={{ cursor: "pointer", fontWeight: 600 }}>OKR da iniciativa (PUDMA)</summary>
        <div style={{ marginTop: 14 }}>
          <strong>Problema</strong>
          <p>{initiative.okr.problem}</p>
          <strong>Usuários</strong>
          <ul className="plain-list">
            {initiative.okr.users.map((u) => (
              <li key={u}>{u}</li>
            ))}
          </ul>
          <strong>Decisões suportadas</strong>
          <ul className="plain-list">
            {initiative.okr.decisions.map((d) => (
              <li key={d}>{d}</li>
            ))}
          </ul>
          <strong>Key Results</strong>
          <table className="data-table">
            <thead>
              <tr>
                <th>Key Result</th>
                <th>Baseline</th>
                <th>Meta</th>
                <th>Prazo</th>
              </tr>
            </thead>
            <tbody>
              {initiative.okr.key_results.map((kr) => (
                <tr key={kr.kr}>
                  <td>{kr.kr}</td>
                  <td>{kr.baseline}</td>
                  <td>{kr.target}</td>
                  <td>{kr.deadline}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>

      <details className="card" style={{ marginBottom: 16 }}>
        <summary style={{ cursor: "pointer", fontWeight: 600 }}>Glossário</summary>
        <table className="data-table" style={{ marginTop: 14 }}>
          <thead>
            <tr>
              <th>Termo</th>
              <th>Definição</th>
            </tr>
          </thead>
          <tbody>
            {initiative.glossary.map((g) => (
              <tr key={g.term}>
                <td>{g.term}</td>
                <td>{g.definition}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </details>

      <hr className="divider" />

      <div className="section-title">Evolução do portfólio</div>
      <p className="page-subtitle">Fonte: planilha mestre de iniciativas Sales ADAN 2026-2027</p>

      <div style={{ display: "flex", gap: 20, margin: "12px 0 16px" }}>
        <label style={{ display: "flex", alignItems: "center", gap: 6, fontSize: "0.88rem" }}>
          <input
            type="checkbox"
            checked={onlyPrioritized}
            onChange={(e) => setOnlyPrioritized(e.target.checked)}
          />
          Mostrar apenas priorizadas no EDF
        </label>
        <label style={{ display: "flex", alignItems: "center", gap: 6, fontSize: "0.88rem" }}>
          <input
            type="checkbox"
            checked={onlyWithDetail}
            onChange={(e) => setOnlyWithDetail(e.target.checked)}
          />
          Mostrar apenas com página de detalhe
        </label>
      </div>

      <table className="data-table">
        <thead>
          <tr>
            <th>Iniciativa</th>
            <th>Tipo de produto de dados</th>
            <th>Ponto focal</th>
            <th>Origem</th>
            <th>Duração</th>
            <th>Priorizado no EDF</th>
          </tr>
        </thead>
        <tbody>
          {filteredRoadmap.map((item) => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td>{item.data_product_type}</td>
              <td>{item.focal_point}</td>
              <td>{item.origin}</td>
              <td>{item.duration}</td>
              <td>{item.prioritized_in_edf ? "Sim" : "Não"}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="page-subtitle">
        {filteredRoadmap.length} de {roadmap.length} iniciativas exibidas. Iniciativas sem página de
        detalhe aparecem apenas aqui (roadmap/conceito).
      </p>
    </div>
  );
}
