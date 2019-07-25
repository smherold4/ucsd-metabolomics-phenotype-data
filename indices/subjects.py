index = {
    "mappings": {
        "subject": {
            "properties": {
                "SUBJECT": {
                    "type": "keyword"
                },
                "COHORT": {
                    "type": "keyword"
                },
                "phenotypes": {
                    "type": "nested",
                    "properties": {
                        "name": {
                            "type": "keyword"
                        },
                        "float": {
                            "type": "double"
                        },
                        "integer": {
                            "type": "integer"
                        },
                        "boolean": {
                            "type": "boolean"
                        },
                        "string": {
                            "type": "keyword"
                        }
                    }
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
