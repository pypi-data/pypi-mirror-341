from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateUploadedFile")


@_attrs_define
class CreateUploadedFile:
    """
    Attributes:
        name (str): The unique name to give to the new file that will be uploaded.
        extension (str): The file extension of the new file to be uploaded, e.g. ".csv"
        description (Union[None, Unset, str]): The description for the new file.
        make_name_unique (Union[None, Unset, bool]): If true, the system will generate a unique name for this file.
        associated_run_id (Union[None, Unset, int]): If set and MakeNameUnique is true, the system will use the
            associated run to generate a unique name for this file.
    """

    name: str
    extension: str
    description: Union[None, Unset, str] = UNSET
    make_name_unique: Union[None, Unset, bool] = UNSET
    associated_run_id: Union[None, Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        extension = self.extension

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

        associated_run_id: Union[None, Unset, int]
        if isinstance(self.associated_run_id, Unset):
            associated_run_id = UNSET
        else:
            associated_run_id = self.associated_run_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "extension": extension,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if make_name_unique is not UNSET:
            field_dict["makeNameUnique"] = make_name_unique
        if associated_run_id is not UNSET:
            field_dict["associatedRunId"] = associated_run_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        extension = d.pop("extension")

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

        def _parse_associated_run_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        associated_run_id = _parse_associated_run_id(d.pop("associatedRunId", UNSET))

        create_uploaded_file = cls(
            name=name,
            extension=extension,
            description=description,
            make_name_unique=make_name_unique,
            associated_run_id=associated_run_id,
        )

        return create_uploaded_file
