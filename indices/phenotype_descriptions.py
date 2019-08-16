index = {
    "settings" : {
        "index" : {
            "number_of_shards" : 5,
            "number_of_replicas" : 1
        },
        "analysis": {
            "filter": {
                "english_stop": {
                    "type":       "stop",
                    "stopwords":  "_english_" 
                },
                "english_keywords": {
                    "type":       "keyword_marker",
                    "keywords":   ["example"] 
                },
                "english_stemmer": {
                    "type":       "stemmer",
                    "language":   "english"
                },
                "english_possessive_stemmer": {
                    "type":       "stemmer",
                    "language":   "possessive_english"
                }
            },
            "analyzer": {
                "phenotype_description_analyzer": {
                    "tokenizer":  "standard",
                    "filter": [
                        "english_possessive_stemmer",
                        "lowercase",
                        "english_stop",
                        "english_keywords",
                        "english_stemmer"
                    ]
                }
            }
        }
    },
    "mappings": {
        "phenotype_description": {
            "properties": {
                "cohort": {
                    "type": "keyword"
                },
                "datatype": {
                    "type": "keyword"
                },
                "description": {
                    "type": "text",
                    "analyzer": "phenotype_description_analyzer"
                },
                "variable_name": {
                    "type": "keyword"
                },
            }
        }
    }
}
