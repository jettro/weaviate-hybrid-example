author_class_obj = {
    "class": "Author",  # <= note the capital "A".
    "description": "A description of this class, in this case, it is about authors",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
            "model": "ada",
            "modelVersion": "002",
            "type": "text"
        }
    },
    "properties": [
        {
            "dataType": [
                "string"
            ],
            "description": "The name of the Author",
            "indexInverted": True,
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": False,
                    "vectorizePropertyName": False
                }
            },
            "name": "name",
            "tokenization": "word"
        },
        {
            "dataType": [
                "int"
            ],
            "description": "The age of the Author",
            "name": "age"
        },
        {
            "dataType": [
                "date"
            ],
            "description": "The date of birth of the Author",
            "name": "born"
        },
        {
            "dataType": [
                "boolean"
            ],
            "description": "A boolean value if the Author won a nobel prize",
            "name": "wonNobelPrize"
        },
        {
            "dataType": [
                "text"
            ],
            "description": "A description of the author",
            "name": "description",
            "indexInverted": True,
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": False,
                    "vectorizePropertyName": False
                }
            },
            "tokenization": "word"
        }
    ]
}

publication_class_obj = {
    "class": "Publication",
    "description": "A description of this class, in this case, it is about publications",
    "properties": [
        {
            "dataType": [
                "string"
            ],
            "description": "The name of the Publication",
            "name": "name",
        }
    ]
}

add_publisher_to_author = {
    "dataType": [
        "Publication"
    ],
    "name": "writesFor"
}

add_authors_to_publisher = {
    "dataType": [
        "Author"
    ],
    "name": "has"
}
