from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateRun")


@_attrs_define
class CreateRun:
    """
    Attributes:
        name (str): The name to give to the new run, this must be unique.
        parent_id (int): The id value for the run that you want to be the parent of this new run.
        description (Union[None, Unset, str]): The description for the new run.
        make_name_unique (Union[None, Unset, bool]): If true then the system will ensure a unique name for this run is
            generated based on the name property supplied above. Default: False.
        auto_delete_minutes (Union[None, Unset, int]): If set, indicates that we wish the system to automatically delete
            the run and all of its data after this many minutes has elapsed.
    """

    name: str
    parent_id: int
    description: Union[None, Unset, str] = UNSET
    make_name_unique: Union[None, Unset, bool] = False
    auto_delete_minutes: Union[None, Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        parent_id = self.parent_id

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        make_name_unique: Union[None, Unset, bool]
        if isinstance(self.make_name_unique, Unset):
            make_name_unique = UNSET
        else:
            make_name_unique = self.make_name_unique

        auto_delete_minutes: Union[None, Unset, int]
        if isinstance(self.auto_delete_minutes, Unset):
            auto_delete_minutes = UNSET
        else:
            auto_delete_minutes = self.auto_delete_minutes

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "parentId": parent_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if make_name_unique is not UNSET:
            field_dict["makeNameUnique"] = make_name_unique
        if auto_delete_minutes is not UNSET:
            field_dict["autoDeleteMinutes"] = auto_delete_minutes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        parent_id = d.pop("parentId")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_make_name_unique(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        make_name_unique = _parse_make_name_unique(d.pop("makeNameUnique", UNSET))

        def _parse_auto_delete_minutes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        auto_delete_minutes = _parse_auto_delete_minutes(d.pop("autoDeleteMinutes", UNSET))

        create_run = cls(
            name=name,
            parent_id=parent_id,
            description=description,
            make_name_unique=make_name_unique,
            auto_delete_minutes=auto_delete_minutes,
        )

        return create_run
