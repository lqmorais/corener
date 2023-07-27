def prediction_converter(data):
  doc_id_to_data = {}
  entity_mapping = {}

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

    if doc_data["text"]:
      doc_data["text"] += " "

    doc_data["text"] += item["text"]
    doc_data["tokens"].extend(item["tokens"])

    offset_tokens = len(doc_data["tokens"]) - len(item["tokens"])
    offset_text = len(doc_data["text"]) - len(item["text"])

    for entity_idx, entity in enumerate(item["entities"]):
      entity_copy = entity.copy()
      entity_copy["start"] += offset_tokens
      entity_copy["end"] += offset_tokens
      entity_copy["start_char"] += offset_text
      entity_copy["end_char"] += offset_text
      doc_data["entities"].append(entity_copy)

      # Mapping for old entity index and new entity index
      entity_mapping[entity_idx] = {
        "new_index": len(doc_data["entities"]) - 1,
        "start_char": entity_copy["start_char"]
      }

    for relation in item["relations"]:
      relation_copy = relation.copy()
      head_entity_index = relation["head"]
      tail_entity_index = relation["tail"]

      head_entity_info = entity_mapping.get(head_entity_index)
      tail_entity_info = entity_mapping.get(tail_entity_index)

      if head_entity_info:
        relation_copy["head"] = head_entity_info["new_index"]
        relation_copy["head_start"] = head_entity_info["start_char"]

      if tail_entity_info:
        relation_copy["tail"] = tail_entity_info["new_index"]
        relation_copy["tail_start"] = tail_entity_info["start_char"]

      doc_data["relations"].append(relation_copy)

  return list(doc_id_to_data.values())

  