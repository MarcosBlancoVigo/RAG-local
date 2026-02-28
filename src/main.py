"""
RAG Local - Script simple para hacer preguntas a tus PDFs.

"""
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

import chromadb.telemetry.product.posthog as _telemetry # Evita que imprima warnings por pantalla al ejecutar
_telemetry.Posthog.capture = lambda *args, **kwargs: None


from pathlib import Path


from ensamblar_rag import construir_chain
from ensamblar_preguntas import bucle_preguntas
from indexar import indexar, cargar_indice
from lectura_documentos import cargar_pdfs


# ─────────────────────────────────────────
# CONFIGURACIÓN 
# ─────────────────────────────────────────

CARPETA_PDFS    = "../documentos"        # Carpeta donde están tus PDFs
CARPETA_INDICE  = "../indice"            # Se crea automáticamente
CHUNK_SIZE      = 1200
CHUNK_OVERLAP   = 150
MODELO_LLM      = "gemma2"            # Modelo de Ollama
NUM_CTX         = 4096                # Ventana de contexto (tokens del prompt base (instrucciones) + tokens de los 4 fragmentos de tus PDFs + tokens de tu pregunta + tokens de la respuesta generada)
NUM_RESULTADOS  = 3                   # Fragmentos a usar por pregunta


# Prompt que se le pasa al modelo
PROMPT = """Eres un experto en condensadores industriales usados en en los ciclos de agua-vapor. Estudia detenidamente la información de los documentos.
Responde siempre en español, de forma clara. Si la información no aparece en los documentos responde "La información no se encuentra en los documentos estudiados".

Información de los documentos:
{context}

Pregunta: {question}

Respuesta:"""


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

def main():

    paginas = cargar_pdfs(CARPETA_PDFS) # cargamos todas las paginas de los documentos

    print("=" * 55)
    print("  🧠 RAG Local — Pregunta a tus documentos PDF")
    print("=" * 55)

    # Crear carpeta de documentos si no existe
    Path(CARPETA_PDFS).mkdir(exist_ok=True)

    # Indexar si es la primera vez, cargar si ya existe el índice
    if not Path(CARPETA_INDICE).exists():
        vectorstore = indexar(paginas, CHUNK_SIZE, CHUNK_OVERLAP, CARPETA_INDICE)
    else:
        print("\n📦 Índice encontrado. Cargando...")
        vectorstore = cargar_indice(CARPETA_INDICE)
        print("   (Si has cambiado los PDFs, borra la carpeta 'indice' y vuelve a ejecutar)")

    chain = construir_chain(MODELO_LLM, NUM_CTX, NUM_RESULTADOS, PROMPT, vectorstore) # cargamos el modelo y lo dejamos listo para recibir preguntas

    print("✅ ¡Listo! Escribe tu pregunta. Escribe 'q' para terminar.\n")

    bucle_preguntas(chain) # recibe la pregunta y se la manda al modelo para que razone la respuesta

if __name__ == "__main__":
    main()