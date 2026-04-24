from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from google.cloud import firestore
import json

app = FastAPI()

jobs = [
    {"id": "1", "title": "Software Engineer Intern", "location": "Remote", "company": "Google"},
    {"id": "2", "title": "Cloud Intern", "location": "NYC", "company": "Amazon"},
]

@app.get("/")
def root():
    return {"status": "MCP server running"}

def fetch_jobs(params):
    role = params.get("role", "").lower()
    location = params.get("location", "").lower()

    return [
        job for job in jobs
        if role in job["title"].lower()
        and location in job["location"].lower()
    ]

def sync_pipeline(params):
    db = firestore.Client()
    action = params.get("action")

    if action == "create":
        db.collection("pipeline").add(params["data"])
        return {"status": "saved"}

    elif action == "list":
        docs = db.collection("pipeline").stream()
        return [doc.to_dict() for doc in docs]

    elif action == "update":
        doc_id = params["id"]
        db.collection("pipeline").document(doc_id).update(params["data"])
        return {"status": "updated"}

    return {"error": "Invalid action"}

@app.post("/mcp")
async def mcp(request: Request):
    try:
        body = await request.json()
        tool = body.get("tool")
        params = body.get("params", {})

        if tool == "fetch_jobs":
            result = fetch_jobs(params)
        elif tool == "sync_pipeline":
            result = sync_pipeline(params)
        else:
            result = {"error": "Unknown tool"}

        async def event_stream():
            yield {
                "event": "message",
                "data": json.dumps(result)
            }

        return EventSourceResponse(event_stream())

    except Exception as e:
        return {"error": str(e)}


# from fastapi import FastAPI, Request
# from sse_starlette.sse import EventSourceResponse
# import json
# import time

# app = FastAPI()

# # -------------------
# # MOCK JOB DATABASE
# # -------------------
# JOBS = [
#     {"id": "1", "company": "Google", "title": "SWE Intern", "location": "NYC"},
#     {"id": "2", "company": "Amazon", "title": "Backend Intern", "location": "Seattle"},
# ]

# # -------------------
# # FETCH JOBS TOOL
# # -------------------
# def fetch_jobs(location=None):
#     results = JOBS
#     if location:
#         results = [j for j in JOBS if location.lower() in j["location"].lower()]
#     return results

# # -------------------
# # MCP SSE STREAM
# # -------------------
# @app.get("/mcp")
# async def mcp_stream(request: Request):

#     async def event_generator():
#         while True:
#             # Simulated response stream
#             data = {
#                 "tool": "fetch_jobs",
#                 "results": fetch_jobs()
#             }

#             yield {
#                 "event": "message",
#                 "data": json.dumps(data)
#             }

#             await request.is_disconnected()
#             break

#     return EventSourceResponse(event_generator())
