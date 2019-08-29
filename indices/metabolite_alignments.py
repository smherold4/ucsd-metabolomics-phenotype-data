index = {
    "settings" : {
        "index" : {
            "number_of_shards" : 22,
            "number_of_replicas" : 1
        }
    },
    "mappings": {
        "metabolite_alignment": {
            "properties": {
                "ML_score": {
                    "type": "float"
                },
                "MZ": {
                    "type": "double"
                },
                "RT": {
                    "type": "double"
                },
                "alignment": {
                    "type": "nested",
                    "properties": {
                        "local_ID": {
                            "type": "keyword"
                        },
                        "study": {
                            "type": "keyword"
                        },
                    }
                },
                "cross_variation": {
                    "type": "double"
                },
                "local_ID": {
                    "type": "keyword"
                },
                "method": {
                    "type": "keyword"
                },
                "prevalence": {
                    "type": "float"
                },
                "source": {
                    "type": "keyword"
                },
                "study": {
                    "type": "keyword"
                },
            }
        }
    }
}
