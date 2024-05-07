import logging

from frontend.solutions import azure_ai_vision, azure_storage, document_intelligence, sandbox, transcription
from frontend.solutions.types import SolutionType

logger = logging.getLogger(__name__)


def start(
    solution_name: str,
    backend_url: str,
    log_level: int,
) -> None:
    try:
        solutions = {
            SolutionType.SANDBOX.value: sandbox.start,
            SolutionType.TRANSCRIPTION.value: transcription.start,
            SolutionType.DOCUMENT_INTELLIGENCE.value: document_intelligence.start,
            SolutionType.AZURE_STORAGE.value: azure_storage.start,
            SolutionType.AZURE_AI_VISION.value: azure_ai_vision.start,
        }
        return solutions[solution_name.upper()](
            backend_url=backend_url,
            log_level=log_level,
        )
    except KeyError:
        logger.error(f"Invalid solution name: {solution_name}, please choose one of {list(SolutionType)}")
        return
