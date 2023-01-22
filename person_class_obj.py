person_class_obj = {
    "class": "Person",
    "description": "This class represents a Person that is known to the system",
    "vectorizer": "text2vec-transformers",
    "moduleConfig": {
        "text2vec-transformer": {
            "poolingStrategy": "masked_mean",
            "vectorizeClassName": False
        }
    },
    "properties": [
        {
            "dataType": [
                "string"
            ],
            "description": "The name of the Person",
            "indexInverted": True,
            "moduleConfig": {
                "text2vec-transformers": {
                    "skip": False,
                    "vectorizePropertyName": False
                }
            },
            "name": "name"
        },
        {
            "dataType": [
                "text"
            ],
            "description": "A description of the person",
            "name": "description",
            "indexInverted": True,
            "moduleConfig": {
                "text2vec-transformers": {
                    "skip": False,
                    "vectorizePropertyName": False
                }
            }
        }
    ]
}
