from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymilvus import MilvusClient, DataType, CollectionSchema
from langchain.embeddings.ollama import OllamaEmbeddings
import fitz 
from django.conf import settings
import os

# file_path requires file to be passed as file_name.pdf

class VectorDatabaseService():
    # This service is a singleton research vector database service. It performs actions ONLY on research
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(VectorDatabaseService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, reset_collection = False, embeddings = OllamaEmbeddings):
        if hasattr(self, '_initialized') and self._initialized:
            return
        # print("INIT CALLED")

        system = os.name
        self.client = MilvusClient(uri=settings.VECTOR_DATABASES[system]['SOURCE'],
                                   token=settings.VECTOR_DATABASES[system]['TOKEN'])
        self.collection_name = settings.VECTOR_DATABASES[system]['COLLECTION']

        self.embeddings = embeddings(model=settings.AI_MODEL_NAME)
        
        
        if reset_collection:
            if self.client.has_collection(self.collection_name):
                self.drop_collection()
            self.client.create_collection(
                collection_name = self.collection_name,
                dimension = 4096,  # Vector size of Ollama Embeddings
                schema = self._create_schema()
            ) 
            self.client.create_index(
                collection_name=self.collection_name,
                index_params=self._create_params()
            )

        if not self.is_collection_loaded():
            self.client.load_collection(collection_name=self.collection_name)\

        self._initialized = True

    def is_collection_loaded(self) -> bool:
        res = self.client.get_load_state(
            collection_name=self.collection_name
        )
        return str(res['state']) == "Loaded"

    def drop_collection(self):
        self.client.drop_collection(collection_name = self.collection_name)

    def _create_params(self):
        index_params = MilvusClient.prepare_index_params()

        index_params.add_index(
            field_name="vector", # Name of the vector field to be indexed
            index_type="FLAT", # Type of the index to create
            index_name="vector_index", # Name of the index to create
            metric_type="COSINE", # Metric type used to measure similarity
            params={
                "nlist": 64, # Number of clusters for the index
            } # Index building params
        )

        return index_params

    def _create_schema(self) -> CollectionSchema:
        schema = MilvusClient.create_schema()
        schema.add_field(
            field_name = "id",
            datatype = DataType.INT64,
            is_primary = True,
            auto_id = True
        )
        schema.add_field(
            field_name = "vector",
            datatype = DataType.FLOAT_VECTOR,
            dim = 4096
        )
        schema.add_field(
            field_name = "text",
            datatype = DataType.VARCHAR,
            max_length = 65535
        )
        schema.add_field(
            field_name = "research_title",
            datatype = DataType.VARCHAR,
            max_length = 100
        )
        return schema

    def add_file(self, file_path: str):
        if not self.is_collection_loaded():
            self.client.load_collection(collection_name=self.collection_name)
        file_path = os.path.basename(file_path)
        if self.file_exists(file_path):
            # print(f"File '{file_path}' already exists. Skipping insertion.")
            return
        absolute_path = os.path.join(settings.RESEARCH_FILES_DIR, file_path)
        doc = fitz.open(str(absolute_path))
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        if not full_text.strip():
            print("No text found in PDF.")
            return
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        chunks = splitter.split_text(full_text)
        
        embeddings = self.embeddings.embed_documents(chunks)

        data = [{
            "vector": vec,
            "text": chunks[i],
            "research_title": file_path
        } for i, vec in enumerate(embeddings)]

        res = self.client.insert(
            collection_name=self.collection_name,
            data=data,
        )

        print(f"Inserted {len(data)} chunks from '{file_path}' into '{self.collection_name}'.")
        return res

    def delete_file(self, file_path):
        if not self.is_collection_loaded():
            self.client.load_collection(collection_name=self.collection_name)
        file_path = os.path.basename(file_path)
        res = self.client.delete(
            collection_name=self.collection_name,
            filter=f"research_title == '{file_path}'",
        )
        return res

    def update_file(self, file_path):
        if not self.is_collection_loaded():
            self.client.load_collection(collection_name=self.collection_name)
        file_path = os.path.basename(file_path)
        self.delete_file(file_path)
        res = self.add_file(file_path)
        return res

    def file_exists(self, file_path: str) -> bool:
        # This method queries collection to check if the file exists by its title
        if not self.is_collection_loaded():
            self.client.load_collection(collection_name=self.collection_name)
        file_path = os.path.basename(file_path)
        result = self.client.query(
            collection_name=self.collection_name,
            filter=f"research_title == '{file_path}'",
            limit=1,
            consistency_level = "Strong"
        )
        return len(result) > 0  # If a result is found, it means the file exists
    
    def list_files(self, limit = 2000):
        if not self.is_collection_loaded():
            self.client.load_collection(collection_name=self.collection_name)
        result = self.client.query(
            collection_name=self.collection_name,
            limit = limit,
            output_fields=["id", "research_title"]
        )

        return result
    
    def get_file_text(self, file_path) -> str:
        if not self.is_collection_loaded():
            self.client.load_collection(collection_name=self.collection_name)
        file_path = os.path.basename(file_path)
        self.client.load_collection(collection_name=self.collection_name)
        result = self.client.query(
            collection_name=self.collection_name,
            filter=f"research_title == '{file_path}'",
            output_fields=["text"]
        )

        plain_text = ''.join(row['text'] for row in result)

        return plain_text
    
    def get_file_embeddings(self, file_path) -> List[dict]:
        if not self.is_collection_loaded():
            self.client.load_collection(collection_name=self.collection_name)
        file_path = os.path.basename(file_path)
        result = self.client.query(
            collection_name=self.collection_name,
            filter=f"research_title == '{file_path}'",
            output_fields=["vector"]
        )

        return result

    def find_similar(self, query: str, source: str = None, top_k: int = 3):
        # Embed the query
        if not self.is_collection_loaded():
            self.client.load_collection(collection_name=self.collection_name)
        query_vectors = self.embeddings.embed_query(query)
        source = os.path.basename(source)

        # Search in the collection
        if source is not None:
            results = self.client.search(
                collection_name = self.collection_name,
                anns_field="vector",
                data = [query_vectors],
                filter=f"research_title == '{source}'",
                limit = top_k,
                output_fields = ["text", "research_title"],
            )
        else:
            results = self.client.search(
                collection_name = self.collection_name,
                anns_field="vector",
                data = [query_vectors],
                limit = top_k,
                output_fields = ["text", "research_title"],
            )

        # Parse and return results
        hits = results[0]  # Each query returns a list of hits
        similar_results = [{
            "text": hit["entity"]["text"],
            "research_title": hit["entity"]["research_title"],
            "score": hit["distance"]
        } for hit in hits]
        self.client.release_collection(collection_name=self.collection_name)
        

        return similar_results

def main():
    print("Hello world2")
    vectorstore = VectorDatabaseService(reset_collection=False)
    # vectorstore.drop_collection()
    # vectorstore.add_file("rector.pdf")
    # vectorstore.add_file("NumericalMethodsResearchPaper.pdf")
    results = vectorstore.find_similar("What it cubic spline?", top_k=1)
    for i, res in enumerate(results):
        print(f"\nResult {i + 1}:")
        print(f"Score: {res['score']}")
        print(f"Title: {res['research_title']}")
        print(f"Text: {res['text']}...")

if __name__ == "__main__":
    main()