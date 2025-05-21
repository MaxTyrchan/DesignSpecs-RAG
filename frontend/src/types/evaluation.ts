export interface EvaluationMetric {
  id: string;
  name: string;
  value: number;
  description: string;
  category: 'relevancy' | 'precision' | 'latency';
}

export interface QueryResponsePair {
  id: string;
  query: string;
  response: string;
  timestamp: Date;
  metrics: EvaluationMetric[];
  groundTruth?: string;
}