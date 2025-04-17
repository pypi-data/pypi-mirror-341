from typing import Any, Dict, List, Optional
from langchain_aws import BedrockEmbeddings
from langchain_community.embeddings.mlflow import MlflowEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

from fairo.settings import get_mlflow_gateway_embeddings_route, get_mlflow_gateway_uri

AWS_AI_EMBEDDING_MODEL = 'cohere.embed-english-v3'


class BaseVectorStore:
    pass


class PostgresVectorStore(BaseVectorStore):
    """
    A PostgreSQL-based vector store using LangChain and pgvector
    """

    def __init__(
            self,
            collection_name: str,
            embedding_model_id: str = AWS_AI_EMBEDDING_MODEL,
            region_name: str = None,
            collection_metadata: dict = None,
            connection_string: str = "postgresql://postgres:postgres@localhost:5432/vectordb",
            pre_delete_collection: bool = False,
            default_k: int = 5
    ):
        """
        Args:
            collection_name: Name of the collection in PostgreSQL
            embedding_model_id: Bedrock embedding model ID
            region_name: AWS region for Bedrock
            collection_metadata: Dict for what metadata we want to add to collection
            connection_string: PostgreSQL connection string
        """
        self.collection_name = collection_name
        self.connection_string = connection_string

        # Set up embeddings
        self.embeddings = MlflowEmbeddings(
            target_uri=get_mlflow_gateway_uri(),
            endpoint=get_mlflow_gateway_embeddings_route(),
        )

        if collection_metadata is not None:
            self.collection_metadata = collection_metadata

        # Initialize the PGVector store
        self.db = PGVector(
            collection_name=collection_name,
            connection=connection_string,
            collection_metadata=self.collection_metadata,
            embeddings=self.embeddings,
            pre_delete_collection=pre_delete_collection
        )

        self.default_k = default_k

    def add_documents(self, documents: List[Document]) -> None:
        """
        Args:
            documents: List of Document objects to add
        """
        if not documents:
            return
        
        # Add documents to PGVector
        self.db.add_documents(documents)

    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Args:
            texts: List of text strings to add
            metadatas: Optional list of metadata dictionaries
        """
        if not texts:
            return

        # Convert to Document objects
        documents = []
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            documents.append(Document(page_content=text, metadata=metadata))

        # Add to vector store
        self.add_documents(documents)

    @staticmethod
    def _format_query(query):
        # Temporary fix, need to consider model / do more than truncate
        return query[0:2048]

    def similarity_search(self, query: str, k: int = None) -> List[Document]:
        """
        Args:
            query: The search query
            k: Number of results to return
        """
        formatted_query = self._format_query(query)
        if k is None:
            k = self.default_k
        return self.db.similarity_search(formatted_query, k=k)

    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple[Document, float]]:
        """
        Args:
            query: The search query
            k: Number of results to return
        """
        formatted_query = self._format_query(query)
        if k is None:
            k = self.default_k
        return self.db.similarity_search_with_score(formatted_query, k=k)

    def delete(self) -> None:
        """Delete the collection from PostgreSQL."""
        try:
            # Use the internal PGVector method to delete a collection
            self.db._client.delete_collection(self.collection_name)
        except Exception as e:
            print(f"Error deleting collection: {str(e)}")

    @classmethod
    def from_existing(cls, 
                     collection_name: str,
                     embedding_model_id: str = AWS_AI_EMBEDDING_MODEL,
                     region_name: str = None,
                     connection_string: str = "postgresql://postgres:postgres@localhost:5432/vectordb"):
        """
        Load an existing collection from PostgreSQL.
        
        Args:
            collection_name: Name of the existing collection
            embedding_model_id: Bedrock embedding model ID
            region_name: AWS region for Bedrock
            connection_string: PostgreSQL connection string
            
        Returns:
            PostgresVectorStore instance connected to the existing collection
        """
        return cls(
            collection_name=collection_name,
            embedding_model_id=embedding_model_id,
            region_name=region_name,
            connection_string=connection_string
        )