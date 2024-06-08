from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .create_item_response_item import CreateItemResponse_item

@dataclass
class CreateItemResponse(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The container_id property
    container_id: Optional[str] = None
    # The database_id property
    database_id: Optional[str] = None
    # The item property
    item: Optional[CreateItemResponse_item] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> CreateItemResponse:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: CreateItemResponse
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return CreateItemResponse()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .create_item_response_item import CreateItemResponse_item

        from .create_item_response_item import CreateItemResponse_item

        fields: Dict[str, Callable[[Any], None]] = {
            "container_id": lambda n : setattr(self, 'container_id', n.get_str_value()),
            "database_id": lambda n : setattr(self, 'database_id', n.get_str_value()),
            "item": lambda n : setattr(self, 'item', n.get_object_value(CreateItemResponse_item)),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("container_id", self.container_id)
        writer.write_str_value("database_id", self.database_id)
        writer.write_object_value("item", self.item)
        writer.write_additional_data_value(self.additional_data)
    

