from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Links")


@_attrs_define
class Links:
    """Provides the URL to use to fetch the values of the list table if this column is of type Id.

    Attributes:
        self_ (Union[None, Unset, str]):
    """

    self_: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        self_: Union[None, Unset, str]
        if isinstance(self.self_, Unset):
            self_ = UNSET
        else:
            self_ = self.self_

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_self_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        self_ = _parse_self_(d.pop("self", UNSET))

        links = cls(
            self_=self_,
        )

        return links
