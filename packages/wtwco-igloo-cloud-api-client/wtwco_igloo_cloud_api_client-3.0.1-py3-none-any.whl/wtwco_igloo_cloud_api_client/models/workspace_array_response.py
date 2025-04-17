from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.message import Message
    from ..models.workspace import Workspace


T = TypeVar("T", bound="WorkspaceArrayResponse")


@_attrs_define
class WorkspaceArrayResponse:
    """
    Attributes:
        messages (Union[None, Unset, list['Message']]):
        result (Union[None, Unset, list['Workspace']]):
    """

    messages: Union[None, Unset, list["Message"]] = UNSET
    result: Union[None, Unset, list["Workspace"]] = UNSET

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

        result: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, list):
            result = []
            for result_type_0_item_data in self.result:
                result_type_0_item = result_type_0_item_data.to_dict()
                result.append(result_type_0_item)

        else:
            result = self.result

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if messages is not UNSET:
            field_dict["messages"] = messages
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.message import Message
        from ..models.workspace import Workspace

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

        def _parse_result(data: object) -> Union[None, Unset, list["Workspace"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                result_type_0 = []
                _result_type_0 = data
                for result_type_0_item_data in _result_type_0:
                    result_type_0_item = Workspace.from_dict(result_type_0_item_data)

                    result_type_0.append(result_type_0_item)

                return result_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Workspace"]], data)

        result = _parse_result(d.pop("result", UNSET))

        workspace_array_response = cls(
            messages=messages,
            result=result,
        )

        return workspace_array_response
