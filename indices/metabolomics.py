index = {
    "mappings": {
        "metabolite": {
            "properties": {
                "cohort": {
                    "type": "keyword"
                },
                "MS_method": {
                    "type": "keyword"
                },
                "created": {
                    "type": "date",
                    "format": "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"
                },
                "features": {
                    "type": "nested",
                    "properties": {
                        "local_ID": {
                            "type": "keyword"
                        },
                        "MZ": {
                            "type": "double"
                        },
                        "RT": {
                            "type": "double"
                        },
                        "ML_score": {
                            "type": "float"
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
                        }
                    }
                }
            }
        }
    }
}
