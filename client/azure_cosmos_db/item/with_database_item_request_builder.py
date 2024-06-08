from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_container_item_request_builder import WithContainer_ItemRequestBuilder

class WithDatabase_ItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_cosmos_db/{database_id}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new WithDatabase_ItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_cosmos_db/{database_id}", path_parameters)
    
    def by_container_id(self,container_id: str) -> WithContainer_ItemRequestBuilder:
        """
        Gets an item from the client.azure_cosmos_db.item.item collection
        param container_id: Unique identifier of the item
        Returns: WithContainer_ItemRequestBuilder
        """
        if not container_id:
            raise TypeError("container_id cannot be null.")
        from .item.with_container_item_request_builder import WithContainer_ItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["container_id"] = container_id
        return WithContainer_ItemRequestBuilder(self.request_adapter, url_tpl_params)
    

