"""
Esta función ensambla las tres piezas del sistema RAG y devuelve una cadena lista para recibir preguntas
"""

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


def construir_chain(MODELO_LLM, NUM_CTX, NUM_RESULTADOS, PROMPT, vectorstore):
    print(f"\n🔗 Conectando con Ollama (modelo: {MODELO_LLM})...")
    llm = Ollama(
        model=MODELO_LLM,
        temperature=0.1,
        num_ctx=NUM_CTX,
        num_thread=8,
    )
    prompt = PromptTemplate(
        template=PROMPT,
        input_variables=["context", "question"]
    )
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", # define cómo se manejan los fragmentos recuperados. "stuff" significa que los mete todos juntos en el prompt de golpe (el más sencillo y el que funciona mejor cuando los fragmentos son pocos y cortos).
        retriever=vectorstore.as_retriever(search_kwargs={"k": NUM_RESULTADOS}), # convierte ChromaDB en un "buscador". Cuando llega una pregunta, este retriever la convierte en un vector, lo compara con todos los vectores del índice y devuelve los `k` fragmentos más similares. Con `NUM_RESULTADOS=4` devuelve los 4 más relevantes.
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )
    
    return chain