index = {
    "mappings": {
        "metabolite_sample": {
            "properties": {
                "cohort": {
                    "type": "keyword"
                },
                 "created": {
                    "type": "date",
                    "format": "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"
                },
                "local_ID": {
                    "type": "keyword"
                },
                "measurement_normalized": {
                    "type": "double"
                },
                "measurement_raw": {
                    "type": "double"
                },
                "method": {
                    "type": "keyword"
                },
                "ML_score": {
                    "type": "float"
                },
                "MZ": {
                    "type": "double"
                },
                "plate_well": {
                    "type": "keyword"
                },
                "RT": {
                    "type": "double"
                },
                "sample_barcode": {
                    "type": "keyword"
                },
                "subject": {
                    "type": "keyword"
                }
            }
        }
    }
}