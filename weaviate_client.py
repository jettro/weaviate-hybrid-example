import json

import weaviate


class WeaviateClient:

    def __init__(self, connection_url="http://localhost:8080") -> None:
        super().__init__()
        self.distance = 0.6
        self.client = weaviate.Client(connection_url)

        self.client.batch.configure(
            batch_size=100,
            dynamic=True,
            timeout_retries=3,
            callback=None,
        )

    def get_schema(self):
        return self.client.schema.get()

    def all_data(self):
        return self.client.data_object.get()

    def clean_schema(self):
        self.client.schema.delete_all()

    def create_class(self, class_obj):
        self.client.schema.create_class(class_obj)

    def load_data(self, data):
        for item in data:
            if len(item["description"]) > 1:
                properties = {
                    "name": item["name"],
                    "description": item["description"]
                }
                self.client.batch.add_data_object(properties, "Person", item["id"])

    def flush_bulk(self):
        self.client.batch.flush()

    def dense_search(self, search_text: str):
        near_text = {
            "concepts": [search_text],
            "distance": self.distance
        }
        result = (
            self.client.query
            .get("Person", ["name", "description"])
            .with_additional(["certainty", "distance"])
            .with_near_text(near_text)
            .do()
        )

        return result

    def sparse_search(self, search_text: str):
        result = (
            self.client.query
            .get("Person", ["name", "description"])
            .with_bm25(query=search_text, properties=["name", "description"])
            .do()
        )

        return result

    def hybrid_search(self, search_text: str):
        # Interesting that you cannot provide a distance here, so recall is more important
        result = (
            self.client.query
            .get("Person", ["name", "description"])
            .with_hybrid(query=search_text, alpha=0.5)
            .do()
        )

        return result
