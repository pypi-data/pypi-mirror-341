from google.api import annotations_pb2 as _annotations_pb2
from kessel.inventory.v1beta2 import common_pb2 as _common_pb2
from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LookupResourcesRequest(_message.Message):
    __slots__ = ("resource_type", "relation", "subject", "pagination", "consistency")
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    CONSISTENCY_FIELD_NUMBER: _ClassVar[int]
    resource_type: _common_pb2.ObjectType
    relation: str
    subject: _common_pb2.SubjectReference
    pagination: _common_pb2.RequestPagination
    consistency: _common_pb2.Consistency
    def __init__(self, resource_type: _Optional[_Union[_common_pb2.ObjectType, _Mapping]] = ..., relation: _Optional[str] = ..., subject: _Optional[_Union[_common_pb2.SubjectReference, _Mapping]] = ..., pagination: _Optional[_Union[_common_pb2.RequestPagination, _Mapping]] = ..., consistency: _Optional[_Union[_common_pb2.Consistency, _Mapping]] = ...) -> None: ...

class LookupResourcesResponse(_message.Message):
    __slots__ = ("resource", "pagination", "consistency_token")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    CONSISTENCY_TOKEN_FIELD_NUMBER: _ClassVar[int]
    resource: _common_pb2.ObjectReference
    pagination: _common_pb2.ResponsePagination
    consistency_token: _common_pb2.ConsistencyToken
    def __init__(self, resource: _Optional[_Union[_common_pb2.ObjectReference, _Mapping]] = ..., pagination: _Optional[_Union[_common_pb2.ResponsePagination, _Mapping]] = ..., consistency_token: _Optional[_Union[_common_pb2.ConsistencyToken, _Mapping]] = ...) -> None: ...
