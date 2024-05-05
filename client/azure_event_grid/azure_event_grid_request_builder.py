from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .event_grid_event.event_grid_event_request_builder import Event_grid_eventRequestBuilder

class Azure_event_gridRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_event_grid
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new Azure_event_gridRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_event_grid", path_parameters)
    
    @property
    def event_grid_event(self) -> Event_grid_eventRequestBuilder:
        """
        The event_grid_event property
        """
        from .event_grid_event.event_grid_event_request_builder import Event_grid_eventRequestBuilder

        return Event_grid_eventRequestBuilder(self.request_adapter, self.path_parameters)
    

