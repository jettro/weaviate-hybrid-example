import json
from uuid import uuid4

from person_class_obj import person_class_obj
from weaviate_client import WeaviateClient


def restart():
    weaviate_client.clean_schema()


def load_persons_from_file(file_name):
    persons = []
    input_file = open(file=file_name, mode='r', encoding='utf-8')
    for line in input_file:
        line_obj = json.loads(line)
        line_obj["id"] = uuid4()
        persons.append(line_obj)
    input_file.close()
    print(persons)
    return persons


def print_raw_json(results):
    print(json.dumps(results, indent=2))


def print_results(results):
    persons = results["data"]["Get"]["Person"]

    print("Number of found persons: {0}".format(len(persons)))
    for person in persons:
        try:
            print("{0} ({2}): {1}".format(person["name"], person["description"], person["_additional"]["distance"]))
        except KeyError:
            print("{0} : {1}".format(person["name"], person["description"]))


if __name__ == "__main__":
    init = False
    weaviate_client = WeaviateClient(connection_url="http://localhost:8080")

    if init:
        restart()
        weaviate_client.create_class(person_class_obj)
        weaviate_client.load_data(load_persons_from_file("./crawlluminis/blogs.jsonl"))
        weaviate_client.flush_bulk()

    # print_raw_json(weaviate_client.get_schema())
    # print_raw_json(weaviate_client.all_data())

    # search_term = "mobiele website"
    # search_term = "zoek expert"
    search_term = "ervaren frontender"
    print("*********** Dense **************")
    print_results(weaviate_client.dense_search(search_term))
    print("*********** Sparse *************")
    print_results(weaviate_client.sparse_search(search_term))
    print("*********** Hybrid *************")
    print_results(weaviate_client.hybrid_search(search_term))
