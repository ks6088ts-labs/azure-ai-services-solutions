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
    from ...models.delete_message_request import DeleteMessageRequest
    from ...models.delete_message_response import DeleteMessageResponse
    from ...models.h_t_t_p_validation_error import HTTPValidationError
    from ...models.send_message_request import SendMessageRequest
    from ...models.send_message_response import SendMessageResponse

class MessagesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_storage_queue/messages
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new MessagesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_storage_queue/messages?queue_name={queue_name}{&max_messages*}", path_parameters)
    
    async def delete(self,body: Optional[DeleteMessageRequest] = None, request_configuration: Optional[RequestConfiguration] = None) -> Optional[DeleteMessageResponse]:
        """
        Delete Message
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[DeleteMessageResponse]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_delete_request_information(
            body, request_configuration
        )
        from ...models.h_t_t_p_validation_error import HTTPValidationError

        error_mapping: Dict[str, ParsableFactory] = {
            "422": HTTPValidationError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ...models.delete_message_response import DeleteMessageResponse

        return await self.request_adapter.send_async(request_info, DeleteMessageResponse, error_mapping)
    
    async def get(self,request_configuration: Optional[RequestConfiguration] = None) -> Optional[UntypedNode]:
        """
        Receive Messages
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[UntypedNode]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ...models.h_t_t_p_validation_error import HTTPValidationError

        error_mapping: Dict[str, ParsableFactory] = {
            "422": HTTPValidationError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_async(request_info, UntypedNode, error_mapping)
    
    async def post(self,body: Optional[SendMessageRequest] = None, request_configuration: Optional[RequestConfiguration] = None) -> Optional[SendMessageResponse]:
        """
        Send Message
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[SendMessageResponse]
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
        from ...models.send_message_response import SendMessageResponse

        return await self.request_adapter.send_async(request_info, SendMessageResponse, error_mapping)
    
    def to_delete_request_information(self,body: Optional[DeleteMessageRequest] = None, request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Delete Message
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.DELETE, '{+baseurl}/azure_storage_queue/messages', self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Receive Messages
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: Optional[SendMessageRequest] = None, request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Send Message
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, '{+baseurl}/azure_storage_queue/messages', self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> MessagesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: MessagesRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return MessagesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class MessagesRequestBuilderGetQueryParameters():
        """
        Receive Messages
        """
        max_messages: Optional[int] = None

        queue_name: Optional[str] = None

    

