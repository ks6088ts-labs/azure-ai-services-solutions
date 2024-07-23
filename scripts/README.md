## How to use the scripts

```shell
# Install dependencies
make install-deps-dev

# Help
poetry run python scripts/manage_vector_store.py --help

VECTOR_STORE_TYPE=faiss

# Create a new vector store in local
poetry run python scripts/manage_vector_store.py create --vector-store-type $VECTOR_STORE_TYPE

# Search for similar vectors
poetry run python scripts/manage_vector_store.py search --vector-store-type $VECTOR_STORE_TYPE
```
