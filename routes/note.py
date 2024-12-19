from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from config.db import conn
from fastapi.templating import Jinja2Templates

note = APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": doc["_id"],
            "topic": doc.get("topic", "No Topic Provided"),
            "desc": doc.get("desc", "No Description Provided")
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})


# @note.post("/")
# async def create_item(request: Request):
#     form = await request.form()
#     formDict = dict(form)
#     note = conn.notes.notes.insert_one(formDict)
#     return {"success": True}

@note.post("/")
async def create_item(request: Request):
    form = await request.form()
    topic = form.get("topic", "").strip()
    desc = form.get("desc", "").strip()

    # Validate inputs
    if not topic or not desc:
        return {"error": "Both topic and description are required."}

    # Insert into MongoDB
    conn.notes.notes.insert_one({"topic": topic, "desc": desc})
    # return {"success": True}


