index = {
    "mappings": {
        "subject": {
            "properties": {
                "PLASMA_ID": {
                    "type": "keyword"
                },
                "COHORT": {
                    "type": "keyword"
                },
                "BL_AGE": {
                    "type": "float"
                },
                "BMI": {
                    "type": "float"
                },
                "CURR_SMOKE": {
                    "type": "boolean"
                },
                "SODIUM": {
                    "type": "integer"
                },
                "KY100_30": {
                    "type": "integer"
                },
                "metabolite_dataset": {
                    "type": "nested",
                    "properties": {
                        "source": {
                            "type": "keyword"
                        },
                        "sample_barcode": {
                            "type": "keyword"
                        },
                        "age_at_sample_collection": {
                            "type": "float"
                        },
                        "plate_well": {
                            "type": "keyword"
                        },
                        "method": {
                            "type": "keyword"
                        },
                        "normalization": {
                            "type": "keyword"
                        },
                        "measurements": {
                            "type": "nested",
                            "properties": {
                                "local_ID": {
                                    "type": "keyword"
                                },
                                "value": {
                                    "type": "float"
                                }
                            }
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
