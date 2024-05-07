from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.multipart_body import MultipartBody
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ...models.chat_completion_with_vision_response import ChatCompletionWithVisionResponse
    from ...models.h_t_t_p_validation_error import HTTPValidationError

class Chat_completions_with_visionRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_openai/chat_completions_with_vision
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new Chat_completions_with_visionRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_openai/chat_completions_with_vision{?system_prompt*,user_prompt*}", path_parameters)
    
    async def post(self,body: Optional[MultipartBody] = None, request_configuration: Optional[RequestConfiguration] = None) -> Optional[ChatCompletionWithVisionResponse]:
        """
        Create Chat Completions With Vision
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ChatCompletionWithVisionResponse]
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
        from ...models.chat_completion_with_vision_response import ChatCompletionWithVisionResponse

        return await self.request_adapter.send_async(request_info, ChatCompletionWithVisionResponse, error_mapping)
    
    def to_post_request_information(self,body: Optional[MultipartBody] = None, request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Create Chat Completions With Vision
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "multipart/form-data", body)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> Chat_completions_with_visionRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: Chat_completions_with_visionRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return Chat_completions_with_visionRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class Chat_completions_with_visionRequestBuilderPostQueryParameters():
        """
        Create Chat Completions With Vision
        """
        system_prompt: Optional[str] = None

        user_prompt: Optional[str] = None

    

