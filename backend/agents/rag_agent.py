from backend.llm.llm_setup import get_llm
from langsmith import traceable

llm = get_llm()

vector_db = None


def set_vector_db(db):
    global vector_db
    vector_db = db


@traceable(name="rag_agent")
def rag_answer(question):

    if vector_db is None:
        return "Please upload and process a document first.", []

    docs = vector_db.similarity_search(question, k=3)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Answer the question using ONLY the provided context.

If the answer is not in the context, say:
"I could not find the answer in the document."

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content, docs