from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="Workspace")


@_attrs_define
class Workspace:
    """
    Attributes:
        id (int): The id the workspace.
        name (Union[None, str]): The name of the workspace.
        description (Union[None, str]): The description of the workspace.
        project_count (int): The number of projects in the workspace
    """

    id: int
    name: Union[None, str]
    description: Union[None, str]
    project_count: int

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name: Union[None, str]
        name = self.name

        description: Union[None, str]
        description = self.description

        project_count = self.project_count

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "projectCount": project_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        project_count = d.pop("projectCount")

        workspace = cls(
            id=id,
            name=name,
            description=description,
            project_count=project_count,
        )

        return workspace
