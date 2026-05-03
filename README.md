# Practica1_IA

Asistente de estudio multiagente para documentos PDF usando `CrewAI` + `Ollama`.

El sistema lee un PDF y genera un unico archivo Markdown con:
- Ideas clave por secciones
- Resumen de estudio
- Preguntas tipo examen con respuesta orientativa
- Explicaciones simples de conceptos dificiles

## 1. Requisitos

- Python 3.10+
- Ollama instalado y en ejecucion
- Un modelo local descargado (por defecto `llama3.2`)

## 2. Instalacion

Desde la raiz del proyecto:

```bash
pip install -r requirements.txt
```

## 3. Configuracion de Ollama

Arranca Ollama y descarga el modelo por defecto:

```bash
ollama pull llama3.2
```

Variables de entorno soportadas:
- `OLLAMA_MODEL` (default: `ollama/llama3.2`)
- `OLLAMA_BASE_URL` (default: `http://localhost:11434`)

Puedes usar el archivo `.env.example` como referencia.

## 4. Estructura del proyecto

- `main.py`: punto de entrada CLI y generacion del Markdown final
- `pdf_reader.py`: extraccion y recorte de texto del PDF
- `study_crew.py`: definicion de agentes, tareas y flujo secuencial
- `pdfs/`: carpeta con PDFs de prueba
- `CONTEXTO/`: material de contexto de la practica

## 5. Uso

Ejecuta:

```bash
python main.py <ruta_pdf> --output <salida.md>
```

Ejemplo:

```bash
python main.py pdfs/quijote.pdf --output salida_quijote.md
```

Parametro opcional para limitar texto enviado al modelo:

```bash
python main.py pdfs/quijote.pdf --max-chars 8000 --output salida_quijote.md
```

## 6. Salida esperada

El archivo de salida (`.md`) contiene 4 secciones:
1. `Ideas clave extraidas`
2. `Resumen de estudio`
3. `Preguntas tipo examen`
4. `Explicaciones de conceptos dificiles`

## 7. Problemas comunes

- `No se pudo extraer texto del PDF`:
  - El PDF puede estar vacio, protegido o escaneado sin OCR.

- Salida con texto raro (`Ã¡`, `Â¿`, etc.):
  - Abre el archivo como UTF-8 en tu editor.

- El modelo no responde:
  - Verifica que Ollama este activo en `http://localhost:11434`.
  - Comprueba que el modelo exista (`ollama list`).

## 8. Nota tecnica

El flujo es secuencial (`Process.sequential`): cada tarea usa la salida de tareas previas. El resultado final se consolida en un solo Markdown para facilitar entrega y revision.
