# 🧠 RAG Local — Pregunta a tus documentos PDF

Sistema de preguntas y respuestas sobre documentos PDF técnicos. No necesita conexión a internet.

---

## 📋 Índice

1. [Tecnologías utilizadas](#tecnologías-utilizadas)
2. [Estructura del proyecto](#estructura-del-proyecto)
3. [Instalación paso a paso](#instalación-paso-a-paso)
4. [Cómo ejecutar](#cómo-ejecutar)
5. [Cómo usar el chat](#cómo-usar-el-chat)
6. [Cómo añadir o cambiar documentos](#cómo-añadir-o-cambiar-documentos)
7. [Cómo cambiar de modelo](#cómo-cambiar-de-modelo)
8. [Configuración avanzada](#configuración-avanzada)
9. [Solución de problemas](#solución-de-problemas)

---

## Tecnologías utilizadas

| Componente | Herramienta | Para qué sirve |
|---|---|---|
| LLM (modelo de lenguaje) | Ollama + Mistral 7B | Genera las respuestas |
| Embeddings | sentence-transformers (HuggingFace) | Convierte texto en vectores para búsqueda semántica |
| Base de datos vectorial | ChromaDB | Almacena y busca los fragmentos de los documentos |
| Carga de PDFs | PyPDF | Lee y extrae el texto de los PDFs |
| Orquestación RAG | LangChain | Conecta todas las piezas |

### ¿Qué es RAG?

RAG (Retrieval-Augmented Generation) es una técnica que combina búsqueda en documentos con generación de texto:

```
Tu pregunta
    │
    ▼
Búsqueda semántica en ChromaDB
    │
    ▼
Recupera los 3 fragmentos más relevantes de tus PDFs
    │
    ▼
Envía esos fragmentos + tu pregunta a Mistral
    │
    ▼
Mistral genera una respuesta basada en esos fragmentos
    │
    ▼
Respuesta + fuentes (nombre del PDF y página)
```

---

## Estructura del proyecto

```
rag_condensador/
│
├── documentos/                  ← 📂 Documentación que aprende el modelo
│   ├── Epri_Condensador.pdf
│   ├── Epri_Condensador_2.PDF
│   ├── Epri_Condensador_3.pdf
│   └── Manual_Mantenimiento.pdf
│
├── indice/                      ← 🤖 Generado automáticamente por el script
|    └── (archivos internos de ChromaDB — no tocar)
|
├── src/
|   ├── main.py                  ← Script principal. Único archivo a ejecutar
|   ├── ensamblar_preguntas.py   ← Script que monta el bucle de preguntas
|   ├── lectura_documentos.py    ← Script que lee y guarda todas las páginas de los pdf que hay en la carpeta documentos
|   ├── indexar.py               ← Script que indexa (o carga los índices si ya estaban creados) los pdfs.
|   └── ensamblar_rag            ← Script que ensambla todo el modelo para que esté listo para responder a las preguntas
|
├── README.md                    ← Documento descriptivo del proyecto
└── requirements.txt             ← Dependencias Python con versiones fijadas
```

> **Nota:** La carpeta `indice/` se crea sola la primera vez que se ejecuta `main.py`. No editar ni borrar salvo que se quiera re-indexar desde cero.

---

## Instalación paso a paso

### Requisitos previos
- Windows 10/11
- Python 3.9 o superior (la versión de python usada en este proyecto fue la 3.11)
- ~6 GB de espacio libre en disco (4 GB modelo + embeddings + índice)

---

### Paso 1 — Instalar Ollama

Ollama es la aplicación que descarga y ejecuta el modelo de lenguaje en el ordenador.

1. Ve a **[https://ollama.com/download](https://ollama.com/download)**
2. Descarga e instala **"Download for Windows"**
3. Tras la instalación aparecerá un icono de llama 🦙 en la barra de tareas (esquina inferior derecha)

---

### Paso 2 — Descargar el modelo Mistral

Tras haber instalado Ollama, abre **CMD** y ejecuta:

```cmd
"C:\Users\TU_USUARIO\AppData\Local\Programs\Ollama\ollama.exe" pull mistral
```

Esto descarga el modelo (~4 GB). Solo se hace **una vez**. Verás una barra de progreso.

---

### Paso 3 — Crear el entorno virtual e instalar dependencias

Desde la terminal, en la carpeta del proyecto:

```cmd
# Crear entorno virtual (entorno del proyecto creado con la terminal de anaconda)
conda create -n nombre_environment python=3.11
conda activate nombre_environment

# Instalar dependencias con versiones exactas
pip install -r requirements.txt
```

Las versiones del `requirements.txt` son:

```
langchain==0.1.20
langchain-community==0.0.38
langchain-core==0.1.52
sentence-transformers==3.0.1
chromadb==0.5.0
pypdf==4.3.1
ollama==0.2.1
```

> Las versiones están fijadas intencionalmente. LangChain cambia su estructura interna entre versiones y estas son las que funcionan correctamente juntas.

---

### Paso 4 — Añadir los documentos PDF

Copia tus archivos PDF técnicos dentro de la carpeta `documentos/`

El script acepta PDFs en subcarpetas también (búsqueda recursiva).

---

## Cómo ejecutar

### Cada vez que quieras usar el sistema:

**1.** Activa el entorno virtual:
```cmd
conda activate nombre_environment
```

**2.** Ve a la carpeta del proyecto y ejecuta:
```cmd
python src/main.py
```

### ¿Qué ocurre al ejecutar?

**Primera vez:**
```
=======================================================
  🧠 RAG Local — Pregunta a tus documentos PDF
=======================================================

⏳ Indexando documentos por primera vez...

📂 Cargando 3 PDF(s)...
  ✅ Epri_Condensador.pdf (340 páginas)
  ✅ Epri_Condensador_2.PDF (282 páginas)
  ✅ Epri_Condensador_3.pdf (186 páginas)

🔪 2627 fragmentos generados
🧠 Generando embeddings...
✅ Índice creado con 2627 vectores

🔗 Conectando con Ollama (modelo: mistral)...

✅ ¡Listo! Escribe tu pregunta. Escribe 'q' para terminar.

❓ Tu pregunta:
```

**Siguientes veces** (mucho más rápido, el índice ya existe):
```
📦 Índice encontrado. Cargando...
📦 Índice cargado (2627 vectores)
🔗 Conectando con Ollama (modelo: mistral)...
✅ ¡Listo! Escribe tu pregunta.
```

---

## Cómo usar el chat

Una vez arrancado, escribe tu pregunta y pulsa **Enter**:

```
❓ Tu pregunta: ¿Cuáles son las causas principales de fallo en condensadores?

⏳ Pensando... 12s
✅ Respuesta generada en 18s

═══════════════════════════════════════════════════════
💡 RESPUESTA:
Las principales causas de fallo en condensadores según los documentos son:
1. Corrosión por picadura en los tubos de titanio...
2. Fouling biológico en el lado del agua de refrigeración...
3. ...

📎 Fuentes:
  • Epri_Condensador.pdf (pág. 47)
  • Epri_Condensador_2.PDF (pág. 112)
═══════════════════════════════════════════════════════
```

Para salir escribe `q` y pulsa Enter.

> **Tiempo de respuesta:** entre 30 segundos y 2 minutos en CPU. El contador en pantalla muestra el tiempo real de razonamiento.

---

## Cómo añadir o cambiar documentos

Si añades nuevos PDFs o reemplazas los existentes, el índice anterior queda obsoleto. Para re-indexar:

**1.** Copia los nuevos PDFs a la carpeta `documentos/`

**2.** Borra la carpeta `indice/`:

**3.** Vuelve a ejecutar `python main.py`. Se re-indexará todo automáticamente.

---

## Cómo cambiar de modelo
Para listar los modelos descargados, abrir el CMD y ejecutar:
```cmd
ollama list
```

Esto te enseña los modelos que hay descargados, así como el tamaño que ocupan:
```
NAME              ID              SIZE      MODIFIED
mistral:latest    6577803aa9a0    4.4 GB    23 hours ago
```

A continuación mostramos una serie de posibles modelos:

| Modelo | Comando de descarga | Tamaño | Velocidad en CPU | Mejor para |
|--------|-------------------|--------|-----------------|------------|
| `mistral` | `ollama pull mistral` | 4.1 GB | ⭐⭐⭐ Media | Uso general. Equilibrado en calidad y velocidad |
| `llama3.2` | `ollama pull llama3.2` | 2.0 GB | ⭐⭐⭐⭐⭐ Muy rápida | Preguntas rápidas, respuestas cortas |
| `phi3` | `ollama pull phi3` | 2.2 GB | ⭐⭐⭐⭐⭐ Muy rápida | El más rápido en CPU. Bueno para pruebas |
| `llama3.1` | `ollama pull llama3.1` | 4.7 GB | ⭐⭐⭐ Media | Razonamiento y respuestas largas y estructuradas |
| `deepseek-r1` | `ollama pull deepseek-r1` | 4.7 GB | ⭐⭐ Lenta | Documentación técnica compleja. Muy preciso |
| `gemma2` | `ollama pull gemma2` | 5.4 GB | ⭐⭐ Lenta | Síntesis de documentos. Buenas explicaciones |


Para descragar el nuevo modelo (por ejemplo `gemma2`) abrir CMD y ejecutar:
```cmd
ollama pull gemma2
```

Ahora al listar los modelos aparece ya el nuevo:
```
NAME              ID              SIZE      MODIFIED       
gemma2:latest     ff02c3702f32    5.4 GB    15 seconds ago
mistral:latest    6577803aa9a0    4.4 GB    24 hours ago
```

Por último, hay que cambiar el nombre del modelo en `main.py`.

Reemplazar:
```
MODELO_LLM = "mistral" 
```
por:
```
MODELO_LLM = "gemma2" 
```

En caso de querer borrar del disco un modelo, simplemente hay que abrir el CMD y ejecutar:
```cmd
ollama rm mistral
```

---

## Configuración avanzada

En la parte superior de `main.py` hay una sección de configuración que se puede ajustar:

```python
CARPETA_PDFS   = "documentos"   # Carpeta con los PDFs
CARPETA_INDICE = "indice"       # Dónde se guarda el índice
MODELO_LLM     = "mistral"      # Modelo de Ollama a usar
CHUNK_SIZE     = 1200           # Tamaño de fragmentos de texto
CHUNK_OVERLAP  = 150            # Solapamiento entre fragmentos
NUM_RESULTADOS = 3              # Fragmentos recuperados por pregunta
```

### Ajustes de velocidad vs. calidad

- **Respuestas más rápidas:** reduce `NUM_RESULTADOS` a 2 y `CHUNK_SIZE` a 500
- **Respuestas más completas:** sube `NUM_RESULTADOS` a 6 y `CHUNK_SIZE` a 1500
- **Menos uso de RAM:** en `construir_chain()`, reduce `num_ctx` de 2048 a 1024

---

## Solución de problemas

**`ModuleNotFoundError`**
→ Asegúrate de tener el entorno activado (`conda activate nombre_environment`) y de haber instalado con las versiones exactas del `requirements.txt`.

**Las respuestas son lentas**
→ Normal en CPU. Usar `phi3` o `llama3.2` para respuestas más rápidas. Reducir también `NUM_RESULTADOS` a 2.

**El modelo responde en inglés**
→ El prompt le indica que responda en español, pero a veces lo ignora. Puedes añadir al final de tu pregunta: *"responde en español"*.

