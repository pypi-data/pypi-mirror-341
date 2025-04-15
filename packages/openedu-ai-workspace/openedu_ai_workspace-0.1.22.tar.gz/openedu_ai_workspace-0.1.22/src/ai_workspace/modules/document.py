from ai_workspace.schemas import DocumentSchema
from ai_workspace.database import MongoDB
from snowflake import SnowflakeGenerator


class Document:
    def __init__(self, mongodb_url: str):
        self.mongodb = MongoDB(mongodb_url)
        self.id_generator = SnowflakeGenerator(42)

    def upload_document(self, document_data: DocumentSchema):
        document_data.document_id = next(self.id_generator)
        documents_dict = document_data.model_dump(exclude_unset=True)
        collection = self.mongodb.db["documents"]
        result = collection.insert_one(documents_dict).inserted_id
        return str(result)
