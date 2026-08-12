from fastapi import APIRouter
from eval.evaluation import (
    correctness_evaluator, target, client, conciseness_evaluator,
    hallucination_evaluator, groundedness_evaluator, relevance_evaluator,
    helpfulness_evaluator
)
from typing import Dict, Any
import uuid


router = APIRouter()


@router.post("/eval")
async def trigger_evaluation() -> Dict[str, Any]:
    """Trigger a new evaluation run"""
    experiment_results = await client.aevaluate(
        target,
        # data="small_eval_dataset",
        data="eval_dataset",
        evaluators=[
            correctness_evaluator,
            conciseness_evaluator,
            hallucination_evaluator,
            groundedness_evaluator,
            relevance_evaluator,
            helpfulness_evaluator
        ],
        experiment_prefix="rag-eval",
        max_concurrency=1,
    )

    # Format the results to match our frontend's expected structure
    formatted_results = {
        "metrics": [],
        "pairs": []
    }

    # Extract evaluation results and format them
    async for result in experiment_results:
        pair = {
            "id": str(uuid.uuid4()),  # Generate a unique ID for each pair
            "query": result.get("input", {}).get("question", ""),
            "response": result.get("prediction", {}).get("answer", ""),
            "timestamp": result.get("timestamp", None),
            "metrics": []
        }

        # Add feedback scores as metrics
        feedback = result.get("feedback", {})
        if feedback:
            for key, value in feedback.items():
                pair["metrics"].append({
                    "id": key,
                    "name": key.replace("_", " ").title(),
                    "value": float(value) * 100 if value is not None else 0,
                    "description": f"Score for {key.replace('_', ' ')}",
                    "category": "precision"
                })

        formatted_results["pairs"].append(pair)

    # Calculate overall metrics
    if formatted_results["pairs"]:
        all_scores = [
            score
            for pair in formatted_results["pairs"]
            for metric in pair["metrics"]
            for score in [metric["value"]]
        ]
        if all_scores:
            formatted_results["metrics"].append({
                "id": "overall",
                "name": "Overall Correctness",
                "value": sum(all_scores) / len(all_scores),
                "description": "Average correctness score across all evaluations",
                "category": "precision"
            })

    return formatted_results
