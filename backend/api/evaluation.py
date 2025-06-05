from fastapi import APIRouter
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class MetricCategory(str, Enum):
    relevancy = "relevancy"
    precision = "precision"
    latency = "latency"

class EvaluationMetric(BaseModel):
    id: str
    name: str
    value: float
    description: str
    category: MetricCategory

class QueryResponsePair(BaseModel):
    id: str
    query: str
    response: str
    timestamp: datetime
    metrics: List[EvaluationMetric]
    groundTruth: Optional[str] = None

class EvaluationResponse(BaseModel):
    metrics: List[EvaluationMetric]
    pairs: List[QueryResponsePair]

@router.get("/evaluation", response_model=EvaluationResponse)
async def get_evaluation_data():
    """Return evaluation metrics and query/response pairs."""
    metrics = [
        EvaluationMetric(
            id="1",
            name="Overall Accuracy",
            value=87,
            description="How accurate the responses are across all queries",
            category=MetricCategory.relevancy,
        ),
        EvaluationMetric(
            id="2",
            name="Context Usage",
            value=92,
            description="How effectively the model uses the provided context",
            category=MetricCategory.precision,
        ),
        EvaluationMetric(
            id="3",
            name="Response Time",
            value=35,
            description="Average time to generate responses",
            category=MetricCategory.latency,
        ),
    ]

    pairs = [
        QueryResponsePair(
            id="1",
            query="What are the key factors affecting global climate change?",
            response="Greenhouse gas emissions and deforestation are among the main factors.",
            timestamp=datetime.utcnow(),
            metrics=[
                EvaluationMetric(
                    id="101",
                    name="Relevancy",
                    value=92,
                    description="How relevant the response is to the query",
                    category=MetricCategory.relevancy,
                )
            ],
            groundTruth="Greenhouse gases and land use changes drive global climate change.",
        )
    ]

    return EvaluationResponse(metrics=metrics, pairs=pairs)
