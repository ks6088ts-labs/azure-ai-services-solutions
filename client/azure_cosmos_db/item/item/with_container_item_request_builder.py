from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_item_item_request_builder import WithItem_ItemRequestBuilder

class WithContainer_ItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_cosmos_db/{database_id}/{container_id}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new WithContainer_ItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_cosmos_db/{database_id}/{container_id}", path_parameters)
    
    def by_item_id(self,item_id: str) -> WithItem_ItemRequestBuilder:
        """
        Gets an item from the client.azure_cosmos_db.item.item.item collection
        param item_id: Unique identifier of the item
        Returns: WithItem_ItemRequestBuilder
        """
        if not item_id:
            raise TypeError("item_id cannot be null.")
        from .item.with_item_item_request_builder import WithItem_ItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["item_id"] = item_id
        return WithItem_ItemRequestBuilder(self.request_adapter, url_tpl_params)
    

