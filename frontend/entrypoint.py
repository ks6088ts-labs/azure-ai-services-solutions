import logging

from frontend.solutions import azure_storage, document_intelligence, sandbox, transcription
from frontend.solutions.types import SolutionType

logger = logging.getLogger(__name__)


def start(
    solution_type: SolutionType,
    backend_url: str,
    log_level: int,
) -> None:
    if solution_type == SolutionType.SANDBOX:
        return sandbox.start(
            backend_url=backend_url,
            log_level=log_level,
        )
    if solution_type == SolutionType.TRANSCRIPTION:
        return transcription.start(
            backend_url=backend_url,
            log_level=log_level,
        )
    if solution_type == SolutionType.DOCUMENT_INTELLIGENCE:
        return document_intelligence.start(
            backend_url=backend_url,
            log_level=log_level,
        )
    if solution_type == SolutionType.AZURE_STORAGE:
        return azure_storage.start(
            backend_url=backend_url,
            log_level=log_level,
        )
