import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from backend.agents.search_agent import search_answer
from backend.agents.skincare_agent import skincare_advice
from backend.agents.rag_agent import rag_answer, set_vector_db
from backend.db.vector_store import create_vector_store
from backend.utils.pdf_loader import load_pdf
from backend.agents.ocr_agent import analyze_image
from backend.agents.doctor_agent import doctor_finder
from backend.agents.skintype_agent import detect_skin_type


st.set_page_config(
    page_title="Skincare AI Assistant",
    page_icon="✨",
    layout="wide"
)

st.title("✨ Skincare AI Assistant")




# ---------------- SIDEBAR ----------------

st.sidebar.header("Agent Mode")

mode = st.sidebar.selectbox(
    "Choose Agent",
    [
        "Skincare Advice",
        "Skin Type Detection",
        "Web Search",
        "Document Q&A",
        "Find a Dermatologist",
        "Ingredient Scanner"
    ]
)

# ---------------- CHAT MEMORY ----------------

history_key = f"messages_{mode}"

if history_key not in st.session_state:
    st.session_state[history_key] = []


# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state[history_key] = []

if mode == "Skin Type Detection":

    st.subheader("🧪 Skin Type Detection")

    q1 = st.selectbox(
        "How does your skin feel after washing?",
        ["Tight and dry", "Comfortable", "Oily quickly", "Oily in T-zone"]
    )

    q2 = st.selectbox(
        "How often do you get acne?",
        ["Rarely", "Sometimes", "Often", "Very often"]
    )

    q3 = st.selectbox(
        "How visible are your pores?",
        ["Very small", "Small", "Large in T-zone", "Large everywhere"]
    )

    q4 = st.selectbox(
        "Does your skin react easily to products?",
        ["Never", "Sometimes", "Often"]
    )

    if st.button("Detect My Skin Type"):

        answers = f"""
After washing: {q1}
Acne frequency: {q2}
Pore visibility: {q3}
Sensitivity: {q4}
"""

        with st.spinner("Analyzing skin type..."):

            result = detect_skin_type(answers)

        st.success("Skin Analysis Complete")

        st.write(result)

        st.session_state[history_key].append({
        "role": "assistant",
        "content": result
})

# ---------------- CITY SELECT ----------------

city = None
if mode == "Find a Dermatologist":

    city = st.sidebar.selectbox(
        "Select City",
        ["Dhaka", "Chittagong", "Sylhet", "Khulna", "Rajshahi"]
    )


# ---------------- PDF RAG ----------------

if mode == "Document Q&A":

    st.sidebar.subheader("Upload Document")

    pdf = st.sidebar.file_uploader("Upload PDF", type="pdf")

    if pdf:

        if st.sidebar.button("Process Document"):

            with st.spinner("Processing document..."):

                chunks = load_pdf(pdf)

                db = create_vector_store(chunks)

                set_vector_db(db)

            st.sidebar.success("Document processed successfully!")


# ---------------- OCR INGREDIENT SCANNER ----------------

if mode == "Ingredient Scanner":

    st.subheader("Upload Product Image")

    img = st.file_uploader("Upload skincare product image")

    if img:

        with open("temp.jpg", "wb") as f:
            f.write(img.read())

        with st.spinner("Analyzing ingredients..."):

            result = analyze_image("temp.jpg")

        st.write(result)

        st.session_state[history_key].append({
        "role": "assistant",
        "content": result
    })

        if os.path.exists("temp.jpg"):
            os.remove("temp.jpg")


# ---------------- SHOW CHAT HISTORY ----------------

for message in st.session_state[history_key]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# ---------------- CHAT INPUT ----------------

question = st.chat_input("Ask something about skincare...")


if question:

    # Save user message
    st.session_state[history_key].append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)


    # ---------------- ASSISTANT RESPONSE ----------------

    with st.chat_message("assistant"):

        # -------- Skincare Advice --------

        if mode == "Skincare Advice":

            answer = skincare_advice(question)

            st.write(answer)

            st.session_state[history_key].append({
                "role": "assistant",
                "content": answer
            })


        # -------- Web Search --------

        elif mode == "Web Search":

            answer = search_answer(question)

            st.write(answer)

            st.session_state[history_key].append({
                "role": "assistant",
                "content": answer
            })


        # -------- RAG DOCUMENT Q&A --------

        elif mode == "Document Q&A":

            try:

                answer, docs = rag_answer(question)

                st.write(answer)

                with st.expander("Source Documents"):
                    for doc in docs:
                        st.write(doc.page_content)

                st.session_state[history_key].append({
                    "role": "assistant",
                    "content": answer
                })

            except:

                st.warning("Please upload and process a PDF first.")


        # -------- DERMATOLOGIST FINDER --------

        elif mode == "Find a Dermatologist":

            query = f"{question} dermatologist in {city}"

            answer = doctor_finder(query)

            st.subheader(f"Top Dermatologists in {city}")

            doctors = answer.strip().split("Name:")

            table_data = []

            for doc in doctors:

                if doc.strip() == "":
                    continue

                lines = [l.strip() for l in doc.split("\n") if l.strip()]

                try:
                    name = lines[0].replace("👨‍⚕️", "").strip()
                    clinic = lines[2].replace("Clinic:", "").strip()
                    address = lines[3].replace("Address:", "").strip()
                    phone = lines[4].replace("Phone:", "").strip()
                    maps = lines[5].replace("Google Maps:", "").strip()

                    table_data.append({
                        "Doctor": name,
                        "Clinic": clinic,
                        "Address": address,
                        "Phone": phone,
                        "Google Maps": maps
                    })

                except:
                    pass

            st.table(table_data)

            st.session_state[history_key].append({
                "role": "assistant",
                "content": f"Displayed dermatologists in {city}"
            })