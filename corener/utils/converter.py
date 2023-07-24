
def prediction_converter(data):
  doc_id_to_data = {}
  for item in data:
    doc_id = item["doc_id"]
    if doc_id not in doc_id_to_data:
      doc_id_to_data[doc_id] = {
          "text": "",
          "tokens": [],
          "entities": [],
          "relations": []
      }
    doc_data = doc_id_to_data[doc_id]
    doc_data["text"] += item["text"]
    doc_data["tokens"].extend(item["tokens"])

    for entity in item["entities"]:
      entity_copy = entity.copy()
      entity_copy["start"] += len(doc_data["tokens"]) - len(item["tokens"])
      entity_copy["end"] += len(doc_data["tokens"]) - len(item["tokens"])
      entity_copy["start_char"] += len(doc_data["text"]) - len(item["text"])
      entity_copy["end_char"] += len(doc_data["text"]) - len(item["text"])
      doc_data["entities"].append(entity_copy)

    doc_data["relations"].extend(item["relations"])

  return list(doc_id_to_data.values())