from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ...models.h_t_t_p_validation_error import HTTPValidationError

class Event_grid_eventRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_event_grid/event_grid_event
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new Event_grid_eventRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_event_grid/event_grid_event{?data*,data_version*,event_type*,subject*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration] = None) -> Optional[UntypedNode]:
        """
        Send Event Grid Event
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[UntypedNode]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from ...models.h_t_t_p_validation_error import HTTPValidationError

        error_mapping: Dict[str, ParsableFactory] = {
            "422": HTTPValidationError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_async(request_info, UntypedNode, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Send Event Grid Event
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> Event_grid_eventRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: Event_grid_eventRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return Event_grid_eventRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class Event_grid_eventRequestBuilderPostQueryParameters():
        """
        Send Event Grid Event
        """
        data: Optional[str] = None

        data_version: Optional[str] = None

        event_type: Optional[str] = None

        subject: Optional[str] = None

    

