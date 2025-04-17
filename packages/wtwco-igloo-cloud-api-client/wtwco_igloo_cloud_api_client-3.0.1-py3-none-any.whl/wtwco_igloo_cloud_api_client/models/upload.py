from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Upload")


@_attrs_define
class Upload:
    """
    Attributes:
        sas_link (Union[None, Unset, str]): The Azure SAS URL, identifying the blob to upload the file contents to in
            Azure Blob Storage.
        identifier (Union[None, Unset, str]): The upload identifier to use in calls to UpdateProgress or CancelUpload.
    """

    sas_link: Union[None, Unset, str] = UNSET
    identifier: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        sas_link: Union[None, Unset, str]
        if isinstance(self.sas_link, Unset):
            sas_link = UNSET
        else:
            sas_link = self.sas_link

        identifier: Union[None, Unset, str]
        if isinstance(self.identifier, Unset):
            identifier = UNSET
        else:
            identifier = self.identifier

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if sas_link is not UNSET:
            field_dict["sasLink"] = sas_link
        if identifier is not UNSET:
            field_dict["identifier"] = identifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_sas_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sas_link = _parse_sas_link(d.pop("sasLink", UNSET))

        def _parse_identifier(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        identifier = _parse_identifier(d.pop("identifier", UNSET))

        upload = cls(
            sas_link=sas_link,
            identifier=identifier,
        )

        return upload
