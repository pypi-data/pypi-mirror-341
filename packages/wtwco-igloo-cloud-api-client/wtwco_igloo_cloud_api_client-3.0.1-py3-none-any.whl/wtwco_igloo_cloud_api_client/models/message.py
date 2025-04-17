from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.message_type import MessageType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Message")


@_attrs_define
class Message:
    """
    Attributes:
        code (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        message_type (Union[Unset, MessageType]):
    """

    code: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    message_type: Union[Unset, MessageType] = UNSET

    def to_dict(self) -> dict[str, Any]:
        code: Union[None, Unset, str]
        if isinstance(self.code, Unset):
            code = UNSET
        else:
            code = self.code

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        message_type: Union[Unset, str] = UNSET
        if not isinstance(self.message_type, Unset):
            message_type = self.message_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if description is not UNSET:
            field_dict["description"] = description
        if message_type is not UNSET:
            field_dict["messageType"] = message_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        code = _parse_code(d.pop("code", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _message_type = d.pop("messageType", UNSET)
        message_type: Union[Unset, MessageType]
        if isinstance(_message_type, Unset):
            message_type = UNSET
        else:
            message_type = MessageType(_message_type)

        message = cls(
            code=code,
            description=description,
            message_type=message_type,
        )

        return message
