export type Phase = "discovery" | "explore" | "poc" | "pilot" | "mvp" | "sustain";

export interface ExecutiveCard {
  label: string;
  value: string;
}

export interface PilotMetric {
  name: string;
  fev: string;
  mar: string;
  abr: string;
  trend: string;
}

export interface TeamMember {
  role: string;
  name: string;
  responsibility: string;
}

export interface KeyResult {
  kr: string;
  baseline: string;
  target: string;
  deadline: string;
}

export interface GlossaryTerm {
  term: string;
  definition: string;
}

export interface Initiative {
  name: string;
  tagline: string;
  last_updated: string;
  objective: string;
  description: string;
  executive_cards: ExecutiveCard[];
  impacted_areas: string[];
  team: TeamMember[];
  pilot_results: {
    title: string;
    reference_period: string;
    source: string;
    note: string;
    metrics: PilotMetric[];
  };
  okr: {
    problem: string;
    users: string[];
    decisions: string[];
    key_results: KeyResult[];
  };
  glossary: GlossaryTerm[];
}

export interface RoadmapInitiative {
  id: number;
  name: string;
  type: string;
  focal_point: string;
  data_product_type: string;
  in_edf: boolean;
  prioritized_in_edf: boolean;
  origin: string;
  duration: string;
  product_id: string | null;
}

export interface Product {
  id: string;
  name: string;
  code: string;
  status: string;
  phase: Phase;
  phase_tags: string[];
  module: string;
  consuming_areas: string[];
  business_owner: string;
  technical_owner: string;
  description: string;
  business_objective: string;
  algorithms: string[];
  tables: string[];
  consumption: string[];
  source_docs: string[];
}

export interface OutputColumn {
  name: string;
  type: string;
  description: string;
  example: string;
}

export interface Algorithm {
  id: string;
  name: string;
  product_id: string;
  status: string;
  phase: Phase;
  last_run: string;
  last_training: string;
  functional: {
    problem_solved: string;
    decision_supported: string;
    users: string[];
    granularity: string;
    update_frequency: string;
    plain_explanation: string;
    known_limitations: string;
  };
  technical: {
    pipeline: string;
    model: string;
    target: string;
    observation_window: string;
    prediction_window: string;
    main_features: string[];
    validation_strategy: string;
    calibration_method: string;
    postprocessing_rules: string;
    retraining_frequency: string;
  };
  output_table: {
    name: string;
    unity_catalog_path: string;
    columns: OutputColumn[];
  };
  technical_metrics: {
    model_performance: string[];
    coverage: string;
    operational_quality: string;
    drift_stability: string;
  };
  business_value: {
    note: string;
    metrics: string[];
  };
}

export interface RoadmapPhaseItem {
  name: string;
  phase: string;
  start_date: string;
  product_id: string;
}

export interface RoadmapPhases {
  phase_order: string[];
  phase_labels: Record<string, string>;
  items: RoadmapPhaseItem[];
}

export type ViewId = "overview" | "products" | "algorithm";
