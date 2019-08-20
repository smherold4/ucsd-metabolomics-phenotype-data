index = {
    "settings" : {
        "index" : {
            "number_of_shards" : 72,
            "number_of_replicas" : 0
        }
    },
    "mappings": {
        "metabolite_sample": {
            "properties": {
                 "created": {
                    "type": "date",
                    "format": "yyyy-MM-dd'T'HH:mm:ss"
                },
                "local_ID": {
                    "type": "keyword"
                },
                "measurement": {
                    "type": "double"
                },
                "normalization": {
                    "type": "keyword"
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
                },
                "study": {
                    "type": "keyword"
                },
            }
        }
    }
}
