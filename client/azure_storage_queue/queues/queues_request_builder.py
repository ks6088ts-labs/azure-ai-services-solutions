from __future__ import annotations
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
    from ...models.create_queue_request import CreateQueueRequest
    from ...models.create_queue_response import CreateQueueResponse
    from ...models.h_t_t_p_validation_error import HTTPValidationError
    from .item.with_queue_name_item_request_builder import WithQueue_nameItemRequestBuilder

class QueuesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_storage_queue/queues
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new QueuesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_storage_queue/queues", path_parameters)
    
    def by_queue_name(self,queue_name: str) -> WithQueue_nameItemRequestBuilder:
        """
        Gets an item from the client.azure_storage_queue.queues.item collection
        param queue_name: Unique identifier of the item
        Returns: WithQueue_nameItemRequestBuilder
        """
        if not queue_name:
            raise TypeError("queue_name cannot be null.")
        from .item.with_queue_name_item_request_builder import WithQueue_nameItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["queue_name"] = queue_name
        return WithQueue_nameItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def post(self,body: Optional[CreateQueueRequest] = None, request_configuration: Optional[RequestConfiguration] = None) -> Optional[CreateQueueResponse]:
        """
        Create Queue
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[CreateQueueResponse]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from ...models.h_t_t_p_validation_error import HTTPValidationError

        error_mapping: Dict[str, ParsableFactory] = {
            "422": HTTPValidationError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ...models.create_queue_response import CreateQueueResponse

        return await self.request_adapter.send_async(request_info, CreateQueueResponse, error_mapping)
    
    def to_post_request_information(self,body: Optional[CreateQueueRequest] = None, request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Create Queue
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> QueuesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: QueuesRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return QueuesRequestBuilder(self.request_adapter, raw_url)
    

