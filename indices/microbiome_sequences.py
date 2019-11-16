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
            },
            "normalizer": {
                "dna_sequence_normalizer": {
                    "type": "custom",
                    "filter": ["lowercase"],
                },
            },
        },
    },
    "mappings": {
        "microbiome_sequence": {
            "properties": {
                "created": {
                    "type": "date",
                    "format": "epoch_second"
                },
                "study": {
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
                    "type": "text",
                    "analyzer": "species_analyzer",
                },
                "sequence": {
                    "type": "keyword",
                    "normalizer": "dna_sequence_normalizer",
                },
                "kingdom": {
                    "type": "text",
                    "analyzer": "species_analyzer",
                },
                "phylum": {
                    "type": "text",
                    "analyzer": "species_analyzer",
                },
                "class": {
                    "type": "text",
                    "analyzer": "species_analyzer",
                },
                "order": {
                    "type": "text",
                    "analyzer": "species_analyzer",
                },
                "family": {
                    "type": "text",
                    "analyzer": "species_analyzer",
                },
                "genus": {
                    "type": "text",
                    "analyzer": "species_analyzer",
                },
            }
        }
    }
}
