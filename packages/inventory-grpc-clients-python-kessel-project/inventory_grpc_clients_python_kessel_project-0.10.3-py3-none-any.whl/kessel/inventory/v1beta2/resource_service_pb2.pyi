from kessel.inventory.v1beta2 import resource_pb2 as _resource_pb2
from google.api import annotations_pb2 as _annotations_pb2
from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReportResourceRequest(_message.Message):
    __slots__ = ("resource",)
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: _resource_pb2.Resource
    def __init__(self, resource: _Optional[_Union[_resource_pb2.Resource, _Mapping]] = ...) -> None: ...

class ReportResourceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteResourceRequest(_message.Message):
    __slots__ = ("local_resource_id", "reporter_type")
    LOCAL_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    REPORTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    local_resource_id: str
    reporter_type: str
    def __init__(self, local_resource_id: _Optional[str] = ..., reporter_type: _Optional[str] = ...) -> None: ...

class DeleteResourceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
