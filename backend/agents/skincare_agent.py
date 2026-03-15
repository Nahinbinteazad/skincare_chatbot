from backend.llm.llm_setup import get_llm
from langsmith import traceable

llm = get_llm()


@traceable(name="skincare_agent")
def skincare_advice(question):

    prompt = f"""
You are a skincare expert.

Give safe and helpful skincare advice.

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content