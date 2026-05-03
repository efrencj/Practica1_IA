from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from pdf_reader import clamp_text, extract_pdf_text
from study_crew import build_study_crew


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Asistente de estudio multiagente para PDFs con CrewAI + Ollama"
    )
    parser.add_argument("pdf", type=str, help="Ruta al PDF que se quiere analizar")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=12000,
        help="Maximo de caracteres enviados al crew (default: 12000)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="salida_estudio.md",
        help="Archivo de salida para guardar el resultado final",
    )
    return parser.parse_args()


def _safe_text(value: Any) -> str:
    """Normaliza cualquier salida de tarea a texto plano."""
    if value is None:
        return ""
    return str(value).strip()


def build_output_markdown(result: Any, crew: Any, pdf_path: str) -> str:
    """Consolida las 4 tareas en un unico Markdown final."""
    sections = [
        ("Ideas clave extraidas", ""),
        ("Resumen de estudio", ""),
        ("Preguntas tipo examen", ""),
        ("Explicaciones de conceptos dificiles", ""),
    ]

    tasks_output = getattr(result, "tasks_output", None)
    if tasks_output:
        # Camino principal en versiones recientes de CrewAI.
        for idx in range(min(4, len(tasks_output))):
            task_out = tasks_output[idx]
            raw = getattr(task_out, "raw", None)
            content = raw if raw else task_out
            sections[idx] = (sections[idx][0], _safe_text(content))
    else:
        # Compatibilidad con versiones donde la salida queda en crew.tasks.
        for idx in range(min(4, len(getattr(crew, "tasks", [])))):
            task = crew.tasks[idx]
            content = getattr(task, "output", "")
            sections[idx] = (sections[idx][0], _safe_text(content))

    lines = [f"# Resultado de estudio: {Path(pdf_path).name}", ""]
    for title, body in sections:
        lines.append(f"## {title}")
        lines.append(body if body else "_Sin contenido generado en esta seccion._")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    args = parse_args()

    raw_text = extract_pdf_text(args.pdf)
    if not raw_text:
        raise ValueError("No se pudo extraer texto del PDF o esta vacio")

    # Se limita el contexto para evitar saturar el modelo local.
    context_text = clamp_text(raw_text, max_chars=args.max_chars)
    crew = build_study_crew(context_text)
    result = crew.kickoff()
    markdown = build_output_markdown(result, crew, args.pdf)

    output_path = Path(args.output)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"Resultado guardado en: {output_path.resolve()}")


if __name__ == "__main__":
    main()
