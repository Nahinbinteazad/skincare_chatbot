import easyocr
from backend.llm.llm_setup import get_llm

reader = easyocr.Reader(['en'])

llm = get_llm()

def analyze_image(image_path):

    text = reader.readtext(image_path, detail=0)

    ingredients = " ".join(text)

    prompt = f"""
These are skincare ingredients extracted from a product label.

Ingredients:
{ingredients}

Explain what each ingredient does in skincare.
"""

    response = llm.invoke(prompt)

    return response.content