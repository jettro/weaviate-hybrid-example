import weaviate
import json

from class_author import author_class_obj, publication_class_obj, add_publisher_to_author, add_authors_to_publisher

client = weaviate.Client("http://localhost:8080")
client.batch.configure(
  batch_size=100,
  dynamic=True,
  timeout_retries=3,
  callback=None,
)


def read_schema():
    return client.schema.get()


def clean_schema():
    client.schema.delete_all()


def create_class(class_obj):
    client.schema.create_class(class_obj)


def add_property_to_class(class_name: str, prop_obj: object):
    client.schema.property.create(class_name, prop_obj)


def prepare_schema():
    create_class(author_class_obj)
    create_class(publication_class_obj)
    add_property_to_class("Author", add_publisher_to_author)
    add_property_to_class("Publication", add_authors_to_publisher)

    print(json.dumps(read_schema(), indent=4))


def load_data_file():
    data_file = open('data.json')
    data = json.load(data_file)
    data_file.close()

    return data


def batch_import_publications(data):
    for publication in data['publications']:
        properties = {
            "name": publication["name"]
        }
        client.batch.add_data_object(properties, "Publication", publication["id"], publication["vector"])


def batch_import_authors(data):
    for author in data['authors']:
        properties = {
            "name": author["name"],
            "age": author["age"],
            "born": author["born"],
            "wonNobelPrize": author["wonNobelPrize"],
            "description": author["description"]
        }
        # client.batch.add_data_object(properties, "Author", author["id"], author["vector"])
        client.batch.add_data_object(properties, "Author", author["id"])


def import_data():
    data = load_data_file()
    batch_import_publications(data)
    client.batch.flush()
    batch_import_authors(data)
    client.batch.flush()


def dense_search(search_text: str):
    near_text = {
        "concepts": [search_text],
        "distance": 0.6
    }
    result = (
        client.query
        .get("Author", ["name", "description"])
        .with_additional(["certainty", "distance"])
        .with_near_text(near_text)
        .do()
    )

    print(json.dumps(result, indent=4))


def sparse_search(search_text: str):
    result = (
        client.query
        .get("Author", ["name", "description"])
        .with_bm25(query=search_text, properties=["name", "description"])
        .do()
    )

    print(json.dumps(result, indent=4))


def hibrid_search(search_text: str):
    result = (
        client.query
        .get("Author", ["name", "description"])
        .with_hybrid(query=search_text, alpha=0.5)
        .do()
    )

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    # print(json.dumps(read_schema(), indent=4))
    # clean_schema()
    # prepare_schema()
    # import_data()
    #
    all_objects = client.data_object.get()
    print(json.dumps(all_objects, indent=2))

    # dense_search("writes about economy")
    # sparse_search("writer")
    # hibrid_search("writes about economy")
