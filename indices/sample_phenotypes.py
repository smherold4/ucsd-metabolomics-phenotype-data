index = {
    "settings": {
        "index": {
            "number_of_shards": 18,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "sample_phenotype": {
            "properties": {
                "subject": {
                    "type": "keyword"
                },
                "sample_barcode": {
                    "type": "keyword",
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
