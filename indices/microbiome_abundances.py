index = {
    "settings": {
        "index": {
            "number_of_shards": 14,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "microbiome_abundance": {
            "properties": {
                "created": {
                    "type": "date",
                    "format": "epoch_second"
                },
                "dataset": {
                    "type": "keyword"
                },
                "sample_id": {
                    "type": "keyword"
                },
                "osu_id": {
                    "type": "long"
                },
                "osu_count": {
                    "type": "integer"
                },
                "pctsim": {
                    "type": "float"
                },
                "species": {
                    "type": "keyword"
                },
            }
        }
    }
}
