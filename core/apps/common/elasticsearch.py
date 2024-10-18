from dataclasses import dataclass

from httpx import Client, post


@dataclass
class ElasticClient:
    http_client: Client

    def upsert_index(self, index: str, document_id: int | str, document: dict):
        response = self.http_client.post(
            f"{index}/_update/{document_id}",
            json={
                "doc": document,
                "doc_as_upsert": True,
            },
        )
        response.raise_for_status()


def search_with_elastic(query: str) -> list:
    response = post(
        "http://elasticsearch:9200/title-index/_search",
        json={
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title^4", "description^3"],
                                "type": "best_fields",
                                "operator": "or",
                                "fuzziness": "AUTO",
                                "tie_breaker": 0.3,
                            }
                        },
                        {
                            "match_phrase": {
                                "title": {"query": query, "boost": 3, "slop": 5}
                            }
                        },
                        {
                            "match_phrase": {
                                "description": {
                                    "query": query,
                                    "boost": 2,
                                    "slop": 5,
                                }
                            }
                        },
                    ],
                    "minimum_should_match": "50%",
                }
            },
        },
    )

    response.raise_for_status()
    ids = [i.get("_source").get("id") for i in response.json().get("hits").get("hits")]
    return ids
