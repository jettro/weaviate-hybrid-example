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

    def load_data(self, data: list, class_name: str, property_mapper):
        """
        The data object is a list of objects. The object must have the property id.
        :param property_mapper: Returns a properties object or None if the item is not valid
        :param class_name: String containing the name of the Weaviate class
        :param data: List of data objects
        :return:
        """
        for item in data:
            properties = property_mapper(item)
            if properties:
                self.client.batch.add_data_object(properties, class_name, item["id"])

    def flush_bulk(self):
        self.client.batch.flush()

    def dense_search(self, search_text: str, class_name: str, fields: list[str]):
        near_text = {
            "concepts": [search_text],
            "distance": self.distance
        }
        result = (
            self.client.query
            .get(class_name=class_name, properties=fields)
            .with_additional(["certainty", "distance"])
            .with_near_text(near_text)
            .do()
        )

        return result

    def sparse_search(self, search_text: str, class_name: str, fields: list[str]):
        result = (
            self.client.query
            .get(class_name=class_name, properties=fields)
            .with_bm25(query=search_text, properties=fields)
            .with_additional(["score", "explainScore"])
            .do()
        )

        return result

    def hybrid_search(self, search_text: str, class_name: str, fields: list[str]):
        # Interesting that you cannot provide a distance here, so recall is more important
        result = (
            self.client.query
            .get(class_name=class_name, properties=fields)
            .with_hybrid(query=search_text, alpha=0.5)
            .with_additional(["score", "explainScore"])
            .do()
        )

        return result
