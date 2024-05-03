from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.api_error import APIError
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .validation_error import ValidationError

@dataclass
class HTTPValidationError(APIError):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The detail property
    detail: Optional[List[ValidationError]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> HTTPValidationError:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: HTTPValidationError
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return HTTPValidationError()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .validation_error import ValidationError

        from .validation_error import ValidationError

        fields: Dict[str, Callable[[Any], None]] = {
            "detail": lambda n : setattr(self, 'detail', n.get_collection_of_object_values(ValidationError)),
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
        writer.write_collection_of_object_values("detail", self.detail)
        writer.write_additional_data_value(self.additional_data)
    
    @property
    def primary_message(self) -> str:
        """
        The primary error message.
        """
        return super().message

