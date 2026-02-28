import glob
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

"""
Este archivo lee los pdf que se encuentran en la carpeta documentos y guarda todas las páginas
"""
def cargar_pdfs(CARPETA_PDFS):
    pdfs = glob.glob(f"{CARPETA_PDFS}/**/*.pdf", recursive=True)
    if not pdfs:
        print(f"\n❌ No hay PDFs en la carpeta '{CARPETA_PDFS}'.")
        print(f"   Copia tus archivos PDF ahí y vuelve a ejecutar el script.")
        exit()

    print(f"\n📂 Cargando {len(pdfs)} PDF(s)...")
    paginas = []
    for pdf in pdfs:
        try:
            docs = PyPDFLoader(pdf).load()
            paginas.extend(docs)
            print(f"  ✅ {Path(pdf).name} ({len(docs)} páginas)")
        except Exception as e:
            print(f"  ❌ Error con {Path(pdf).name}: {e}")
    return paginas