import type { Phase } from "../types";

export const PHASE_LABELS: Record<Phase, string> = {
  discovery: "Discovery",
  explore: "Explore",
  poc: "PoC",
  pilot: "Pilot",
  mvp: "MVP",
  sustain: "Sustain",
};

export const PHASE_COLORS: Record<Phase, string> = {
  discovery: "var(--phase-discovery)",
  explore: "var(--phase-explore)",
  poc: "var(--phase-poc)",
  pilot: "var(--phase-pilot)",
  mvp: "var(--phase-mvp)",
  sustain: "var(--phase-sustain)",
};

export const PHASE_ORDER: Phase[] = ["discovery", "explore", "poc", "pilot", "mvp", "sustain"];

export function phaseProgress(phase: Phase): number {
  const idx = PHASE_ORDER.indexOf(phase);
  if (idx === -1) return 0;
  return ((idx + 1) / PHASE_ORDER.length) * 100;
}

export function PhaseBadge({ phase }: { phase: Phase }) {
  const color = PHASE_COLORS[phase] ?? "var(--muted-2)";
  return (
    <span
      className="badge"
      style={{ backgroundColor: `color-mix(in srgb, ${color} 15%, white)`, color, border: `1px solid ${color}` }}
    >
      {PHASE_LABELS[phase] ?? phase}
    </span>
  );
}

export function SecondaryTag({ label }: { label: string }) {
  return <span className="badge-secondary">{label}</span>;
}
