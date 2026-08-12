export interface EvaluationMetric {
  id: string;
  name: string;
  value: number;
  description: string;
  category: "relevancy" | "precision" | "latency" | "ragas" | "openevals";
  source?: "ragas" | "openevals";
}

export interface QueryResponsePair {
  id: string;
  query: string;
  response: string;
  timestamp: Date;
  metrics: EvaluationMetric[];
  groundTruth?: string;
}

export type EvaluationType = "openevals" | "ragas" | "hybrid";

export interface EvaluationResponse {
  metrics: EvaluationMetric[];
  pairs: QueryResponsePair[];
  evaluation_type?: string;
  evaluation_summary?: {
    openevals_metrics_count?: number;
    ragas_metrics_count?: number;
    total_pairs_evaluated?: number;
    examples_evaluated?: number;
  };
  ragas_scores?: Record<string, number>;
  examples_evaluated?: number;
}
