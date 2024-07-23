import logging
from enum import Enum
from os import getenv
from pprint import pprint
from typing import Annotated

import typer
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS, VectorStore
from langchain_community.vectorstores.azure_cosmos_db_no_sql import AzureCosmosDBNoSqlVectorSearch
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings

app = typer.Typer()


class VectorStoreType(str, Enum):
    Faiss = "faiss"
    AzureAISearch = "azureaisearch"
    AzureCosmosDbNoSql = "azurecosmosdbnosql"


def get_log_level(debug: bool) -> int:
    return logging.DEBUG if debug else logging.INFO


def setup_logging(debug: bool = False):
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: " "%(message)s",
        level=get_log_level(debug),
        force=True,
    )


def get_embeddings():
    return AzureOpenAIEmbeddings(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        model=getenv("AZURE_OPENAI_MODEL_EMBEDDING"),
    )


def get_cosmos_client():
    return CosmosClient(
        url=getenv("AZURE_COSMOSDB_ENDPOINT"),
        credential=getenv("AZURE_COSMOSDB_KEY"),
    )


def get_local_vector_store_path(identifier: str):
    return f"./artifacts/vectorstore/{identifier}"


def get_vector_embedding_policy():
    return {
        "vectorEmbeddings": [
            {
                "path": "/embedding",
                "dataType": "float32",
                "distanceFunction": "cosine",
                "dimensions": 1536,
            }
        ]
    }


def get_indexing_policy():
    return {
        "indexingMode": "consistent",
        "includedPaths": [{"path": "/*"}],
        "excludedPaths": [{"path": '/"_etag"/?'}],
        "vectorIndexes": [{"path": "/embedding", "type": "quantizedFlat"}],
    }


def create_azure_search(index_name: str) -> AzureSearch:
    return AzureSearch(
        azure_search_endpoint=getenv("AZURE_AI_SEARCH_ENDPOINT"),
        azure_search_key=getenv("AZURE_AI_SEARCH_API_KEY"),
        index_name=index_name,
        embedding_function=get_embeddings().embed_query,
        additional_search_client_options={"retry_total": 4},
    )


def get_vector_store(
    vector_store_type: VectorStoreType,
    identifier: str,
) -> VectorStore:
    if vector_store_type == VectorStoreType.Faiss:
        logging.info("Creating Faiss vector store")
        return FAISS.load_local(
            folder_path=get_local_vector_store_path(identifier),
            embeddings=get_embeddings(),
            allow_dangerous_deserialization=True,
        )
    elif vector_store_type == VectorStoreType.AzureAISearch:
        logging.info("Creating Azure AI Search vector store")
        return create_azure_search(identifier)
    elif vector_store_type == VectorStoreType.AzureCosmosDbNoSql:
        logging.info("Creating Azure Cosmos DB NoSQL vector store")
        cosmos_database_name = "langchain_python_db"
        return AzureCosmosDBNoSqlVectorSearch(
            cosmos_client=get_cosmos_client(),
            embedding=get_embeddings(),
            vector_embedding_policy=get_vector_embedding_policy(),
            indexing_policy=get_indexing_policy(),
            cosmos_container_properties={"partition_key": PartitionKey(path="/id")},
            cosmos_database_properties={"id": cosmos_database_name},
            database_name=cosmos_database_name,
            container_name="langchain_python_container",
        )


def create_vector_store(
    vector_store_type: VectorStoreType,
    identifier: str,
    documents: list[Document],
) -> VectorStore:
    if vector_store_type == VectorStoreType.Faiss:
        logging.info("Creating Faiss vector store")
        vector_store: FAISS = FAISS.from_documents(
            documents=documents,
            embedding=get_embeddings(),
        )
        vector_store.save_local(folder_path=get_local_vector_store_path(identifier))
        return
    elif vector_store_type == VectorStoreType.AzureAISearch:
        logging.info("Creating Azure AI Search vector store")
        vector_store = create_azure_search(identifier)
        vector_store.add_documents(documents=documents)
        return
    elif vector_store_type == VectorStoreType.AzureCosmosDbNoSql:
        logging.info("Creating Azure Cosmos DB NoSQL vector store")
        cosmos_database_name = "langchain_python_db"

        AzureCosmosDBNoSqlVectorSearch.from_documents(
            documents=documents,
            embedding=get_embeddings(),
            cosmos_client=get_cosmos_client(),
            database_name=cosmos_database_name,
            container_name="langchain_python_container",
            vector_embedding_policy=get_vector_embedding_policy(),
            indexing_policy=get_indexing_policy(),
            cosmos_database_properties={"id": cosmos_database_name},
            cosmos_container_properties={"partition_key": PartitionKey(path="/id")},
        )
        return


@app.command()
def create(
    input_csv_file_path: Annotated[str, typer.Option(help="Path to the input CSV file")] = "./data/contoso_rules.csv",
    identifier="contoso_rules",
    vector_store_type: Annotated[VectorStoreType, typer.Option(case_sensitive=False)] = VectorStoreType.Faiss,
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    setup_logging(debug)

    # Load documents from CSV
    try:
        documents = CSVLoader(file_path=input_csv_file_path).load()
    except Exception as e:
        logging.error(f"Failed to load documents from CSV: {e}")
        return

    # Create vector store
    create_vector_store(
        vector_store_type=vector_store_type,
        identifier=identifier,
        documents=documents,
    )


@app.command()
def search(
    identifier="contoso_rules",
    vector_store_type: Annotated[VectorStoreType, typer.Option(case_sensitive=False)] = VectorStoreType.Faiss,
    query: Annotated[str, typer.Option(help="Query to search")] = "社内の機密情報は外部に漏らさないでください",
    k: Annotated[int, typer.Option(help="Number of documents to retrieve")] = 5,
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    setup_logging(debug)

    # Create vector store
    vector_store = get_vector_store(
        vector_store_type=vector_store_type,
        identifier=identifier,
    )

    # Search
    got_documents = vector_store.similarity_search(
        query=query,
        k=k,
    )
    for document in got_documents:
        pprint(document.page_content)


if __name__ == "__main__":
    load_dotenv()
    app()
