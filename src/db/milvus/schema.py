from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, utility


def _create_milvus_documents_collection():
    collection_name = "documents"

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="user_id", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="document_id", dtype=DataType.VARCHAR, max_length=1024),
        FieldSchema(name="chunk_id", dtype=DataType.VARCHAR, max_length=1024),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="document_metadata", dtype=DataType.JSON),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR,
                    dim=1536)
    ]
    schema = CollectionSchema(
        fields=fields, description="Document collection schema", enable_dynamic_field=False)

    collection = Collection(collection_name, schema)

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {
            "nlist": 256
        }
    }

    collection.create_index(field_name="embedding", index_params=index_params)
    collection.create_index(field_name="user_id")
    collection.create_index(field_name="document_id")

    collection.flush()

    return collection


def get_milvus_documents_collection():
    if utility.has_collection("documents"):
        return Collection("documents")
    else:
        return _create_milvus_documents_collection()
