import re

def preprocess_data(data, max_length):
    preprocessed = []

    for doc_idx, doc in enumerate(data):
      text_norm = ' '.join(doc.split(' '))
      text_norm = text_norm.encode('utf-8', errors='ignore').decode('utf-8')
      text_norm = re.sub('([.,!?<>():#|*])', r' \1 ', text_norm)
      text_norm = re.sub('(?<=[0-9./])\s+(?=[0-9./])', '', text_norm)
      text_norm = re.sub('(?<=[0-9,/])\s+(?=[0-9,/])', '', text_norm)
      text_norm = re.sub(r'[\n]+', '', text_norm)
      text_norm = text_norm.strip()
      text_norm = text_norm.split()

      for i in range(0, len(text_norm), max_length):
        preprocessed.append((doc_idx," ".join(text_norm[i:i + max_length])))
      
    return preprocessed