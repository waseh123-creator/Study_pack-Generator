"""
prompts.py
Prompt builders for each stage of the study-pack workflow.
"""

import json


def _json_context(context: dict, keys: list[str]) -> str:
    selected = {key: context.get(key) for key in keys}
    return json.dumps(selected, ensure_ascii=False, indent=2)


def build_prompt(stage: str, context: dict) -> str:
    """Return the prompt for a named workflow stage."""

    if stage == "planning":
        user = context["user_input"]
        return f"""
You are the PLANNING agent in a personalized AI study-pack system.

Create a practical learning plan before any content is generated.

Student input:
{json.dumps(user, ensure_ascii=False, indent=2)}

Return ONLY valid JSON:
{{
  "goal": "...",
  "learning_objectives": ["...", "..."],
  "difficulty": "...",
  "recommended_order": ["...", "..."],
  "sections": ["..."],
  "question_count": 10,
  "personalization_notes": ["..."]
}}

Make the plan match the subject, topic, level, language and selected sections.
"""

    if stage == "content":
        return f"""
You are the CONTENT GENERATION agent.

Generate the educational material according to the plan below.

{_json_context(context, ["user_input", "plan"])}

Selected components must be respected exactly.
Make explanations accurate, useful and appropriate for the student's level.

Return ONLY valid JSON:
{{
  "title": "...",
  "overview": "...",
  "sections": [
    {{
      "type": "Summary / Notes",
      "title": "...",
      "content": "..."
    }}
  ]
}}

For flashcards, MCQs and other structured material, keep the content clearly
numbered and easy to render.
"""

    if stage == "assessment":
        return f"""
You are the ASSESSMENT agent.

Use the generated content and learning plan to create assessment material.
Do not introduce concepts that were not taught unless they are clearly useful
as a reasonable application question.

Context:
{_json_context(context, ["user_input", "plan", "content"])}

Return ONLY valid JSON:
{{
  "questions": [
    {{
      "number": 1,
      "type": "MCQ",
      "question": "...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "answer": "...",
      "explanation": "..."
    }}
  ],
  "answer_key": ["1: B"],
  "assessment_notes": "..."
}}

Respect the requested question count where applicable.
"""

    if stage == "review":
        return f"""
You are the REVIEW agent and quality controller.

Review the generated study pack and assessment against the student's input
and the original plan.

Context:
{_json_context(context, ["user_input", "plan", "content", "assessment"])}

Check:
- factual consistency
- relevance to topic
- difficulty alignment
- language alignment
- missing requested sections
- duplicate questions
- ambiguous MCQs
- incorrect answer keys
- poor explanations
- unsupported claims

Return ONLY valid JSON:
{{
  "approved": true,
  "issues": [],
  "corrections": [],
  "quality_summary": "..."
}}

If there are problems, list precise corrections.
"""

    if stage == "refinement":
        return f"""
You are the FINAL REFINEMENT agent.

Produce the final polished study pack using the original request, plan,
generated content, assessment and review findings.

Context:
{_json_context(context, ["user_input", "plan", "content", "assessment", "review"])}

Apply valid review corrections. Do not invent unsupported information.
Keep the output concise enough to be useful while preserving important detail.

Return ONLY valid JSON:
{{
  "title": "...",
  "overview": "...",
  "sections": [
    {{
      "type": "...",
      "title": "...",
      "content": "..."
    }}
  ],
  "assessment": {{
    "questions": [],
    "answer_key": []
  }},
  "quality_notes": "..."
}}
"""

    raise ValueError(f"Unknown workflow stage: {stage}")
