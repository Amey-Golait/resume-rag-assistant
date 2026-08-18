from pathlib import Path

import chromadb
from chromadb import Collection

DEFAULT_COLLECTION_NAME = "resumes"


def get_collection(
    persist_dir: Path,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Collection:
    client = chromadb.PersistentClient(path=str(persist_dir))
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )


def store_embeddings(
    persist_dir: Path,
    chunks: list[str],
    embeddings: list[list[float]],
    source: str,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> int:
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length")

    if not chunks:
        return 0

    collection = get_collection(persist_dir, collection_name)
    ids = [f"{source}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )

    return len(chunks)


def search_chunks(
    persist_dir: Path,
    query_embedding: list[float],
    top_k: int = 5,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> list[dict]:
    collection = get_collection(persist_dir, collection_name)

    if collection.count() == 0:
        return []

    n_results = min(top_k, collection.count())
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    matches: list[dict] = []
    for i in range(len(results["ids"][0])):
        matches.append(
            {
                "id": results["ids"][0][i],
                "chunk": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
        )

    return matches
