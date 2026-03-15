from backend.llm.llm_setup import get_llm
from langsmith import traceable

llm = get_llm()


@traceable(name="skintype_agent")
def detect_skin_type(user_answers):

    prompt = f"""
You are a dermatologist AI.

Based on the user's answers, determine their skin type.

Possible skin types:
- Oily
- Dry
- Combination
- Sensitive
- Normal

User Answers:
{user_answers}

Provide:
1. Skin Type
2. Short Explanation
3. Basic Skincare Tips
"""

    response = llm.invoke(prompt)

    return response.content