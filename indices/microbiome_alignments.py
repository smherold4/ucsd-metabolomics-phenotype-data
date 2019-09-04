index = {
    "settings": {
        "index": {
            "number_of_shards": 14,
            "number_of_replicas": 1
        },
        "analysis": {
            "tokenizer": {
                "strain_tokenizer": {
                    "type": "pattern",
                    "pattern": "[\_\,\s]", # tokenize on underscores, commas and spaces
                }
            },
            "analyzer": {
                "strain_analyzer": {
                    "tokenizer": "strain_tokenizer"
                }
            }
        },
    },
    "mappings": {
        "microbiome_alignment": {
            "properties": {
                "created": {
                    "type": "date",
                    "format": "epoch_second"
                },
                "study": {
                    "type": "keyword"
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
                    "type": "text",
                    "analyzer": "strain_analyzer",
                },
                "copy_number": {
                    "type": "integer"
                },
            }
        }
    }
}
