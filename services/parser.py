import json

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []

    for item in data:
        documents.append({
            "id": item["id"],
            "text": item["content"],
            "source": item["title"]
        })

    return documents