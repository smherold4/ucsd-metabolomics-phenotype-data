index = {
    "settings": {
        "index": {
            "number_of_shards": 14,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "microbiome_alignment": {
            "properties": {
                "created": {
                    "type": "date",
                    "format": "epoch_second"
                },
                "variant_id": {
                    "type": "keyword"
                },
                "qseqid": {
                    "type": "integer"
                },
                "length": {
                    "type": "integer"
                },
                "qstart": {
                    "type": "integer"
                },
                "qend": {
                    "type": "integer"
                },
                "sstart": {
                    "type": "integer"
                },
                "send": {
                    "type": "integer"
                },
                "slen": {
                    "type": "integer"
                },
                "score": {
                    "type": "integer"
                },
                "match": {
                    "type": "integer"
                },
                "mismatch": {
                    "type": "integer"
                },
                "gapopen": {
                    "type": "integer"
                },
                "gapextend": {
                    "type": "float"
                },
                "pctsim": {
                    "type": "float"
                },
                "strain": {
                    "type": "keyword"
                },
                "copy_number": {
                    "type": "integer"
                },
            }
        }
    }
}
