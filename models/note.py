from pydantic import BaseModel


class Note(BaseModel):
    topic: str
    desc: str
