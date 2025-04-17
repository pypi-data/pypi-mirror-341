from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunResult")


@_attrs_define
class RunResult:
    """
    Attributes:
        name (Union[None, Unset, str]): The name of the run result, to be used in the API.
        display_name (Union[None, Unset, str]): The user-friendly display name of the run result.
        is_in_use (Union[Unset, bool]): Set to true if the run is calculated and the model generated some output for
            this run result.
        help_ (Union[None, Unset, str]): The link to the documentation for this run result.
    """

    name: Union[None, Unset, str] = UNSET
    display_name: Union[None, Unset, str] = UNSET
    is_in_use: Union[Unset, bool] = UNSET
    help_: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        display_name: Union[None, Unset, str]
        if isinstance(self.display_name, Unset):
            display_name = UNSET
        else:
            display_name = self.display_name

        is_in_use = self.is_in_use

        help_: Union[None, Unset, str]
        if isinstance(self.help_, Unset):
            help_ = UNSET
        else:
            help_ = self.help_

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if is_in_use is not UNSET:
            field_dict["isInUse"] = is_in_use
        if help_ is not UNSET:
            field_dict["help"] = help_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_display_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        display_name = _parse_display_name(d.pop("displayName", UNSET))

        is_in_use = d.pop("isInUse", UNSET)

        def _parse_help_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        help_ = _parse_help_(d.pop("help", UNSET))

        run_result = cls(
            name=name,
            display_name=display_name,
            is_in_use=is_in_use,
            help_=help_,
        )

        return run_result
