from logging import getLogger

from pydantic import BaseModel

logger = getLogger(__name__)


class SearchRequest(BaseModel):
    system_prompt: str = "You are a helpful assistant. You are here to help the user with their questions."
    prompt: str = "Who is the president of the United States?"
