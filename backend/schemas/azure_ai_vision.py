from logging import getLogger

from pydantic import BaseModel

logger = getLogger(__name__)


class ImageAnalysisResponse(BaseModel):
    result: dict
