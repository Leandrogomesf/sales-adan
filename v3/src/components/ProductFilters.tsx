import type { Product } from "../types";

export interface ProductFilterState {
  module: string;
  phase: string;
  area: string;
}

interface ProductFiltersProps {
  products: Product[];
  filters: ProductFilterState;
  onChange: (filters: ProductFilterState) => void;
}

export function ProductFilters({ products, filters, onChange }: ProductFiltersProps) {
  const modules = Array.from(new Set(products.map((p) => p.module))).sort();
  const phases = Array.from(new Set(products.map((p) => p.phase))).sort();
  const areas = Array.from(new Set(products.flatMap((p) => p.consuming_areas))).sort();

  return (
    <div className="filters-row">
      <div className="filter-group">
        <label>Módulo</label>
        <select
          value={filters.module}
          onChange={(e) => onChange({ ...filters, module: e.target.value })}
        >
          <option value="">Todos</option>
          {modules.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
      </div>
      <div className="filter-group">
        <label>Fase</label>
        <select
          value={filters.phase}
          onChange={(e) => onChange({ ...filters, phase: e.target.value })}
        >
          <option value="">Todas</option>
          {phases.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
      </div>
      <div className="filter-group">
        <label>Área consumidora</label>
        <select
          value={filters.area}
          onChange={(e) => onChange({ ...filters, area: e.target.value })}
        >
          <option value="">Todas</option>
          {areas.map((a) => (
            <option key={a} value={a}>
              {a}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

export function applyProductFilters(
  products: Product[],
  filters: ProductFilterState,
  searchTerm: string
): Product[] {
  let result = products;
  if (filters.module) result = result.filter((p) => p.module === filters.module);
  if (filters.phase) result = result.filter((p) => p.phase === filters.phase);
  if (filters.area) result = result.filter((p) => p.consuming_areas.includes(filters.area));
  if (searchTerm.trim()) {
    const term = searchTerm.trim().toLowerCase();
    result = result.filter(
      (p) => p.name.toLowerCase().includes(term) || p.description.toLowerCase().includes(term)
    );
  }
  return result;
}
