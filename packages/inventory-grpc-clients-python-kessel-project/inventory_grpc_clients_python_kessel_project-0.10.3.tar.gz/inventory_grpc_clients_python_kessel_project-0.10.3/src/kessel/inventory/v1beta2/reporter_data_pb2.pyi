from google.protobuf import struct_pb2 as _struct_pb2
from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReporterData(_message.Message):
    __slots__ = ("reporter_type", "reporter_instance_id", "reporter_version", "local_resource_id", "api_href", "console_href", "resource_data")
    REPORTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPORTER_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    REPORTER_VERSION_FIELD_NUMBER: _ClassVar[int]
    LOCAL_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    API_HREF_FIELD_NUMBER: _ClassVar[int]
    CONSOLE_HREF_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_DATA_FIELD_NUMBER: _ClassVar[int]
    reporter_type: str
    reporter_instance_id: str
    reporter_version: str
    local_resource_id: str
    api_href: str
    console_href: str
    resource_data: _struct_pb2.Struct
    def __init__(self, reporter_type: _Optional[str] = ..., reporter_instance_id: _Optional[str] = ..., reporter_version: _Optional[str] = ..., local_resource_id: _Optional[str] = ..., api_href: _Optional[str] = ..., console_href: _Optional[str] = ..., resource_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
