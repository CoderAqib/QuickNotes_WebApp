# convert MongoDB's BSON format to JSON

def note_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "topic": item["topic"],
        "desc": item["desc"]
    }


def notes_entity(items) -> list:
    return [note_entity(item) for item in items]
