from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .container.container_request_builder import ContainerRequestBuilder
    from .database.database_request_builder import DatabaseRequestBuilder
    from .item.item_request_builder import ItemRequestBuilder
    from .item.with_database_item_request_builder import WithDatabase_ItemRequestBuilder

class Azure_cosmos_dbRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_cosmos_db
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new Azure_cosmos_dbRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_cosmos_db", path_parameters)
    
    def by_database_id(self,database_id: str) -> WithDatabase_ItemRequestBuilder:
        """
        Gets an item from the client.azure_cosmos_db.item collection
        param database_id: Unique identifier of the item
        Returns: WithDatabase_ItemRequestBuilder
        """
        if not database_id:
            raise TypeError("database_id cannot be null.")
        from .item.with_database_item_request_builder import WithDatabase_ItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["database_id"] = database_id
        return WithDatabase_ItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    @property
    def container(self) -> ContainerRequestBuilder:
        """
        The container property
        """
        from .container.container_request_builder import ContainerRequestBuilder

        return ContainerRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def database(self) -> DatabaseRequestBuilder:
        """
        The database property
        """
        from .database.database_request_builder import DatabaseRequestBuilder

        return DatabaseRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def item(self) -> ItemRequestBuilder:
        """
        The item property
        """
        from .item.item_request_builder import ItemRequestBuilder

        return ItemRequestBuilder(self.request_adapter, self.path_parameters)
    

