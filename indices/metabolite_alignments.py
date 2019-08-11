index = {
    "settings" : {
        "index" : {
            "number_of_shards" : 14,
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
                        "cohort": {
                            "type": "keyword"
                        },
                        "local_ID": {
                            "type": "keyword"
                        }
                    }
                },
                "cohort": {
                    "type": "keyword"
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
                "source": {
                    "type": "keyword"
                }
            }
        }
    }
}