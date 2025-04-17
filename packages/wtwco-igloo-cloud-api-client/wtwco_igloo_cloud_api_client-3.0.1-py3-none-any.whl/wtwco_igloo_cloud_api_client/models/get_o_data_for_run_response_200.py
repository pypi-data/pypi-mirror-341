from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_o_data_for_run_response_200_value_item import GetODataForRunResponse200ValueItem


T = TypeVar("T", bound="GetODataForRunResponse200")


@_attrs_define
class GetODataForRunResponse200:
    """
    Attributes:
        odata_context (Union[Unset, str]): A link to the metatadata for this table
        value (Union[Unset, list['GetODataForRunResponse200ValueItem']]): The data for the table. The types of
            properties will depend on the table being selected from and the columns requested by $select
    """

    odata_context: Union[Unset, str] = UNSET
    value: Union[Unset, list["GetODataForRunResponse200ValueItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        odata_context = self.odata_context

        value: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.value, Unset):
            value = []
            for value_item_data in self.value:
                value_item = value_item_data.to_dict()
                value.append(value_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if odata_context is not UNSET:
            field_dict["@odata.context"] = odata_context
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_o_data_for_run_response_200_value_item import GetODataForRunResponse200ValueItem

        d = src_dict.copy()
        odata_context = d.pop("@odata.context", UNSET)

        value = []
        _value = d.pop("value", UNSET)
        for value_item_data in _value or []:
            value_item = GetODataForRunResponse200ValueItem.from_dict(value_item_data)

            value.append(value_item)

        get_o_data_for_run_response_200 = cls(
            odata_context=odata_context,
            value=value,
        )

        get_o_data_for_run_response_200.additional_properties = d
        return get_o_data_for_run_response_200

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
