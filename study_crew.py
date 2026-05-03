from __future__ import annotations

import os

from crewai import Agent, Crew, LLM, Process, Task


def build_local_llm() -> LLM:
    """Construye el cliente LLM local leyendo configuracion desde entorno."""
    model = os.getenv("OLLAMA_MODEL", "ollama/llama3.2")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    return LLM(model=model, base_url=base_url)


def build_study_crew(extracted_text: str) -> Crew:
    """Define agentes, tareas y flujo secuencial para el asistente de estudio."""
    llm_local = build_local_llm()

    pdf_reader_agent = Agent(
        role="Especialista en lectura de documentos",
        goal="Extraer ideas y estructura relevante del contenido del PDF",
        backstory=(
            "Eres experto en analisis de textos academicos. "
            "Identificas ideas clave y filtras informacion irrelevante."
        ),
        llm=llm_local,
        verbose=True,
    )

    summarizer_agent = Agent(
        role="Analista de contenido",
        goal="Crear un resumen claro, estructurado y util para estudiar",
        backstory=(
            "Eres un profesor virtual que sintetiza informacion compleja "
            "en un formato breve y entendible."
        ),
        llm=llm_local,
        verbose=True,
    )

    question_agent = Agent(
        role="Especialista en evaluacion",
        goal="Generar preguntas tipo examen con respuestas orientativas",
        backstory=(
            "Transformas contenido en ejercicios para reforzar aprendizaje "
            "y medir comprension."
        ),
        llm=llm_local,
        verbose=True,
    )

    tutor_agent = Agent(
        role="Tutor explicador",
        goal="Explicar conceptos dificiles de forma simple y progresiva",
        backstory=(
            "Eres un tutor paciente que adapta explicaciones al nivel "
            "de la persona estudiante."
        ),
        llm=llm_local,
        verbose=True,
    )

    # Task 1: extraer ideas clave desde el contenido bruto del PDF.
    task_read = Task(
        description=(
            "Analiza el siguiente texto extraido de un PDF y devuelve una lista de ideas "
            "clave por secciones, con 1 frase por idea.\n\n"
            f"TEXTO PDF:\n{extracted_text}"
        ),
        expected_output="Lista de ideas clave agrupadas por secciones del documento.",
        agent=pdf_reader_agent,
    )

    # Task 2: resumir apoyandose en la salida de Task 1.
    task_summary = Task(
        description=(
            "Con base en las ideas extraidas por el agente anterior, genera un resumen "
            "estructurado para estudiar con: tema principal, 5-10 puntos clave y mini "
            "conclusion final."
        ),
        expected_output="Resumen de estudio estructurado y claro.",
        agent=summarizer_agent,
        context=[task_read],
    )

    # Task 3: generar preguntas usando ideas + resumen.
    task_questions = Task(
        description=(
            "A partir del resumen y las ideas clave, crea 10 preguntas tipo examen "
            "(mezcla de respuesta corta y desarrollo) e incluye respuesta orientativa "
            "para cada una."
        ),
        expected_output="10 preguntas de examen con respuestas orientativas.",
        agent=question_agent,
        context=[task_read, task_summary],
    )

    # Task 4: simplificar los conceptos mas dificiles detectados.
    task_explain = Task(
        description=(
            "Identifica 5 conceptos que podrian resultar dificiles y explicalos en lenguaje "
            "simple con analogias breves."
        ),
        expected_output="5 explicaciones simplificadas de conceptos complejos.",
        agent=tutor_agent,
        context=[task_read, task_summary],
    )

    return Crew(
        agents=[pdf_reader_agent, summarizer_agent, question_agent, tutor_agent],
        tasks=[task_read, task_summary, task_questions, task_explain],
        process=Process.sequential,
        verbose=True,
    )
