import pandas as pd
from langchain_community.tools import DuckDuckGoSearchRun
from backend.llm.llm_setup import get_llm
from langsmith import traceable

llm = get_llm()
search = DuckDuckGoSearchRun()

# Load dermatologist dataset
df = pd.read_csv("backend/data/dermatologists_bd.csv")


@traceable(name="doctor_agent")
def doctor_finder(question):

    city = None

    for c in df["city"].unique():
        if c.lower() in question.lower():
            city = c

    if city:
        doctors = df[df["city"] == city].head(5)
    else:
        doctors = df.head(5)

    # If dataset found doctors
    if len(doctors) > 0:

        output = ""

        for _, row in doctors.iterrows():

            output += f"""
Name: {row['name']}
Clinic: {row['clinic']}
City: {row['city']}
Address: {row['address']}
Phone: {row['phone']}
Google Maps: {row['map_link']}

Tips:
• Check Google reviews before visiting
• Call the clinic to confirm consultation fees
• Verify clinic hours

-----------------------
"""

        return output

    # Fallback to web search if dataset empty
    query = "best dermatologists in Bangladesh phone address rating review"

    search_results = search.run(query)

    prompt = f"""
Find real dermatologists in Bangladesh from the search results.

Provide:

Name
Clinic
Address
Phone
Rating if available

Search Results:
{search_results}
"""

    response = llm.invoke(prompt)

    return response.content