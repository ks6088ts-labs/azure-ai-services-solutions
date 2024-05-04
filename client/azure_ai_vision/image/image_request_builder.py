from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .analyze.analyze_request_builder import AnalyzeRequestBuilder
    from .vectorize.vectorize_request_builder import VectorizeRequestBuilder

class ImageRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /azure_ai_vision/image
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ImageRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/azure_ai_vision/image", path_parameters)
    
    @property
    def analyze(self) -> AnalyzeRequestBuilder:
        """
        The analyze property
        """
        from .analyze.analyze_request_builder import AnalyzeRequestBuilder

        return AnalyzeRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def vectorize(self) -> VectorizeRequestBuilder:
        """
        The vectorize property
        """
        from .vectorize.vectorize_request_builder import VectorizeRequestBuilder

        return VectorizeRequestBuilder(self.request_adapter, self.path_parameters)
    

