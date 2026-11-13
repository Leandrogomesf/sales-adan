import type { ViewId } from "../types";
import { HomeIcon, GridIcon, FlaskIcon } from "./icons";
import { SearchBar } from "./SearchBar";

interface SidebarProps {
  view: ViewId;
  onNavigate: (view: ViewId) => void;
  searchTerm: string;
  onSearchChange: (term: string) => void;
}

const NAV_ITEMS: { id: ViewId; label: string; icon: JSX.Element }[] = [
  { id: "overview", label: "Visão Geral", icon: <HomeIcon /> },
  { id: "products", label: "Produtos de Dados", icon: <GridIcon /> },
  { id: "algorithm", label: "Detalhe do Algoritmo", icon: <FlaskIcon /> },
];

export function Sidebar({ view, onNavigate, searchTerm, onSearchChange }: SidebarProps) {
  return (
    <aside className="sidebar">
      <div style={{ marginBottom: 14 }}>
        <SearchBar
          value={searchTerm}
          onChange={(term) => {
            onSearchChange(term);
            if (term.trim()) onNavigate("products");
          }}
        />
      </div>
      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            className={`sidebar-link ${view === item.id ? "active" : ""}`}
            onClick={() => onNavigate(item.id)}
          >
            {item.icon}
            {item.label}
          </button>
        ))}
      </nav>
      <div className="sidebar-footer">
        <img src="/pepsico-logo.png" alt="PepsiCo" />
      </div>
    </aside>
  );
}
