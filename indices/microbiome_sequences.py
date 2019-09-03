index = {
    "settings": {
        "index": {
            "number_of_shards": 14,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "microbiome_sequence": {
            "properties": {
                "created": {
                    "type": "date",
                    "format": "epoch_second"
                },
                "dataset": {
                    "type": "keyword"
                },
                "osu_id": {
                    "type": "long"
                },
                "pctsim": {
                    "type": "float"
                },
                "copy_number": {
                    "type": "integer"
                },
                "qseqid": {
                    "type": "integer"
                },
                "species": {
                    "type": "keyword"
                },
                "sequence": {
                    "type": "keyword",
                },
            }
        }
    }
}
