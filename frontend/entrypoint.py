import logging

from frontend.pages import misc as misc_pages

logger = logging.getLogger(__name__)


def start(
    solution_name: str,
    backend_url: str,
    log_level: int,
):
    # add solution-specific logic here
    if solution_name == "hoge":
        pass
    else:
        misc_pages.start(
            backend_url=backend_url,
            log_level=log_level,
        )
