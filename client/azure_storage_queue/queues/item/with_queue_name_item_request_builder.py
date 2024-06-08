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
    from ....models.delete_queue_response import DeleteQueueResponse
    from ....models.h_t_t_p_validation_error import HTTPValidationError

class WithQueue_nameItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_storage_queue/queues/{queue_name}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new WithQueue_nameItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_storage_queue/queues/{queue_name}", path_parameters)
    
    async def delete(self,request_configuration: Optional[RequestConfiguration] = None) -> Optional[DeleteQueueResponse]:
        """
        Delete Queue
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[DeleteQueueResponse]
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        from ....models.h_t_t_p_validation_error import HTTPValidationError

        error_mapping: Dict[str, ParsableFactory] = {
            "422": HTTPValidationError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.delete_queue_response import DeleteQueueResponse

        return await self.request_adapter.send_async(request_info, DeleteQueueResponse, error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Delete Queue
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.DELETE, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> WithQueue_nameItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: WithQueue_nameItemRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return WithQueue_nameItemRequestBuilder(self.request_adapter, raw_url)
    

