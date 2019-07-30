index = {
    "mappings": {
        "subject": {
            "properties": {
                "cohort": {
                    "type": "keyword"
                },
                "subject": {
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
                "samples": {
                    "type": "nested",
                    "properties": {
                        "sample_barcode": {
                            "type": "keyword"
                        },
                        "source": {
                            "type": "keyword"
                        },
                        "age_at_sample_collection": {
                            "type": "float"
                        },
                        "metabolite_dataset": {
                            "type": "nested",
                            "properties": {
                                "plate_well": {
                                    "type": "keyword"
                                },
                                "method": {
                                    "type": "keyword"
                                },
                                "features": {
                                    "type": "nested",
                                    "properties": {
                                        "local_ID": {
                                            "type": "keyword"
                                        },
                                        "measurements": {
                                            "type": "nested",
                                            "properties": {
                                                "value": {
                                                    "type": "float"
                                                },
                                                "normalization": {
                                                    "type": "keyword"
                                                }
                                            }
                                        }
                                    }
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
