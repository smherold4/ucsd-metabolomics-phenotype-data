index = {
    "settings": {
        "index": {
            "number_of_shards": 14,
            "number_of_replicas": 1
        },
        "analysis": {
            "tokenizer": {
                "comma_whitespace_tokenizer": {
                    "type": "pattern",
                    "pattern": "[\,\s]",
                },
            },
            "analyzer": {
                "species_analyzer": {
                    "filter": ["lowercase"],
                    "tokenizer": "comma_whitespace_tokenizer",
                }
            }
        },
    },
    "mappings": {
        "microbiome_abundance": {
            "properties": {
                "ablog10": {
                    "type": "float",
                },
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
