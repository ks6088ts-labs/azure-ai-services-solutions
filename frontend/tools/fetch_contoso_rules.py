# GitHub: https://github.com/naotaka1128/llm_app_codes/chapter_010/tools/fetch_qa_content.py

from os import getenv

from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from langchain_openai import AzureOpenAIEmbeddings


class FetchContentInput(BaseModel):
    """型を指定するためのクラス"""

    query: str = Field()


def get_embeddings():
    return AzureOpenAIEmbeddings(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=getenv("AZURE_OPENAI_MODEL_EMBEDDING"),
    )


def create_azure_search(index_name: str) -> AzureSearch:
    return AzureSearch(
        azure_search_endpoint=getenv("AZURE_AI_SEARCH_ENDPOINT"),
        azure_search_key=getenv("AZURE_AI_SEARCH_API_KEY"),
        index_name=index_name,
        embedding_function=get_embeddings().embed_query,
        additional_search_client_options={"retry_total": 4},
    )


@tool(args_schema=FetchContentInput)
def fetch_contoso_rules(query):
    """
    Contoso 社の就業規則情報から、関連するコンテンツを見つけるツールです。
    Contoso 社に関する具体的な知識を得るのに役立ちます。

    このツールは `similarity`（類似度）と `content`（コンテンツ）を返します。
    - 'similarity'は、回答が質問にどの程度関連しているかを示します。
        値が高いほど、質問との関連性が高いことを意味します。
        'similarity'値が0.5未満のドキュメントは返されません。
    - 'content'は、質問に対する回答のテキストを提供します。
        通常、よくある質問とその対応する回答で構成されています。

    空のリストが返された場合、ユーザーの質問に対する回答が見つからなかったことを意味します。
    その場合、ユーザーに質問内容を明確にしてもらうのが良いでしょう。

    Returns
    -------
    List[Dict[str, Any]]:
    - page_content
      - similarity: float
      - content: str
    """
    db = create_azure_search("contoso_rules")
    docs = db.similarity_search_with_relevance_scores(
        query=query,
        k=3,
        score_threshold=0.5,
    )
    return [
        {
            "similarity": similarity,
            "content": i.page_content,
        }
        for i, similarity in docs
    ]


if __name__ == "__main__":
    import logging

    from dotenv import load_dotenv

    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: " "%(message)s",
        level=logging.DEBUG,
        force=True,
    )

    load_dotenv()
    docs = fetch_contoso_rules("ドレスコード")
    for doc in docs:
        print(doc)
