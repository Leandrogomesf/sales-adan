import { useState } from "react";
import productsData from "../data/products.json";
import type { Product } from "../types";
import { RoadmapBanner } from "../components/RoadmapBanner";
import { ProductCard } from "../components/ProductCard";
import { ProductFilters, applyProductFilters } from "../components/ProductFilters";
import type { ProductFilterState } from "../components/ProductFilters";

const products = productsData.products as Product[];

interface ProductsPageProps {
  searchTerm: string;
  onOpenProduct: (productId: string) => void;
}

export function ProductsPage({ searchTerm, onOpenProduct }: ProductsPageProps) {
  const [filters, setFilters] = useState<ProductFilterState>({ module: "", phase: "", area: "" });

  const filtered = applyProductFilters(products, filters, searchTerm);

  return (
    <div className="view-fade">
      <RoadmapBanner />

      <h1 className="page-title">Produtos de Dados</h1>
      <p className="page-subtitle">Catálogo de produtos de dados do portfólio Sales ADAN.</p>

      <ProductFilters products={products} filters={filters} onChange={setFilters} />

      <p className="page-subtitle">
        {filtered.length} de {products.length} produtos exibidos.
      </p>

      {filtered.length === 0 ? (
        <div className="info-box">Nenhum produto encontrado com os filtros selecionados.</div>
      ) : (
        <div className="grid grid-2">
          {filtered.map((product) => (
            <ProductCard key={product.id} product={product} onOpen={onOpenProduct} />
          ))}
        </div>
      )}
    </div>
  );
}
