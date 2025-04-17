from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_version import ModelVersion


T = TypeVar("T", bound="Model")


@_attrs_define
class Model:
    """
    Attributes:
        name (Union[None, Unset, str]): The name of the model.
        versions (Union[None, Unset, list['ModelVersion']]): The list of available versions for this model.
    """

    name: Union[None, Unset, str] = UNSET
    versions: Union[None, Unset, list["ModelVersion"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        versions: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.versions, Unset):
            versions = UNSET
        elif isinstance(self.versions, list):
            versions = []
            for versions_type_0_item_data in self.versions:
                versions_type_0_item = versions_type_0_item_data.to_dict()
                versions.append(versions_type_0_item)

        else:
            versions = self.versions

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if versions is not UNSET:
            field_dict["versions"] = versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.model_version import ModelVersion

        d = src_dict.copy()

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_versions(data: object) -> Union[None, Unset, list["ModelVersion"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                versions_type_0 = []
                _versions_type_0 = data
                for versions_type_0_item_data in _versions_type_0:
                    versions_type_0_item = ModelVersion.from_dict(versions_type_0_item_data)

                    versions_type_0.append(versions_type_0_item)

                return versions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["ModelVersion"]], data)

        versions = _parse_versions(d.pop("versions", UNSET))

        model = cls(
            name=name,
            versions=versions,
        )

        return model
