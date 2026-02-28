import time
import threading
from pathlib import Path

"""
Este archivo monta el bucle de preguntas y te da las fuentes consultadas cuando el modelo te devuelve una respuesta
"""

def preguntar(chain, pregunta):
    resultado = chain.invoke({"query": pregunta})

    print("\n" + "═" * 55)
    print("💡 RESPUESTA:")
    print(resultado["result"])

    # Mostrar fuentes
    fuentes_vistas = set()
    fuentes = []
    for doc in resultado.get("source_documents", []):
        nombre = Path(doc.metadata.get("source", "?")).name
        pagina = doc.metadata.get("page", "?")
        clave = (nombre, pagina)
        if clave not in fuentes_vistas:
            fuentes_vistas.add(clave)
            fuentes.append(f"{nombre} (pág. {pagina + 1 if isinstance(pagina, int) else pagina})")

    if fuentes:
        print("\n📎 Fuentes:")
        for f in fuentes:
            print(f"  • {f}")
    print("═" * 55)


def mostrar_timer(stop_event):
        """Muestra un contador en tiempo real mientras el modelo piensa."""
        segundos = 0
        while not stop_event.is_set():
            segundos += 1
            print(f"\r⏳ Pensando... {segundos}s", end="", flush=True)
            time.sleep(1)     
        print(f"\r✅ Respuesta generada en {segundos}s{' ' * 10}")  # limpia la línea


def bucle_preguntas(chain):
      # Bucle de preguntas
    while True:
        try:
            pregunta = input("❓ Tu pregunta: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 ¡Hasta luego!")
            break

        if not pregunta:
            continue
        if pregunta.lower() in ("q"):
            print("👋 ¡Hasta luego!")
            break

        # Lanzar el timer en un hilo paralelo
        stop_event = threading.Event()
        timer_thread = threading.Thread(target=mostrar_timer, args=(stop_event,))
        timer_thread.start()

        preguntar(chain, pregunta)

        # Parar el timer cuando llegue la respuesta
        stop_event.set()
        timer_thread.join()
        print()