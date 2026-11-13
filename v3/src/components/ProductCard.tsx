import type { Product } from "../types";
import { PhaseBadge, SecondaryTag, phaseProgress } from "./PhaseBadge";

interface ProductCardProps {
  product: Product;
  onOpen: (productId: string) => void;
}

export function ProductCard({ product, onOpen }: ProductCardProps) {
  return (
    <div className="card product-card">
      <div className="product-card-header">
        <div>
          <h3>{product.name}</h3>
          <div className="code">{product.code}</div>
        </div>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", justifyContent: "flex-end" }}>
          <PhaseBadge phase={product.phase} />
          {product.phase_tags.map((tag) => (
            <SecondaryTag key={tag} label={tag} />
          ))}
        </div>
      </div>

      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${phaseProgress(product.phase)}%` }} />
      </div>

      <p className="description">{product.description}</p>

      <div className="meta">
        <strong>Módulo:</strong> {product.module} · <strong>Áreas:</strong>{" "}
        {product.consuming_areas.join(", ")}
      </div>

      <button className="btn-primary" onClick={() => onOpen(product.id)}>
        Ver detalhe do produto
      </button>
    </div>
  );
}
