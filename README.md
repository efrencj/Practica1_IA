# practica1_IA

Asistente de estudio multiagente para PDFs usando CrewAI + Ollama.

## Estructura
- `main.py`: entrada CLI
- `pdf_reader.py`: extraccion de texto del PDF
- `study_crew.py`: definicion de agentes y tareas secuenciales
- `requirements.txt`: dependencias

## Requisitos
1. Tener Ollama ejecutandose en local (`http://localhost:11434`)
2. Tener descargado un modelo compatible, por ejemplo `llama3.2`
3. Instalar dependencias: `pip install -r requirements.txt`

## Uso
`python main.py pdfs/quijote.pdf --output salida_quijote.md`

Opcional:
`python main.py pdfs/quijote.pdf --max-chars 8000`
