import roadmapPhases from "../data/roadmapPhases.json";
import type { RoadmapPhases } from "../types";
import { PHASE_COLORS } from "./PhaseBadge";
import type { Phase } from "../types";

const data = roadmapPhases as RoadmapPhases;

const MONTH_LABELS: Record<string, string> = {
  "01": "Jan", "02": "Fev", "03": "Mar", "04": "Abr",
  "05": "Mai", "06": "Jun", "07": "Jul", "08": "Ago",
  "09": "Set", "10": "Out", "11": "Nov", "12": "Dez",
};

function formatStartDate(startDate: string): string {
  const [year, month] = startDate.split("-");
  return `${MONTH_LABELS[month] ?? month}/${year.slice(2)}`;
}

export function RoadmapBanner() {
  return (
    <details className="card roadmap-banner">
      <summary>🗺️ Roadmap de maturidade do portfólio</summary>
      <div className="roadmap-body grid grid-4">
        {data.phase_order.map((phase) => {
          const color = PHASE_COLORS[phase as Phase] ?? "var(--muted-2)";
          const items = data.items
            .filter((i) => i.phase === phase)
            .sort((a, b) => a.start_date.localeCompare(b.start_date));
          return (
            <div key={phase}>
              <div className="roadmap-col-header" style={{ borderTopColor: color }}>
                {data.phase_labels[phase]}
              </div>
              {items.map((item) => (
                <div className="roadmap-item" key={item.name}>
                  {item.name} · {formatStartDate(item.start_date)}
                </div>
              ))}
            </div>
          );
        })}
      </div>
    </details>
  );
}
