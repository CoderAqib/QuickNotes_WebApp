from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse, HTMLResponse
from routes.note import note
from fastapi.staticfiles import StaticFiles
from config.db import conn
from fastapi.templating import Jinja2Templates
from schemas.note import note_entity


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(note)


@app.get("/about", response_class=HTMLResponse)
async def about_page():
    with open("templates/about.html") as f:
        return HTMLResponse(content=f.read())


# Set up Jinja2 templates (assuming your templates are stored in the "templates" folder)
templates = Jinja2Templates(directory="templates")

# MongoDB connection (make sure MongoDB is running locally or use a cloud database URI)
client = conn
db = client["notes"]  # Database name
notes_collection = db["notes"]  # Collection name


# Route to display all notes
@app.get("/notes", response_class=HTMLResponse)
async def notes_page(request: Request):
    # Fetch all notes from MongoDB
    notes = list(notes_collection.find({}))

    # Convert MongoDB's ObjectId to string so it can be rendered in HTML
    for note in notes:
        note["_id"] = str(note["_id"])  # Convert ObjectId to string

    # Pass the notes to the 'notes.html' template
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})


@app.get("/search")
async def search_notes(topic: str = Query(...)):
    try:
        # Search for notes with a case-insensitive match
        notes = notes_collection.find({"topic": {"$regex": topic, "$options": "i"}})
        result = [{"id": str(note["_id"]), "topic": note["topic"], "desc": note["desc"]} for note in notes]

        if not result:
            return JSONResponse(content={"message": "Notes not found"}, status_code=404)

        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"An error occurred: {str(e)}"}, status_code=500)

