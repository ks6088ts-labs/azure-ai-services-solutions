from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class DeleteMessageRequest(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The message_id property
    message_id: Optional[str] = None
    # The pop_receipt property
    pop_receipt: Optional[str] = None
    # The queue_name property
    queue_name: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> DeleteMessageRequest:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DeleteMessageRequest
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return DeleteMessageRequest()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "message_id": lambda n : setattr(self, 'message_id', n.get_str_value()),
            "pop_receipt": lambda n : setattr(self, 'pop_receipt', n.get_str_value()),
            "queue_name": lambda n : setattr(self, 'queue_name', n.get_str_value()),
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
        writer.write_str_value("message_id", self.message_id)
        writer.write_str_value("pop_receipt", self.pop_receipt)
        writer.write_str_value("queue_name", self.queue_name)
        writer.write_additional_data_value(self.additional_data)
    

