# ✅ File: app/main.py
from fastapi import FastAPI
from app.schemas import SearchQuery
from app.services import get_services_duckduckgo, get_from_mock, is_general_question

app = FastAPI()

@app.post("/search")
def search(query: SearchQuery):
    results = get_services_duckduckgo(query.query)

    if not results:
        return {
            "response": f"😕 Sorry, I couldn’t find a reliable answer or result for your query: **'{query.query}'**."
        }

    mock_results = get_from_mock(query.query)

    if is_general_question(query.query) and results:
        reply = "\n".join([r['address'] for r in results])
        return {
            "response": f"📘 Here's what I found about **{results[0]['name']}** (showing {len(results)} points):\n\n{reply}"
        }

    if results == mock_results:
        reply = "\n".join([f"{i+1}. {r['name']} - {r['address']}" for i, r in enumerate(results)])
        return {
            "response": f"🙋 We couldn’t find any real-time results for **'{query.query}'**. But here are {len(results)} trusted suggestions from our records:\n\n{reply}"
        }

    reply = "\n".join([f"{i+1}. {r['name']} - {r['address']}" for i, r in enumerate(results)])
    return {
        "response": f"✅ Found {len(results)} relevant result(s) for **'{query.query}'**:\n\n{reply}"
    }


