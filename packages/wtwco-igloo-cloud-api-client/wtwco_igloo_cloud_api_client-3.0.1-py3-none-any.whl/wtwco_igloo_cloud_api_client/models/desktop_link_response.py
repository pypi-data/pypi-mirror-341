from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.desktop_link import DesktopLink
    from ..models.message import Message


T = TypeVar("T", bound="DesktopLinkResponse")


@_attrs_define
class DesktopLinkResponse:
    """
    Attributes:
        messages (Union[None, Unset, list['Message']]):
        result (Union[Unset, DesktopLink]):
    """

    messages: Union[None, Unset, list["Message"]] = UNSET
    result: Union[Unset, "DesktopLink"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        messages: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.messages, Unset):
            messages = UNSET
        elif isinstance(self.messages, list):
            messages = []
            for messages_type_0_item_data in self.messages:
                messages_type_0_item = messages_type_0_item_data.to_dict()
                messages.append(messages_type_0_item)

        else:
            messages = self.messages

        result: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if messages is not UNSET:
            field_dict["messages"] = messages
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.desktop_link import DesktopLink
        from ..models.message import Message

        d = src_dict.copy()

        def _parse_messages(data: object) -> Union[None, Unset, list["Message"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                messages_type_0 = []
                _messages_type_0 = data
                for messages_type_0_item_data in _messages_type_0:
                    messages_type_0_item = Message.from_dict(messages_type_0_item_data)

                    messages_type_0.append(messages_type_0_item)

                return messages_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Message"]], data)

        messages = _parse_messages(d.pop("messages", UNSET))

        _result = d.pop("result", UNSET)
        result: Union[Unset, DesktopLink]
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = DesktopLink.from_dict(_result)

        desktop_link_response = cls(
            messages=messages,
            result=result,
        )

        return desktop_link_response
