index = {
    "settings": {
        "index": {
            "number_of_shards": 10,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "subject_phenotype": {
            "properties": {
                "subject": {
                    "type": "keyword"
                },
                "name": {
                    "type": "keyword"
                },
                "float": {
                    "type": "double"
                },
                "integer": {
                    "type": "integer"
                },
                "boolean": {
                    "type": "boolean"
                },
                "string": {
                    "type": "keyword"
                },
                "study": {
                    "type": "keyword"
                },
            }
        }
    }
}
