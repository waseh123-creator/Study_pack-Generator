"""
app.py
Main Streamlit application for AI Study Pack Generator.

Run locally:
    streamlit run app.py

Streamlit deployment:
    Add GEMINI_API_KEY in Streamlit Secrets.
"""

import os
from typing import Any

import streamlit as st
from google import genai

from prompts import build_prompt
from workflow import run_workflow


APP_TITLE = "AI Study Pack Generator"
DEFAULT_MODEL = "gemini-2.5-flash"

PACK_OPTIONS = [
    "Summary / Notes",
    "Key Concepts",
    "Flashcards",
    "MCQs",
    "Short Questions",
    "Long Questions",
    "True / False",
    "Study Plan",
]

LEVELS = ["Beginner", "Intermediate", "Advanced"]
LANGUAGES = ["English", "Roman Urdu", "Urdu"]


def get_api_key() -> str:
    """Read the API key from Streamlit Secrets or environment variables."""
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        secret_key = ""

    return (secret_key or os.getenv("GEMINI_API_KEY", "")).strip()


def create_client(api_key: str):
    if not api_key:
        raise ValueError(
            "Gemini API key is missing. Add GEMINI_API_KEY to Streamlit Secrets."
        )
    return genai.Client(api_key=api_key)


def validate_inputs(subject: str, topic: str, components: list[str]) -> list[str]:
    errors = []

    if not subject.strip():
        errors.append("Please enter a subject.")

    if not topic.strip():
        errors.append("Please enter a topic.")

    if not components:
        errors.append("Select at least one study-pack component.")

    return errors


def md_content(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return str(content)


def render_final_pack(result: dict):
    final = result.get("refinement", {})

    st.subheader(final.get("title", "Your Study Pack"))

    overview = final.get("overview")
    if overview:
        st.markdown("### Overview")
        st.markdown(md_content(overview))

    for section in final.get("sections", []):
        section_type = section.get("type", "Study Material")
        title = section.get("title", section_type)
        content = section.get("content", "")

        st.markdown(f"## {title}")
        st.caption(section_type)
        st.markdown(md_content(content))

    assessment = final.get("assessment", {})
    questions = assessment.get("questions", [])

    if questions:
        st.markdown("## Assessment")

        for q in questions:
            number = q.get("number", "")
            qtype = q.get("type", "Question")
            question = q.get("question", "")

            st.markdown(f"### {number}. {qtype}")
            st.markdown(question)

            options = q.get("options", [])
            if options:
                for option in options:
                    st.markdown(f"- {option}")

            answer = q.get("answer")
            explanation = q.get("explanation")

            if answer:
                st.markdown(f"**Answer:** {answer}")
            if explanation:
                st.markdown(f"**Explanation:** {explanation}")

    quality_notes = final.get("quality_notes")
    if quality_notes:
        st.info(f"Quality review: {quality_notes}")


def render_workflow_status(result: dict):
    st.markdown("### Workflow Status")

    stages = [
        ("Planning", result.get("plan", {})),
        ("Content Generation", result.get("content", {})),
        ("Assessment", result.get("assessment", {})),
        ("Review", result.get("review", {})),
        ("Refinement", result.get("refinement", {})),
    ]

    cols = st.columns(len(stages))

    for col, (name, data) in zip(cols, stages):
        status = data.get("_stage_status", "unknown")
        icon = "✅" if status == "success" else "⚠️"
        col.metric(name, icon)


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="📚",
        layout="wide",
    )

    st.title("📚 AI Study Pack Generator")
    st.write(
        "Generate a personalized study pack through a multi-stage AI workflow: "
        "planning → content → assessment → review → refinement."
    )

    with st.sidebar:
        st.header("Study Configuration")

        api_key = get_api_key()

        if api_key:
            st.success("Gemini API key loaded from Secrets.")
        else:
            st.warning("Add GEMINI_API_KEY to Streamlit Secrets.")

        model = st.text_input(
            "Gemini Model",
            value=DEFAULT_MODEL,
            help="Change this only if your Gemini account supports another model.",
        )

        subject = st.text_input(
            "Subject",
            placeholder="e.g. Database Systems",
        )

        topic = st.text_input(
            "Topic",
            placeholder="e.g. Normalization",
        )

        level = st.selectbox(
            "Academic Level",
            LEVELS,
            index=1,
        )

        language = st.selectbox(
            "Language",
            LANGUAGES,
        )

        components = st.multiselect(
            "Study Pack Components",
            PACK_OPTIONS,
            default=[
                "Summary / Notes",
                "Key Concepts",
                "Flashcards",
                "MCQs",
            ],
        )

        question_count = st.slider(
            "Question Count",
            min_value=5,
            max_value=20,
            value=10,
            step=5,
        )

        extra_instructions = st.text_area(
            "Additional Instructions",
            placeholder="e.g. Make it exam-oriented and include practical examples.",
        )

        generate = st.button(
            "🚀 Generate Study Pack",
            type="primary",
            use_container_width=True,
        )

    if generate:
        errors = validate_inputs(subject, topic, components)

        if not api_key:
            errors.append("GEMINI_API_KEY is not configured in Streamlit Secrets.")

        if errors:
            for error in errors:
                st.error(error)
            return

        user_input = {
            "subject": subject.strip(),
            "topic": topic.strip(),
            "level": level,
            "language": language,
            "selected_components": components,
            "question_count": question_count,
            "extra_instructions": extra_instructions.strip(),
        }

        try:
            client = create_client(api_key)

            with st.spinner(
                "Running AI workflow: planning → content → assessment → review → refinement..."
            ):
                result = run_workflow(
                    client=client,
                    model=model,
                    user_input=user_input,
                    prompt_builder=build_prompt,
                )

            st.session_state["study_result"] = result

        except Exception as exc:
            st.error(f"Application error: {exc}")

    result = st.session_state.get("study_result")

    if result:
        render_workflow_status(result)

        if result.get("errors"):
            with st.expander("Workflow warnings"):
                for error in result["errors"]:
                    st.warning(error)

        st.divider()
        render_final_pack(result)


if __name__ == "__main__":
    main()
