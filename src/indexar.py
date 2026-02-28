from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def indexar(paginas, CHUNK_SIZE, CHUNK_OVERLAP, CARPETA_INDICE):
    print("\n⏳ Indexando documentos por primera vez...")
    print("   (Esto solo ocurre una vez, o cuando cambies los PDFs)\n")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(paginas)
    print(f"\n🔪 {len(chunks)} fragmentos generados")

    print("🧠 Generando embeddings")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CARPETA_INDICE,
    )
    print(f"✅ Índice creado con {vectorstore._collection.count()} vectores\n")
    return vectorstore


def cargar_indice(CARPETA_INDICE):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = Chroma(
        persist_directory=CARPETA_INDICE,
        embedding_function=embeddings,
    )
    print(f"📦 Índice cargado ({vectorstore._collection.count()} vectores)")
    return vectorstore