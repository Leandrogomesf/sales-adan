import { useState } from "react";
import type { ViewId } from "./types";
import { Sidebar } from "./components/Sidebar";
import { OverviewPage } from "./pages/OverviewPage";
import { ProductsPage } from "./pages/ProductsPage";
import { AlgorithmPage } from "./pages/AlgorithmPage";

export default function App() {
  const [view, setView] = useState<ViewId>("overview");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProductId, setSelectedProductId] = useState<string | null>(null);
  const [selectedAlgorithmId, setSelectedAlgorithmId] = useState<string | null>(null);

  function handleOpenProduct(productId: string) {
    setSelectedProductId(productId);
    setSelectedAlgorithmId(null);
    setView("algorithm");
  }

  function handleAlgorithmSelectionChange(productId: string, algorithmId: string) {
    setSelectedProductId(productId);
    setSelectedAlgorithmId(algorithmId);
  }

  return (
    <div className="app-shell">
      <Sidebar
        view={view}
        onNavigate={setView}
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
      />
      <main className="main">
        {view === "overview" && <OverviewPage />}
        {view === "products" && (
          <ProductsPage searchTerm={searchTerm} onOpenProduct={handleOpenProduct} />
        )}
        {view === "algorithm" && (
          <AlgorithmPage
            selectedProductId={selectedProductId}
            selectedAlgorithmId={selectedAlgorithmId}
            onSelectionChange={handleAlgorithmSelectionChange}
          />
        )}
      </main>
    </div>
  );
}
