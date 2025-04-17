from kessel.inventory.v1beta2 import reporter_data_pb2 as _reporter_data_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Resource(_message.Message):
    __slots__ = ("inventory_id", "resource_type", "reporter_data", "common_resource_data")
    INVENTORY_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPORTER_DATA_FIELD_NUMBER: _ClassVar[int]
    COMMON_RESOURCE_DATA_FIELD_NUMBER: _ClassVar[int]
    inventory_id: str
    resource_type: str
    reporter_data: _reporter_data_pb2.ReporterData
    common_resource_data: _struct_pb2.Struct
    def __init__(self, inventory_id: _Optional[str] = ..., resource_type: _Optional[str] = ..., reporter_data: _Optional[_Union[_reporter_data_pb2.ReporterData, _Mapping]] = ..., common_resource_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
