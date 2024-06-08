from __future__ import annotations
from kiota_abstractions.api_client_builder import enable_backing_store_for_serialization_writer_factory, register_default_deserializer, register_default_serializer
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.serialization import ParseNodeFactoryRegistry, SerializationWriterFactoryRegistry
from kiota_serialization_form.form_parse_node_factory import FormParseNodeFactory
from kiota_serialization_form.form_serialization_writer_factory import FormSerializationWriterFactory
from kiota_serialization_json.json_parse_node_factory import JsonParseNodeFactory
from kiota_serialization_json.json_serialization_writer_factory import JsonSerializationWriterFactory
from kiota_serialization_multipart.multipart_serialization_writer_factory import MultipartSerializationWriterFactory
from kiota_serialization_text.text_parse_node_factory import TextParseNodeFactory
from kiota_serialization_text.text_serialization_writer_factory import TextSerializationWriterFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .azure_ai_document_intelligence.azure_ai_document_intelligence_request_builder import Azure_ai_document_intelligenceRequestBuilder
    from .azure_ai_vision.azure_ai_vision_request_builder import Azure_ai_visionRequestBuilder
    from .azure_cosmos_db.azure_cosmos_db_request_builder import Azure_cosmos_dbRequestBuilder
    from .azure_event_grid.azure_event_grid_request_builder import Azure_event_gridRequestBuilder
    from .azure_openai.azure_openai_request_builder import Azure_openaiRequestBuilder
    from .azure_storage_blob.azure_storage_blob_request_builder import Azure_storage_blobRequestBuilder
    from .azure_storage_queue.azure_storage_queue_request_builder import Azure_storage_queueRequestBuilder

class ApiClient(BaseRequestBuilder):
    """
    The main entry point of the SDK, exposes the configuration and the fluent API.
    """
    def __init__(self,request_adapter: RequestAdapter) -> None:
        """
        Instantiates a new ApiClient and sets the default values.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        if not request_adapter:
            raise TypeError("request_adapter cannot be null.")
        super().__init__(request_adapter, "{+baseurl}", None)
        register_default_serializer(JsonSerializationWriterFactory)
        register_default_serializer(TextSerializationWriterFactory)
        register_default_serializer(FormSerializationWriterFactory)
        register_default_serializer(MultipartSerializationWriterFactory)
        register_default_deserializer(JsonParseNodeFactory)
        register_default_deserializer(TextParseNodeFactory)
        register_default_deserializer(FormParseNodeFactory)
    
    @property
    def azure_ai_document_intelligence(self) -> Azure_ai_document_intelligenceRequestBuilder:
        """
        The azure_ai_document_intelligence property
        """
        from .azure_ai_document_intelligence.azure_ai_document_intelligence_request_builder import Azure_ai_document_intelligenceRequestBuilder

        return Azure_ai_document_intelligenceRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def azure_ai_vision(self) -> Azure_ai_visionRequestBuilder:
        """
        The azure_ai_vision property
        """
        from .azure_ai_vision.azure_ai_vision_request_builder import Azure_ai_visionRequestBuilder

        return Azure_ai_visionRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def azure_cosmos_db(self) -> Azure_cosmos_dbRequestBuilder:
        """
        The azure_cosmos_db property
        """
        from .azure_cosmos_db.azure_cosmos_db_request_builder import Azure_cosmos_dbRequestBuilder

        return Azure_cosmos_dbRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def azure_event_grid(self) -> Azure_event_gridRequestBuilder:
        """
        The azure_event_grid property
        """
        from .azure_event_grid.azure_event_grid_request_builder import Azure_event_gridRequestBuilder

        return Azure_event_gridRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def azure_openai(self) -> Azure_openaiRequestBuilder:
        """
        The azure_openai property
        """
        from .azure_openai.azure_openai_request_builder import Azure_openaiRequestBuilder

        return Azure_openaiRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def azure_storage_blob(self) -> Azure_storage_blobRequestBuilder:
        """
        The azure_storage_blob property
        """
        from .azure_storage_blob.azure_storage_blob_request_builder import Azure_storage_blobRequestBuilder

        return Azure_storage_blobRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def azure_storage_queue(self) -> Azure_storage_queueRequestBuilder:
        """
        The azure_storage_queue property
        """
        from .azure_storage_queue.azure_storage_queue_request_builder import Azure_storage_queueRequestBuilder

        return Azure_storage_queueRequestBuilder(self.request_adapter, self.path_parameters)
    

