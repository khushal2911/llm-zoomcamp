
from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch, exceptions

query = "When is the next cohort?"

@data_loader
def search(*args, **kwargs) -> List[Dict]:
    """
    query_embedding: Union[List[int], np.ndarray]
    """
    
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = kwargs.get('index_name', 'documents')
    source = kwargs.get('source', "cosineSimilarity(params.query_vector, 'embedding') + 1.0")
    top_k = kwargs.get('top_k', 5)
    chunk_column = kwargs.get('chunk_column', 'content')

    search_query = {
                    "size": 5,
                    "query": {
                        "bool": {
                            "must": {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["question", "text", "section"],
                                    "type": "best_fields"
                                }
                            },
                        }
                    }
    }

    #if isinstance(query_embedding, np.ndarray):
        #query_embedding = query_embedding.tolist()


    print("Sending search_query:", query)

    es_client = Elasticsearch(connection_string)
    
    try:
        response = es_client.search(
            index=index_name,
            body=search_query
        )

        print("Raw response from Elasticsearch:", response)

        return [hit['_source'] for hit in response['hits']['hits']]
    
    except exceptions.BadRequestError as e:
        print(f"BadRequestError: {e.info}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
