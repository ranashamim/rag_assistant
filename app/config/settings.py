from pydantic_settings import BaseSettings, SettingsConfigDict

from app.models.enums import ChunkMethod


class Settings(BaseSettings):
    # Qdrant
    qdrant_host: str
    qdrant_port: int
    qdrant_collection_name: str

    # Embedding
    embedding_model_name: str
    embedding_dimension: int
    embedding_distance: str

    # Chunking
    chunk_method: ChunkMethod
    chunk_size: int
    chunk_overlap: int
    chunk_overlap_sentences: int
    semantic_chunk_percentile: int

    groq_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()