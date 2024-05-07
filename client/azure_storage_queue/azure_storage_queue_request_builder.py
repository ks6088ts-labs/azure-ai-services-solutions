from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .messages.messages_request_builder import MessagesRequestBuilder
    from .queues.queues_request_builder import QueuesRequestBuilder

class Azure_storage_queueRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_storage_queue
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new Azure_storage_queueRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_storage_queue", path_parameters)
    
    @property
    def messages(self) -> MessagesRequestBuilder:
        """
        The messages property
        """
        from .messages.messages_request_builder import MessagesRequestBuilder

        return MessagesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def queues(self) -> QueuesRequestBuilder:
        """
        The queues property
        """
        from .queues.queues_request_builder import QueuesRequestBuilder

        return QueuesRequestBuilder(self.request_adapter, self.path_parameters)
    

