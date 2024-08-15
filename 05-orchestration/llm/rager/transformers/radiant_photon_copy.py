import hashlib

import re
from typing import Any, Dict, List

def generate_document_id(doc):
    combined = f"{doc['course']}-{doc['question']}-{doc['text'][:10]}"
    hash_object = hashlib.md5(combined.encode())
    hash_hex = hash_object.hexdigest()
    document_id = hash_hex[:8]
    return document_id

@transformer
def chunk_documents(data: List[Dict[str, Any]], *args, **kwargs):
    documents = []
    for idx, item in enumerate(data):
        course = item['course']
        for doc in item['documents']:
            doc['course'] = course
            # previously we used just "id" for document ID
            doc['document_id'] = generate_document_id(doc)
            documents.append(doc)

    print(len(documents))

    return documents
