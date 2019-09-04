index = {
    "settings": {
        "index": {
            "number_of_shards": 14,
            "number_of_replicas": 1
        },
        "analysis": {
            "tokenizer": {
                "species_tokenizer": {
                    "type": "pattern",
                    "pattern": "[\_\,\s]", # tokenize on underscores, commas and spaces
                }
            },
            "analyzer": {
                "species_analyzer": {
                    "tokenizer": "species_tokenizer"
                }
            }
        }
    },
    "mappings": {
        "microbiome_abundance": {
            "properties": {
                "created": {
                    "type": "date",
                    "format": "epoch_second"
                },
                "study": {
                    "type": "keyword"
                },
                "subjectID": {
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
                    "type": "text",
                    "analyzer": "species_analyzer",
                },
            }
        }
    }
}
