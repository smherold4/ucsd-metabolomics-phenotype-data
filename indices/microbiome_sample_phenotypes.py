index = {
    "settings": {
        "index": {
            "number_of_shards": 14,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "microbiome_sample_phenotype": {
            "properties": {
                "created": {
                    "type": "date",
                    "format": "epoch_second"
                },
                "study": {
                    "type": "keyword"
                },
                "subject": {
                    "type": "keyword"
                },
                "sample_id": {
                    "type": "keyword"
                },
                "variable": {
                    "type": "keyword"
                },
                "value": {
                    "type": "text",
                    "analyzer": "english",
                },
            }
        }
    }
}
