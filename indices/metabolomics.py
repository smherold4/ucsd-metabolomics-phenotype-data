index = {
    "mappings": {
        "metabolite": {
            "properties": {
                "COHORT": {
                    "type": "keyword"
                },
                "subject": {
                    "type": "keyword"
                },
                "sample_barcode": {
                    "type": "keyword"
                },
                "plate_well": {
                    "type": "keyword"
                },
                "age_at_sample_collection": {
                    "type": "float"
                },
                "source": {
                    "type": "keyword"
                },
                "MS_method": {
                    "type": "keyword"
                },
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
                "measurement": {
                    "type": "nested",
                    "properties": {
                        "normalization": {
                            "type": "keyword"
                        },
                        "value": {
                            "type": "double"
                        }
                    }
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
                "created": {
                    "type": "date",
                    "format": "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"
                },
            }
        }
    }
}
