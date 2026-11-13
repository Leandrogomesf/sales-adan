import type { ReactNode } from "react";

const COLORS: Record<string, [string, string]> = {
  brand: ["#2563eb", "var(--brand-soft)"],
  accent: ["#6d5efc", "var(--accent-soft)"],
  green: ["#16a34a", "var(--green-soft)"],
  orange: ["#ea580c", "var(--orange-soft)"],
};

interface KpiCardProps {
  icon: ReactNode;
  label: string;
  value: string;
  color?: keyof typeof COLORS;
}

export function KpiCard({ icon, label, value, color = "brand" }: KpiCardProps) {
  const [iconColor, iconBg] = COLORS[color] ?? COLORS.brand;
  return (
    <div className="card kpi-card">
      <div className="icon-badge" style={{ backgroundColor: iconBg, color: iconColor }}>
        {icon}
      </div>
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
    </div>
  );
}
