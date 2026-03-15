from langchain_community.tools import DuckDuckGoSearchRun
from backend.llm.llm_setup import get_llm
from langsmith import traceable

search = DuckDuckGoSearchRun()
llm = get_llm()


@traceable(name="search_agent")
def search_answer(question):

    results = search.run(question)

    prompt = f"""
Use this search result to answer the question.

Search Results:
{results}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content