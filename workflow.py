"""
workflow.py
Multi-stage AI workflow for personalized study-pack generation.

Stages:
1. Planning
2. Content Generation
3. Assessment
4. Review
5. Refinement

The workflow passes context from one stage to the next.
"""

import json
import re
from typing import Any, Dict, List, Callable


def clean_json(text: str) -> str:
    """Extract JSON from a model response that may contain markdown fences."""
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def parse_json(text: str, fallback: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Safely parse model JSON and return a fallback object on failure."""
    try:
        return json.loads(clean_json(text))
    except (json.JSONDecodeError, TypeError):
        return fallback if fallback is not None else {}


def call_ai(client, model: str, prompt: str) -> str:
    """Single AI gateway used by every workflow stage."""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("The AI returned an empty response.")
    return text


def run_stage(
    name: str,
    client,
    model: str,
    prompt: str,
    fallback: Dict[str, Any],
) -> Dict[str, Any]:
    """Run one stage with consistent error handling."""
    try:
        raw = call_ai(client, model, prompt)
        result = parse_json(raw)

        if not result:
            raise ValueError(f"{name} returned invalid or empty JSON.")

        result["_stage_status"] = "success"
        return result

    except Exception as exc:
        # Preserve workflow context rather than crashing the entire app.
        fallback = dict(fallback)
        fallback["_stage_status"] = "error"
        fallback["_error"] = f"{name}: {exc}"
        return fallback


def run_workflow(
    client,
    model: str,
    user_input: Dict[str, Any],
    prompt_builder: Callable[[str, Dict[str, Any]], str],
) -> Dict[str, Any]:
    """
    Execute the complete multi-stage workflow.

    Context is explicitly passed forward:
    user_input -> plan -> content -> assessment -> review -> refinement
    """

    context: Dict[str, Any] = {"user_input": user_input}
    errors: List[str] = []

    # -------------------------
    # STAGE 1: PLANNING
    # -------------------------
    plan_prompt = prompt_builder("planning", context)
    plan = run_stage(
        "Planning stage",
        client,
        model,
        plan_prompt,
        fallback={
            "goal": user_input.get("topic", "Study topic"),
            "learning_objectives": [f"Understand {user_input.get('topic', 'the topic')}"],
            "difficulty": user_input.get("level", "Intermediate"),
            "sections": user_input.get("selected_components", []),
            "question_count": user_input.get("question_count", 10),
        },
    )
    context["plan"] = plan
    if plan.get("_stage_status") == "error":
        errors.append(plan.get("_error", "Planning stage failed."))

    # -------------------------
    # STAGE 2: CONTENT
    # -------------------------
    content_prompt = prompt_builder("content", context)
    content = run_stage(
        "Content generation stage",
        client,
        model,
        content_prompt,
        fallback={
            "title": f"{user_input.get('topic', 'Study')} Study Pack",
            "overview": "Content generation could not be completed.",
            "sections": [],
        },
    )
    context["content"] = content
    if content.get("_stage_status") == "error":
        errors.append(content.get("_error", "Content generation failed."))

    # -------------------------
    # STAGE 3: ASSESSMENT
    # -------------------------
    assessment_prompt = prompt_builder("assessment", context)
    assessment = run_stage(
        "Assessment stage",
        client,
        model,
        assessment_prompt,
        fallback={
            "questions": [],
            "answer_key": [],
            "assessment_notes": "Assessment generation failed.",
        },
    )
    context["assessment"] = assessment
    if assessment.get("_stage_status") == "error":
        errors.append(assessment.get("_error", "Assessment stage failed."))

    # -------------------------
    # STAGE 4: REVIEW
    # -------------------------
    review_prompt = prompt_builder("review", context)
    review = run_stage(
        "Review stage",
        client,
        model,
        review_prompt,
        fallback={
            "approved": False,
            "issues": ["Review stage could not be completed."],
            "corrections": [],
        },
    )
    context["review"] = review
    if review.get("_stage_status") == "error":
        errors.append(review.get("_error", "Review stage failed."))

    # -------------------------
    # STAGE 5: REFINEMENT
    # -------------------------
    refinement_prompt = prompt_builder("refinement", context)
    refinement = run_stage(
        "Refinement stage",
        client,
        model,
        refinement_prompt,
        fallback={
            "title": f"{user_input.get('topic', 'Study')} Study Pack",
            "overview": "Final refinement could not be completed.",
            "sections": content.get("sections", []),
            "assessment": assessment,
        },
    )
    context["refinement"] = refinement
    if refinement.get("_stage_status") == "error":
        errors.append(refinement.get("_error", "Refinement stage failed."))

    context["errors"] = errors
    context["workflow_status"] = "completed_with_errors" if errors else "completed"

    return context
